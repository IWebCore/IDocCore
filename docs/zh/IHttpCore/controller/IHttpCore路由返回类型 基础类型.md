# IHttpCore 路由返回类型 基础类型

IHttpCore Controller 提供了无比丰富的函数返回类型。通过这些返回类型，用户可以给客户端返回任何他想要返回的内容。用户不必通过繁琐的步骤来一项一项的将内容写出来，而是通过我们一系列的返回类型可以节省大量的编码工作。

此外，用户也可以自定义返回类型，以此满足业务需要。



## Qt 的返回类型反射

在  Qt 中，如果一个类被标记为  `Q_GADGET`，那么这个类在编译的时候就会被 `MOC` 工具扫描，生成一系列的元信息，存放在 `moc_xxx.cpp` 文件中，我么可以通过该类的 静态 `staticMetaObject()` 函数来获取该类所扫描的信息。  

如果一个反射类中的函数被标记为 `Q_INVOKABLE`， 那么这个函数的名称，返回类型，参数类型以及参数名称，调用方式都会被记录下来。这篇文档我们只关注元信息中的 返回值类型名称和返回值类型 Id。

当我们知道返回值类型的名称和返回值类型Id 的时候，我们就可以处理这些返回值，将他转换成我们想要的内容。在IHttpCore框架中，我们将返回的对象处理成为 http 响应。这个就是我们能够实现不同类型的路由返回的原因。



## 字符串类型

字符串返回类型返回的是一个字符串, 统一使用 utf-8编码，默认的返回状态是 `200 OK`,默认的返回的 Content-Type 是 `text/plain; charset=UTF-8`。如果希望返回一个不同的 Http Status， 或者 返回的类型修改掉，可以考虑 `IPlainTextResponse`。

### QString

QString 是最常用的返回类型，它也是 Qt 默认支持的类型。示例代码如下

```c++
$GetMapping(qstring)
QString qstring()
{
    return "QString"
}
```

### std::string

std::string是c++标准库中支持的类型，示例代码如下

```c++
$GetMapping(stdString)
std::string stdString()
{
    return "stdString";
}
```

注意这里必须使用 std::string 类型，不能通过`using namespace std；` 将 std 前缀省略掉，是不合法的。

```c++
using namespace std; // 引入 std 命名空间

GetMapping(stringFun)
string stringFun()
{
    return "string";
}
```

上述代码可以编译成功，但是在运行出去会报错，告诉开发者 `string` 类型无法解析。因此，在返回值的类型中， `std::string` 是合法的类型，而 `string` 是非法的类型

### IString

IString 类型是框架中定义的string 类型,目的是减少string类型的拷贝，提高软件运行效率，具体的可以参考 `core/IString文档`。他的用法和 QString， 以及 std::string 并没有区别。下面是他的使用方式：

```c++
$GetMapping(istring)
IString istring()
{
    return "IString";
}
```

### QByteArray

QByteArray 类型返回的Content-Type 类型是 `application/octet-stream`,意思是这个类型并不是 text 类型，而是一个字符流类型。所以这里如果需要明确的返回字符串，不能够使用 QByteArray。但是一些特殊的场景使用 QByteArray 是一个很好的选择，他的示例如下：

```c++
$GetMapping(qbytearray)
QByteArray qbytearray()
{
    return "IStringView";
}
```



## 数值类型

IHttpCore支持返回数值类型。返回的数值将会被转换成字符串发送给客户端。返回的状态是 `200 OK` 状态，返回的content-type 是 `text/plain`。

### 原生的数值类型

原生的数值类型包含 如下的类型

- short， ushort， unsigned short
- int， uint， unsigned int
- long， ulong， unsigned long
- long long， qlonglong， qulonglong， unsigned long long
- float， double

代码示例如下：

```c++
$GetMapping(uintVal)
uint uintVal(){
    return std::numeric_limits<uint>::max();
}

$GetMapping(unsignedlonglongVal)
unsigned long long unsignedlonglongVal(){
    return std::numeric_limits<unsigned long long>::max();
}
```

注意上面的类型中，如 ushort 和 unsigned short 是同一个类型。但是 unsigned short 是 c++ 标准中给出的类型名称，而 ushort 则是 `qglobal.h` 中重新定义的类型名称。所以在这里写了两种的类型。他们都可以被使用在返回类型中。其他的类型名称也是如此。

还有一点注意的是 short 在 c++标准中可以写出 `signed short`。但是在我们的返回值类型中不被支持。你不可以写出如下的代码：

