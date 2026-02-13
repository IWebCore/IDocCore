# Packages

## 引言

在 ICore 程序中，在代码文件中，随处可以看见 如下的代码：

```cpp
$PackageWebCoreBegin

$PackageWebCoreEnd
```

这两行代码是宏定义，用于设定命名空间，而命名空间就是 IWebCore，可以查找到他的定义是如下：

```cpp
#define $PackageWebCoreBegin  $IPackageBegin(IWebCore)

#define $PackageWebCoreEnd    $IPackageEnd(IWebCore)
```

如果宏扩展下来，代码就会变成如下形式：

```cpp
inline namespace IWebCore {
    
}
```



## IPackageBegin / IPackageEnd

我们可以查看以下 IPackageBegin 的定义：

```c++
#define $IPackageBegin_1(name1) \
inline namespace name1 {

#define $IPackageBegin_2(name1, name2) \
inline namespace name1 {   \
    inline namespace name2 {

#define $IPackageBegin_3(name1, name2, name3) \
inline namespace name1 {   \
    inline namespace name2 {   \
        inline namespace name3

#define $IPackageBegin_4(name1, name2, name3, name4) \
inline namespace name1 {   \
    inline namespace name2 {   \
        inline namespace name3 \
            inline namespace name4


// .... util $IPackageBegin_9

#define $IPackageBegin_(N) $IPackageBegin_##N
#define $IPackageBegin_EVAL(N) $IPackageBegin_(N)
#define $IPackageBegin(...) PP_EXPAND( $IPackageBegin_EVAL(PP_EXPAND( PP_NARG(__VA_ARGS__) ))(__VA_ARGS__) )

```

在上面的定义中，我们定义了一个宏, 大致如下：

```cpp
IPackageBegin(arg1, arg2, ....)
```

这个宏最多可以传递9个嵌套的命名空间的名称, 每一个参数都会在原来的命名空间的基础上再嵌套一层命名空间。

IPackageEnd 也是如此，

注意这里我们的开发环境是基于c++17, 这里不支持折叠命名空间。在 c++20的条件下，上面带代码会更加简单。

### inline namespace

这里为什么有一个 inline? 是因为我想让这个namespace里面的东西对开发者是使用是透明的，开发者不需要使用 namespace IWebCore 就可以引用到该对象。

因为使用了inline 的方式，那么如果有另外一个名称相同的类或对象名声，则还是会冲突，这个时候，开发者可以在对象名称的前面添加命名空间限定来解决命名冲突的问题。

### 为什么要用命名空间

既然对开发者透明，那么直接不要这个namepace IWebCore 可以么？ 不建议的，因为在 IWebCore 中，库是源代码库，里面会有很多很多的类，如果类名相同的情况下，没有 namespace 包裹，则会出现 类编译冲突的问题。关于这个问题，其中一个解决办法是将库编译成二进制，而选择性的导出其中一部分名称。但是这里还是建议每一个库都带上自己的命名空间。

### 在自定义的包中如何使用 IPackage 类型

用户自定义包时，可以通过定义自己的 宏，来定义包的命名空间。假设用户新建一个包 Abc， 那么用户可以定义 宏如下：

```c++
#define $PackageAbcBegin  $IPackageBegin(Abc)

#define $PackageAbcEnd    $IPackageEnd(Abc)
```

用户在每一需要包裹的 namespace 前面可以写下如下代码

```c++
$PackageAbcBegin

class Abc
{
	// ... 
}

$PacakgeAbcEnd
```

建议用户使用如上的方式定义包的命名空间，原因如下：

- 统一风格， 在所有的包都这样写的时候，IWebCore 风格统一，用户心智负担小。
- 避免出错， 通过宏定义的方式，如果用户拼写错误，编译器会报错。这样防止用户写错代码。