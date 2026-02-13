# 配置模块

## 引言

在ICore 中提供了一套非常好用的配置模块，用户可以简单的添加配置信息，可以很方便的引用到配置信息。举个例子，我们在ICore中使用到的宏注解： `$SetAppThreadCount(4)`便是向系统写入配置信息:

```cpp
$SetAppThreadCount(4)
int main(int argc, char* argv[]) {
    IApplication app(argc, argv);
    return app.run();
}
```

而当需要引用这个配置信息的时候，也很简单：

```cpp
int IAsioApplication::run()
{
    detail::SignalHandler signal_handler;

    if(!m_threadCount){
        auto defaultCount = std::thread::hardware_concurrency() * 2;
        $ContextInt count{"/system/threadCount", defaultCount};
        m_threadCount = *count;
    }
    IAsioContext::instance().run(m_threadCount);

    return 0;
}
```

在第7行，我们使用 `$ContextInt` 类型来构造一个对象，对象的第一个内容是我们的配置信息所在的位置，第二个信息是默认值。

在实际的执行中，count 对象会在`/system/threadCount` 这个`json_pointer` 位置查找有没有json值，有的话，自动转换成 int 类型赋值给 count， 没有的话，则会使用默认值。

下面我们依次讲解其中的内容。

## 配置的类型

在ICore中，配置信息被分为两类：

- Context 配置
- profile 配置

context 配置是系统性的配置，他在程序完全启动之前有效。比如设置是否启动测试，是否屏蔽某一个 task， 设置多少线程以运行程序等等功能。

profile 是在程序完全启动之后，对功能的一个约束。比如我启动了一个http 服务器，那么接收的http 信息最多可以多长，header 信息有多长，这个取决于 profile 配置，我启动一个 IHttpPythonTest, 它的运行目录在哪里，这个也是取决于 profile 配置。

这样区分 context配置和 profile 配置可以很好的厘清框架配置和具体的功能配置之间的区别。用户在之后的操作中，更多的是使用 context 配置，而不修改 context 配置；而profile 配置，则会根据自己的需要定义一系列的 profile配置，并引用 profile 配置。



## 引用到配置

无论是 profile 类型的配置，还是context 类型的配置，他们存储配置的容器时一个 IJson 类型。用户添加配置时往IJson 类型里面添加字段，用户获取配置的时候时尝试查询该 IJson 对象，如果查询到了，会尝试将该对象转换成用户希望的类型，如果转换成功，则用户在 IJson 对象中查询到了配置，上述如果失败，对象会存储查询失败的信息，并尝试使用给定的默认值，如果没有默认值，则会使用默认构造函数构造一个对象出来。

### profile 配置的引用

profile 定义了一个获取引用的类：

```c++
template<typename T>
class IProfileImport : public IConfigImportInterface<T>
{
public:
    IProfileImport(std::string path);
    IProfileImport(std::string path, T value);

public:
    IProfileImport& operator =(const T& value) = delete;

protected:
    virtual IConfigManageInterface& getConfigManage() const final;
};

```

用户在这里可以传入 std::string 类型的 path 来进行获取数据。path 类型时 nlohmann/json的 json pointer 类型。用户也可以提供一个默认值给 IProfileImport, 如果配置查询失败的时候，则可以使用 默认值。

nlohmann/json 库中的 JSON Pointer 提供了一种简洁的方式来定位和操作 JSON 数据中的特定节点。通过类似 `/foo/bar/0` 的路径字符串（遵循 RFC 6901 标准），用户可直接访问嵌套结构，例如获取 `{"foo": {"bar": [42, 43]}}` 中的第一个元素 42。特殊字符（如 `/` 和 `~`）需转义为 `~1` 和 `~0`。使用 `json_pointer` 类构造路径后，可通过 `at()` 或 `operator[]` 访问数据，若路径无效会抛出 `out_of_range` 异常。该功能简化了深层数据的读写，同时兼容标准规范。

所以用户在写path的时候需要注意符合RFC6906的标准。

以下是一个使用 profile 类型的案例

```c++
IProfileImport<int> port{"/http/port", 8088};
server.setPort(*port);
```

注意这里用户使用 port 的时候需要通过 `*`  解引用操作符来获取其内部存储的实际值。

#### 简单的标记

上面的代码有一些繁琐，为了简单的获取到想要的配置信息我们对 `IProfileImport` 进行了重定义,如下：