```c++
$GetMapping(hello)
signed short hello();
```

这个可以考虑支持，也很容易支持。但是本人觉得没必要，不会有人故意写 `signed short` 这种类型的。所以这类的类型在IHttpCore 中非法，如果用户使用这种类型，程序在执行的初期会报错。



用户还需要注意的一点是各种类型的长度问题。比如 int 类型在不同的环境中长度不一致。从 16位到64位都有例证。用户在实际的使用过程中需要实际判断返回值的范围大小并 返回类型支持的大小。如果使用错误，则会造成数据的混乱，强制转换等问题。关于这个，可以参考下面的一种方式。

### std::int 类型

c标准支持 int16_t 这种类型，c++标准做了进一步的封装，使用std::int16_t 这种类型。他们表示这个数据总长度是 16位的。所有的IHttpCore 支持的数据类型如下：

- int16_t, std::int16_t, uint_16_t, std::uint16_t
- int32_t, std::int32_t, uint_32_t, std::uint32_t
- int64_t, std::int64_t, uint_64_t, std::uint64_t

用户可以使用这种精确的位大小的类型来返回一个数值，这样就可以避免返回类型强制转换等等一系列的问题。示例代码如下：

```c++
$GetMapping(stdUInt32_t)
std::uint32_t stdUInt32_t(){
    return std::numeric_limits<std::uint32_t>::max();
}

$GetMapping(stdUInt64_t)
std::uint64_t stdUInt64_t(){
    return std::numeric_limits<std::uint64_t>::max();
}
```

### char 相关的类型

上面的类型中，缺乏一类的类型，长度为8位的数据类型。他们可以是如下的名称

- char， signed char， schar， unsigned char， uchar， 
- int8_t , std::int8_t, uint8_t, std::uint8_t

这部分的类型目前没有作为返回值的类型，之后会支持成为返回值的类型。没有做的原因是因为作者拧巴了，添加这部分的类型很简单，但是作者就是没有添加上去。

注意在通常的概念上，char类型用于表示一个字符，所以如果类型是 `字符类型`，则是表示开发者希望返回的是单个字符。而其他的带符号的类型 和 int8_t 这样的类型则表示 `数值类型`。他返回的是该类型的数值。

用户想返回一个字符，直接转换成长度为一的字符串返回，如果想返回数值，使用 short 这些更大的类型进行返回。

## Http 响应状态

如果用户是简单的希望服务器端只是响应一个状态，不需要携带任何额外的信息，可以将返回类型设置为 IHttpStatus 或者直接 int 类型。

当然，这种需求并不常见。用户更好的选择是返回一个 `IStatusResponse` 类型

### IHttpStatus

IHttpStatus 的介绍参考 `IHttpCore status` 文档。他的用法如下：

```c++
$GetMapping(httpStatus)
IHttpStatus httpStatus()
{
    return IHttpStatus::ACCEPTED_202;
}
```

他的响应状态是 202，响应内容为空，没有响应内容。

## 复合结构

在C++中，复合类型是指由基本数据类型组合而成的类型。复合类型包括指针、引用、数组、结构体（struct）、联合体（union）和类（class）。这些类型允许程序员构建更复杂的数据结构，以适应各种编程需求。

在 IHttpCore 框架中，我们可以直接返回复合的结构类型，并在请求响应的过程中，将这些复合类型转换成json 类型数据返回给客户端。

### Bean

在 IHttpCore 中,我们引入了 Bean 的概念， Bean 是一个特定的结构体，这个结构体可以和 json 进行相互转换。关于 Bean 的更多信息，可以参考 `core/bean`的文档。 

在实际的应用过程中，Bean类型会进一步被封装成 数据库的 表（Table） 和视图（View）。这样用户可以直接通过数据库查询获得Bean 数据，返回给客户端。具体的内容，可以参考 `IRdbCore` 相关的文档。  



#### 定义一个Bean

我们定义的Bean 如下

> MyBean.h

```c++
#pragma once

#include "core/bean/IBeanInterface.h"

class MyBean : public IBeanInterface<MyBean>
{
    Q_GADGET
public:
    MyBean() = default;
    MyBean(int id, QString name){
        this->index = id;
        this->name = name;
    }

    $BeanField(int, index, 100)
    $BeanField(QString, name, "yuekeyuan")
};
```

上面定义的Bean 继承于 IBeanInterface， 包含两个字段， int 类型的`index` 字段，字段的默认值是100，以及 QString  类型的 `name` 字段， 字段的默认值是 `yuekeyuan`。

#### Bean类型

接下来写一个Bean类型的返回对象

```c++
$GetMapping(getBean)
MyBean getBean(){
    return {};
}
```

其中测试案例如下：

```c++
def test_bean():
    val = requests.get(serverAddress + "/ReturnTypeController/getBean")
    assert val.status_code == 200
    assert val.json() == {"index":100,"name":"yuekeyuan"}
    assert val.headers["Content-Type"]  == "application/json; charset=UTF-8"
    print(val.text)
    print(val.headers)
```

在上面我们直接返回 MyBean 类型的默认数据。测试案例通过。在上面的测试中，我们看见，他的返回类型是 `application/json; charset=UTF-8` 类型。 返回的状态是 `200 OK`, 具体的内容是`{"index":100,"name":"yuekeyuan"}`。

这样的返回值类型直接为 Bean类型可以避免开发者自己做类型转换，节省开发者的时间和工作量。



#### Bean 序列容器

在用户定义的Bean的基础之上，我们可以使用序列容器包裹Bean 类型，返回 bean 类型的序列容器。

在 IHttpCore 中，框架支持的序列容器类型有

- QList
- std::list
- QVector
- std::vector

|                    | ***\*Qt类型\**** | ***\*标准库类型\**** |
| ------------------ | ---------------- | -------------------- |
| ***\*链表\****     | QList<Bean>      | std::list<Bean>      |
| ***\*动态数组\**** | QVector<Bean>    | std::vector<Bean>    |

这四种容器类型。这是因为我们在Qt系统的基础上进行开发，支持了 Qt 的容器类型和 标准库的容器类型。他的用法如下：

```c++
$GetMapping(getBeanQList)
QList<MyBean> getBeanQList()
{
    return QList<MyBean>{
        MyBean{1, "hello"},
        MyBean{2, "world"}
    };
}

$GetMapping(getBeanStdList)
std::list<MyBean> getBeanStdList()
{
    return std::list<MyBean>{
        MyBean{1, "hello"},
        MyBean{2, "world"}
    };
}
```

上面列举了 QList 和 std::list 的用法，QVector 和std::vector的用法是一致的。这里不一一列举。

上面的请求返回状态为 `200 OK`， 返回类型为 `application/json; charset=UTF-8`， 返回的内容为：`[{"index":1,"name":"hello"},{"index":2,"name":"world"}]`。可以看见，这是一个json 数组，并且内容正确。

注意，这些别名必须如上述表格中书写的样式一致，如果不一致，编译代码不会出错，但在程序运行初期，由于Qt 反射的某些原因，这些类型并不能被识别，框架会向用户报错。



#### Bean 关联容器

IHttpCore目前支持 QMap 和 std::map 了两种类型的关联容器。这两种关联容器的目前的键类型可以是 `QString` 和 `std::string` 和 `IString`。所以一个Bean 类型可以特化成六种类型的关联容器。

|                    | ***\*QString\****       | ***\*std::string\****       | ***\*IString\****       |
| ------------------ | ----------------------- | --------------------------- | ----------------------- |
| ***\*QMap\****     | QMap<QString, Bean>     | QMap<std::string, Bean>     | QMap<IString, Bean>     |
| ***\*std::map\**** | std::map<QString, Bean> | std::map<std::string, Bean> | std::map<IString, Bean> |

下面我们举一些例子：

```c++
$GetMapping(getBeanQMapQstring)
QMap<QString, MyBean> getBeanQMapQstring()
{
    return QMap<QString, MyBean>{
        {"yue", MyBean{1, "hello"}},
        {"qichu", MyBean{2, "world"}}
    };
}

$GetMapping(getBeanStdStringStdMap)
std::map<std::string, MyBean> getBeanStdStringStdMap()
{
    return std::map<std::string, MyBean>{
        {"yue", MyBean{1, "hello"}},
        {"qichu", MyBean{2, "world"}}
    };
}
```

注意这里有一个点，就是这里的类型必须是一个完整的类型。类型不能够使用 `typedef` 或者 `using` 或者 `#define` 等各种方法给完整的类型一个别名。这些别名不能够被 IHttpCore 框架识别。  



### 常规复合类型

复合类型不仅对于用户自定义的Bean 类型有效，IHttpCore 同样支持一些常规类型的复合类型组合。