```cpp
template<typename T>
using $Profile = IProfileImport<T>;

template<typename T>
using $ProfileMap = IProfileImport<std::map<std::string, T>>;

using $ProfileIJson = $Profile<IJson>;
using $ProfileBool = $Profile<bool>;
using $ProfileChar = $Profile<char>;
using $ProfileUChar = $Profile<uchar>;
using $ProfileSChar = $Profile<signed char>;
using $ProfileShort = $Profile<short>;
using $ProfileUShort = $Profile<ushort>;
using $ProfileInt = $Profile<int>;
using $ProfileUInt = $Profile<uint>;
using $ProfileLong = $Profile<long>;
using $ProfileULong = $Profile<ulong>;
using $ProfileLongLong = $Profile<long long>;
using $ProfileULongLong = $Profile<qulonglong>;
using $ProfileFloat = $Profile<float>;
using $ProfileDouble = $Profile<double>;
using $ProfileLongDouble = $Profile<long double>;

using $ProfileMapStdString = $ProfileMap<std::string>;
using $ProfileQString = $Profile<QString>;
using $ProfileStdString = $Profile<std::string>;
using $ProfileQStringList = $Profile<QStringList>;

using $IJson = $ProfileIJson;
using $Bool = $ProfileBool;
using $Char = $ProfileChar;
using $UChar = $ProfileUChar;
using $SChar = $ProfileSChar;
using $Short = $ProfileShort;
using $UShort = $ProfileUShort;
using $Int = $ProfileInt;
using $UInt = $ProfileUInt;
using $Long = $ProfileLong;
using $ULong = $ProfileULong;
using $LongLong = $ProfileLongLong;
using $ULongLong = $ProfileULongLong;
using $Float = $ProfileFloat;
using $Double = $ProfileDouble;
using $LongDouble = $ProfileLongDouble;

using $MapStdString = $ProfileMapStdString;
using $QString = $ProfileQString;
using $StdString = $ProfileStdString;
using $QStringList = $ProfileQStringList;
```

 在上面的代码中，我们列举了可能会用到的所有类型。类型的定义也很简单 `$` 加上类型首字母大写就可以了。

在上面的代码中，我们就可以改为如下的代码：

```cpp
$Int port{"/http/port", 8088};
server.setPort(*port);
```

 这样，配置更加简洁易懂。



#### 查询异常

在上面的代码中，如果查询异常，比如在 IJson对象中没有 `/http/port` 这个json pointer 对应的数据，或者 `/http/port` 这里面存储的是一个string类型，不能够被转换为 int 类型，或者它转换int 类型会超过 int 类型的范围，那么这个情况又该如何判断呢？

在 IProfileImport 类型中，对于结果有三种状态：

- 构造值 `InitializedValue`

  这个状态表示当前对象查询或者转换 json 值失败，而用户也没有提供默认值，那么配置对象中现在存储的值是一个默认值，对应的， $Bool 是 false， $Int 是 0， 而$QString 是  “” , 空字符串。、

  用户可以通过函数 `bool isInitializedValue() const;` 来判断当前值是否时构造值。

- 默认值 `DefaultValue`

  如果用户在构造 ProfileImport 对象时传入了默认值，那么在 json 查询或转换失败的时候，会使用默认值状态。

  用户可以通过 `bool isDefaultedValue() const;` 来判断是否时默认值。

- 加载值  `LoadedValue`,

  用户在json查询并转换成功的时候，IProfileImport 会变为 LoadedValue 状态。

  用户可以通过 `bool isLoadedValue() const` 来判断当前的值是否时加载值。

#### 使用配置值

对于一个 IProfileImport 对象而言，用以下两种方式使用里面的值

- 通过解引用对象来获取值
- 通过 value 函数来获取值

示例如下：

```cpp
$Int port{"/http/port", 8088};

// 方式1
//server.setPort(*port);

// 方式2
server.setPort(port.value());
```

### Context 配置的引用

#### Context 的重定义

context 的重定义如下：

```cpp
template<typename T>
using $Context = IContextImport<T>;

template<typename T>
using $ContextMap = IContextImport<std::map<std::string, T>>;

using $ContextJson = $Context<IJson>;
using $ContextBool = $Context<bool>;
using $ContextChar = $Context<char>;
using $ContextUChar = $Context<uchar>;
using $ContextSChar = $Context<signed char>;
using $ContextShort = $Context<short>;
using $ContextUShort = $Context<ushort>;
using $ContextInt = $Context<int>;
using $ContextUInt = $Context<uint>;
using $ContextLong = $Context<long>;
using $ContextULong = $Context<ulong>;
using $ContextLongLong = $Context<long long>;
using $ContextULongLong = $Context<qulonglong>;
using $ContextFloat = $Context<float>;
using $ContextDouble = $Context<double>;
using $ContextLongDouble = $Context<long double>;

using $ContextMapStdString = $ContextMap<std::string>;
using $ContextQString = $Context<QString>;
using $ContextStdString = $Context<std::string>;
using $ContextQStringList = $Context<QStringList>;
```

这里没有再生了 Context 字符，而是在 `$` 和类型之间添加了一个 `Context` 字符串。因为 Context配置查询相对于 Profile 查询并不是一个常见的，面向开发者的操作。所以更短的配置查询留给了 profile 查询。

context 配置查询的操作和 profile 配置查询的操作一致，这里不再记录。

## 注册配置

### Context 配置注册

#### IContextTaskInterface 

Context 配置注册的基础是 IContextTaskInterface 类，它的声明如下：

```c++
template<typename T, bool enabled = true>
class IContextTaskInterface : public ITaskWareUnit<T, IConfigTaskCatagory, enabled>, public ISoloUnit<T>
{
public:
    IContextTaskInterface() = default;

public:
    virtual IJson config() = 0;
    virtual std::string path() const;

protected:
    virtual void $task() final;
};
```

用户继承该类，就可以注册自己的配置到 Context 配置中去。 

config() 函数返回的



### Profile 配置注册





## 注意事项