这些类型如下：

- bool 类型

> bool

- 字符串类型：

> QString， std::string,  IString

- 数值类型：

> short, ushort, int, uint, long, ulong, float, double等。

这些类型可以被序列容器或者关联容器组合成为复合结构，在路由映射的函数中作返回类型使用。

#### 序列容器

序列容器举例如下：

```c++
$GetMapping(intList)
QList<int> intList()
{
    return {1, 2, 4};
}

$GetMapping(intVector)
std::vector<int> intVector()
{
    return {1, 2, 5};
}

$GetMapping(stringList)
std::list<std::string> stringList()
{
    return {"hello", "world", "yuekeyuan"};
}
```

注意一点，QStringList 也可以被IHttpCore 映射函数返回。



#### 关联容器

和Bean 的关联容器类似，常规类型也支持关联容器。举例如下：

```c++
$GetMapping(stdMapstdStringInt)
std::map<std::string, int> stdMapstdStringInt(){
    return std::map<std::string, int>{
        {"hello", 1},
        {"world", 2},
        {"yuekeyuan", 3}
    };
}

$GetMapping(qMapstdStringInt)
QMap<std::string, int> qMapstdStringInt(){
    return QMap<std::string, int>{
        {"hello", 1},
        {"world", 2},
        {"yuekeyuan", 3}
    };
}

$GetMapping(stdMapQStringInt)
std::map<QString, int> stdMapQStringInt(){
    return std::map<QString, int>{
        {"hello", 1},
        {"world", 2},
        {"yuekeyuan", 3}
    };
}

$GetMapping(qMapQStringInt)
QMap<QString, int> qMapQStringInt(){
    return QMap<QString, int>{
        {"hello", 1},
        {"world", 2},
        {"yuekeyuan", 3}
    };
}
```

注意一点，我们所有的类型名称不能简写，不能替代。



## IJson

IHttpCore 支持 IJson 作为返回值，IJson 是 nolhmann/json 库的别称。

```
using IJson = nolhmann::json;
```

我们为 nolhmann/json 写一个名称代替一是为了和我们的项目代码一致，而是为了简化操作，减少字符的输入。注意一点，用户不可以使用 nolhmann/json, 或者 json 作为返回值名称，必须使用 IJson 作为返回值名称，这些名称在运行初期会出现异常报错。

 关于IJson 的内容，用户可以查看  [nlohmann/json: JSON for Modern C++](https://github.com/nlohmann/json) 查看。



下面我们举一个例子：

```c++
$GetMapping(ijson)
IJson ijson(){
    return IJson({"hello", "world"});
}
```

在这个例子当中，我们作了一个IJson类型的简单返回。在这里用户可以将任何的json 数据直接返回给客户端。

## 时间类型

IHttpCore 支持将 Qt 的时间类型返回给用户。在返回的时候转换成相应的字符串发送给客户端。

### QDate

QDate 类型作为返回类型如下：

```c++
$GetMapping(qDate)
QDate qDate(){
    return QDate(2022,10,12);
}
```

在请求上述的路径之后，客户端会得到 `2022-10-12` 这样的返回值。（这一天是 起初出生的日子）。

返回类型的默认格式是 `yyyy-MM-dd`。如果用户想要额外的数据格式，比如 `2022/10/12` 这种格式，他可以在项目中自定义配置，改变 `/http/QDateFormat` 这个配置路径的值，改为 `yyyy/MM/dd`。 关于配置选项，请查看 `core/config` 相关的文档。

如果返回的QDate 这个类型不是一个正常的数据，则会返回 500 Internal Error 状态。



### QTime

QTime 作为返回路径示例如下：

```c++
$GetMapping(qTime)
QTime qTime(){
    return QTime(12,12,12);
}
```

QTime 的默认格式是 `HH:mm:ss` 所以上述路径返回的字符串为 `12:12:12`。如果用户需要自定义返回的格式类型，修改 `/http/QTime` 的路径配置即可。

如果返回的QTime 数值不正确，则会返回 500 的状态。



### QDateTime

QDateTime 示例如下：

```c++
$GetMapping(qDateTime)
QDateTime qDateTime(){
    return QDateTime(qDate(), qTime());
}
```

QDateTime 默认的格式是：`yyyy-MM-ddTHH:mm:ss`，用户可以修修改 `/http/QDateTimeFormat` 路径下的配置来转换类型。

如果返回的数值不正确，则会返回500 状态给客户端。