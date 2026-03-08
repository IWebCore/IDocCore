# IHttpCore 路由

## 关于路由

HTTP路由是Web开发中的一个关键概念，它负责将客户端的HTTP请求映射到服务器上相应的处理程序或资源。在构建Web应用时，开发者通常会设计一套路由规则，以便根据不同的URL路径和HTTP方法（如GET、POST、PUT、DELETE等）来执行不同的操作。例如，当用户访问一个博客网站的主页时，服务器可能会根据路由规则将请求转发到一个特定的函数或控制器，该函数或控制器负责渲染主页内容并返回给客户端。

在现代Web框架中，路由通常通过声明式的方式进行配置，允许开发者以清晰、简洁的语法定义路由规则。例如，在Express.js（一个流行的Node.js Web框架）中，路由可以这样定义：

```javascript
app.get('/articles/:id', function(req, res) {
});
```

在 python flask 中这样定义：

```python
@app.route('/')
def hello_world():
    return 'Hello, World!'
```

通过这些方式，开发者可以灵活地控制Web应用的导航结构，同时确保应用能够响应各种用户请求。良好的HTTP路由设计不仅有助于提高应用的可维护性，还能提升用户体验，因为它们允许开发者快速定位和处理特定的请求。



### IHttpCore 中的路由

在 IHttpCore 中，路由的定义 和 flask， SpringMvc类似，可以让用户通过注解的方式进行定义。

下面给一个简单的例子



> MyController

```c++
class MyController : public IControllerInterface<MyController>
{
    Q_GADGET
public:
    $GetMapping(index, /)
    QString index();

    $PostMapping(abc)
    IFileResponse abc();

    $DeleteMapping(deleteFile, /del/<id>)
    IStatusResponse deleteFile(int id);
};
```

上面给了三个路由映射的案例，第一个是 映射到 `GET /`, 第二个映射到 `POST /abc` ， 第三个映射到 `DELETE /del/<id>` ，其中 <id> 是一个通配符，并将拦截的内容传入到函数当中去。下面我们详细解释IHttpCore中的路由规则。



## 请求方法

在上面的案例中，我们看到了三种不同的请求方法。IHttpCore总计支持 `GET`, `POST`, `PUT`, `DELETE`,`PATCH`, `HEAD`, `OPTIONS` 七种请求方法。支持宏注解的方法有5 种，宏注解分别为：

- $GetMapping
- $PutMapping
- $PostMapping
- $DeleteMapping
- $PatchMapping

`HEAD` 方法是返回 `GET` 方法的 头部信息，不需要宏注解定义他的返回函数。`OPTIONS` 方法是查询是对一个特定的url 返回有哪些方法被支持了，同样不需要宏注解定义他的处理函数。

上述的Mapping 的命名规则统一，是 `$` + `METHOD` + `Mapping` 的样式。 他们的使用方法类似，下面以 $GetMapping 为例进行讲解。



### $XxxMapping

`$GetMapping`的宏注解实现如下：

```c++
#define $GetMapping_1(funName)  \
    $GetMappingDeclare(funName) \
    Q_INVOKABLE

#define $GetMapping_2(funName, url1)  \
    $GetMappingDeclare(funName, url1) \
    Q_INVOKABLE

#define $GetMapping_3(funName, url1, url2)  \
    $GetMappingDeclare(funName, url1, url2) \
    Q_INVOKABLE

#define $GetMapping_4(funName, url1, url2, url3)  \
    $GetMappingDeclare(funName, url1, url2, url3) \
    Q_INVOKABLE

#define $GetMapping_5(funName, url1, url2, url3, url4)  \
    $GetMappingDeclare(funName, url1, url2, url3, url4) \
    Q_INVOKABLE

#define $GetMapping_6(funName, url1, url2, url3, url4, url5)  \
    $GetMappingDeclare(funName, url1, url2, url3, url4, url5) \
    Q_INVOKABLE

#define $GetMapping_7(funName, url1, url2, url3, url4, url5, url6)  \
    $GetMappingDeclare(funName, url1, url2, url3, url4, url5, url6) \
    Q_INVOKABLE

#define $GetMapping_8(funName, url1, url2, url3, url4, url5, url6, url7)  \
    $GetMappingDeclare(funName, url1, url2, url3, url4, url5, url6, url7) \
    Q_INVOKABLE

#define $GetMapping_9(funName, url1, url2, url3, url4, url5, url6, url7, url8)  \
    $GetMappingDeclare(funName, url1, url2, url3, url4, url5, url6, url7, url8) \
    Q_INVOKABLE

#define $GetMapping_(N) $GetMapping_##N
#define $GetMapping_EVAL(N) $GetMapping_(N)
#define $GetMapping(...) PP_EXPAND( $GetMapping_EVAL(PP_EXPAND( PP_NARG(__VA_ARGS__) ))(__VA_ARGS__) )
```

在上面的代码中，可以看见，GetMapping 的参数可以从 1个参数到9个参数。 

- 第一个参数一定是他对应的函数名称。 

- 当只有一个参数的时候，函数名称也是我们要映射的路由路径。 

- - 这个比如上面 MyController.h 中，第8行， abc  既是要映射的函数名称，也是要映射的函数路径。

- 当参数多于1个的时候，除了第一个参数之外的参数都是要映射的路径。也就是说我们的一个 $GetMapping 可以有最多8个路径，被映射到这个函数上面。

- - 在绝大多数的情况下，其实只需要一个路径即可。这里可以多路径映射是给一些特殊需要的程序所留的接口。



另外我们看见 `$GetMapping` 宏注解的最后跟着一个 `Q_INVOKABLE` 的宏。`Q_INVOKABLE` 是用于修饰函数的，被该宏修饰的函数可以在 Qt Moc 的时候被记录，在运行期可以获得他的名字，参数，返回值等一系列的信息。这个也是为什么`GetMapping` 后面一定要跟上 函数的原因。如果没有跟着函数，程序在运行的时候就会报错。

那有没有方法绕过这个限制呢，有的，可以往下看:

### $XxxMappingDeclare

```c++
#define $GetMappingDeclare_1(funName)  \
    Q_CLASSINFO( PP_CONTROLLER_PROP(funName, GET, 1), #funName)

#define $GetMappingDeclare_2(funName, url1)  \
    Q_CLASSINFO( PP_CONTROLLER_PROP(funName, GET, 1), #url1)

#define $GetMappingDeclare_3(funName, url1, url2)  \
    $GetMappingDeclare(funName, url1) \
    Q_CLASSINFO( PP_CONTROLLER_PROP(funName, GET, 2), #url2)

#define $GetMappingDeclare_4(funName, url1, url2, url3)  \
    $GetMappingDeclare(funName, url1, url2) \
    Q_CLASSINFO( PP_CONTROLLER_PROP(funName, GET, 3), #url3)

#define $GetMappingDeclare_5(funName, url1, url2, url3, url4)  \
    $GetMappingDeclare(funName, url1, url2, url3) \
    Q_CLASSINFO( PP_CONTROLLER_PROP(funName, GET, 4), #url4)

#define $GetMappingDeclare_6(funName, url1, url2, url3, url4, url5)  \
    $GetMappingDeclare(funName, url1, url2, url3, url4) \
    Q_CLASSINFO( PP_CONTROLLER_PROP(funName, GET, 5), #url5)

#define $GetMappingDeclare_7(funName, url1, url2, url3, url4, url5, url6)  \
    $GetMappingDeclare(funName, url1, url2, url3, url4, url5) \
    Q_CLASSINFO( PP_CONTROLLER_PROP(funName, GET, 6), #url6)

#define $GetMappingDeclare_8(funName, url1, url2, url3, url4, url5, url6, url7)  \
    $GetMappingDeclare(funName, url1, url2, url3, url4, url5, url6) \
    Q_CLASSINFO( PP_CONTROLLER_PROP(funName, GET, 7), #url7)

#define $GetMappingDeclare_9(funName, url1, url2, url3, url4, url5, url6, url7, url8)  \
    $GetMappingDeclare(funName, url1, url2, url3, url4, url5, url6, url7) \
    Q_CLASSINFO( PP_CONTROLLER_PROP(funName, GET, 8), #url8)

#define $GetMappingDeclare_(N) $GetMappingDeclare_##N
#define $GetMappingDeclare_EVAL(N) $GetMappingDeclare_(N)
#define $GetMappingDeclare(...) PP_EXPAND( $GetMappingDeclare_EVAL(PP_EXPAND( PP_NARG(__VA_ARGS__) ))(__VA_ARGS__) )
```

我们实际对路由以及路由函数的信息的绑定是在 `$GetMappingDeclare` 中完成的。上述中他会将 functionName 和url 以 键-值 映射的方式写入类的元信息（meta info）中。这样我们在后续的Action 注册生成的过程中，就可以知道哪些路由对应哪些函数。

注意这里 `$GetMappingDeclare` 与 `$GetMapping` 的区别除了 `$GetMapping` 更短更容易书写之外，`$GetMappingDeclare` 本身不带 `Q_INVOKABLE` 这个宏后缀。这样，我们就可以将路由和函数分离开来。

如下所示

```c++
$GetMappingDeclare(fun, /abc)
$PostMappingDeclare(fun, /abc)


$GetMappingDeclare(fun2, /get_fun2)
$GetMapping(fun2, /get_fun2_again)
QString fun2();

Q_INVOKABLE QString fun();
```

上面有两组映射，第一组中 1-2行是我们使用`MappingDeclare` 声明一个 `Get` 和一个 `POST` 方法。他对应的函数定义在 第9行。注意第九行的函数前面有 `Q_INVOKABLE` 宏限定。这限定会将该函数入到类的元信息当中。

第5-7行是第二个路由映射。该路由映射的宏注解第一个是 `GetMappingDeclare`,第二个是 `$GetMapping`。函数的元信息会通过第二个 `$GetMapping` 后面所带的 `Q_INVOKABLE` 进行反射。

在通常的使用当中，在定义了一个路由映射关系的前提下，如果想要增加一个相同请求方法的路由，可以直接在当前的 Mapping的参数后面继续写入一个路由即可， 不需要定义多个宏注解。如果是不同的方法的一个路由，这个时候就需要 `MappingDeclare` 进行声明新的路由规则。



## 路径规则

IHttpCore 框架中的路径规则通常是指在控制器（Controller）中定义的URL映射规则。这些规则用于将HTTP请求映射到相应的控制器（Controller）方法上。IHttpCore使用`$AsController`宏注解来定义控制器的公共路径规则，它可以用在类级别上。 使用 `$XxxMapping` 如 `$GetMapping` 来定义具体函数的路径规则，他作用在具体的函数上面。



### 路由路径和路由片段

在IHttpCore 将全局的路基和 针对于具体方法的路基拼接在一起，成为一个处理函数的路径，这个是一个完整的路由路径。路由路径由 `/` 分隔符和路由片段组成，路由片段之间有且只有一个 `/` 分隔符。在 IHttpCore 中，路由片段可以是普通的url 路由片段，也可以是 捕获路由片段， 捕获路由片段是以 `<` 开头，以 `>` 结尾的片段。下面做一个详细的介绍。



### 普通路由片段

普通的路径片段是只不具有捕获功能的，合法的，可以被服务器解析的路径片段。在 rfc 文档中有具体的相关规定。

> 在 ***\**\*RFC 9110\*\**\*** 中，路径部分遵循 ***\**\*RFC 3986\*\**\*** 的字符集定义，因此路径段中的字符集应包括：
> ***\*字母\****：`a-z`, `A-Z`
> ***\*数字\****：`0-9`
> ***\*特殊字符\****：
> `-`、`_`、`.`、`~` 等（这些是 URI 中常见的合法字符）
> 分隔符：`!`、`$`、`&`、`'`、`(`、`)`、`*`、`+`、`,`、`;`、`=` 等
> 编码字符（如 `%20` 替代空格）
> 路径段不能包含斜杠 `/`，因为 `/` 用作路径段之间的分隔符。如果路径段中需要使用斜杠，必须使用 URL 编码（`%2F`）来代替。

其次，中文等内容也可以作为路由片段的一部分。中文字符会在服务器发送请求的时候通过 urlencode 进行编码，成为普通的路由片段。在服务器接收到请求后会 urldecode 进行解码，变回为中文字符。不过在开发的过程中，不建议使用中文字符。

以下列举一些合法的路径片段:

1. 字母和数字

> example, abc123,  HelloWorld,  file2025

1. 特殊字符（常见合法字符）

-（连字符）

_（下划线）

.（点号）

~（波浪号）

@（at符号）

+（加号）

,（逗号） ;（分号）  =（等号）

例如：

> product-name  user_profile file.name folder~1

1. 中文字符（无需编码）

现代浏览器和服务器支持中文作为路径片段的一部分：

> 产品  手机   文件夹

例如：

https://example.com/产品

https://example.com/手机/价格

1. 数字和符号组合

> product-123 , data_2025 , name~version

1. 带有编码字符的路径片段

有些特殊字符（如空格、#、?、& 等）不能直接出现在路径段中，必须进行 URL 编码。例如：

> 空格：%20



### <> 路径

这个路径是一个通配符，用于匹配路径中的任意一个片段。注意这里是只能且必须匹配一个路径片段，如果路径片段为空，或者路径超过一个路径片段，则无法匹配。



- ***\*示例\****：`/products/<>`

- - 匹配：`/products/123`, `/products/abc`
  - 不匹配：`/products/123/details`, `/products`

- ***\*用法示例\****：

```c++
$GetMapping(fun, /products/<>)
QString fun();

GetMapping(hello, /products/<>/hello)
QString hello();
```

注意这里的通配符只会去匹配路径，并不会捕获路径。所以如果用户只是想在这里匹配一个路径，并且不关心这个路径的内容是什么，可以直接使用 `<>` 通配符。如果用户想要对路径片段进行捕获，或则对路径的格式进行限定，则需要下面的 路由片段匹配格式。



### <name>

`<name>` 和上面的 `<>` 通配符的类似，他的作用是通配一个路径，不管这个路径是什么内容。有一点不同的是，`<name>` 不仅会对 url 路径片段进行通配，他也会捕获自己的路径内容，捕获的内容可以放置在 函数参数当中，也可以通过 `IRequest` 类进行查询使用。

下面举一个例子

```c++
$GetMapping(hi, hi/<your>/<name>)
QString hi(QString $Path(your), QString $Path(name)) {
    return your + name;
}
```

在上面的例子中，我们拦截了 第二个路径参数和第三个路径参数，并将他们拼接在一起输出。 注意函数参数有 `$Path` 限定，这个表示`your` 和 `name` 这两个参数必须从捕获的路径参数中查找，具体关于请求参数限定的内容，可以参考 `IHttpCore 函数参数` 的相关内容。

上面的请求中，请求路径是  `/hi/yue/keyuan`，返回内容是 `yuekeyuan`。实现了完美的拦截。



### <name | restrict> 

实际的应用过程中，用户不仅希望对参数进行捕获，更希望参数有合法性。比如我们的参数必须是一个数字，参数必须符合一个正则规则，或者是用户定义的其他规则。 `<name|restrict>` 这个路由片段的目的是对参数进行一个人为的限定。让参数符合一定的要求，不符合的参数不能通过路由到该处理函数。



在这个路由规则中，`name` 表示我们捕获的参数名称。如果用户仅仅希望是参数限定，可以省略这个 `name` 的内容，这样我们的路径片段就会变成 `<|restrict>`。这个路径片段只对url 进行判断，不对片段进行捕获。



此外，我们还可以省略 restrict， 那这样的通配符会成为  `<name|>` 或则 `<|>`, 他会匹配任何的url 片段。



在 IHttpCore 中，我们预定义了一系列的 restrict。 他们分别如下：

- 数值类型

> short ,ushort, int, uint, long ,ulong, longlong, ulonglong, float, double

这些类型是数值类型，如果查询的参数是数值，并且他的范围在选定的类型范围之内，则匹配成功，否则，匹配失败。



- 时间类型

> date, QDate, time, QTime, datetime， QDateTime

这里的类型是时间类型，输入的内容必须能够转换成 Qt 支持的时间格式，比如 date/QDate， 如果输入内容可以转换成这个类型，则匹配成功。



- 字符串类型

> string, QString

这两个东西是凑数的，因为所有的内容这俩都能匹配，写在这里的原因是想让程序完整，自洽。



- 特殊类型

> uuid, base64

uuid类型是 满足 QUUid 生成格式类型。 base64 是指通过 base64转码之后的类型。



下面我们举例说明以上的内容

```c++
$GetMapping(datetimeVal, /datetimeVal/<val|datetime>)
QString datetimeVal(QDateTime $Path(val)){
    return val.toString(Qt::DateFormat::ISODate);
}

$GetMapping(doubleVal, /doubleVal/<val|double>)
QString doubleVal(double $Path(val)){
    return QString::number(val);
}

$GetMapping(uuidVal, /uuidVal/<val|uuid>)
QString uuidVal(QString $Path(val)){
    eturn val;
}
```

另外，用户可以自定义限制，来满足开发需求。具体内容可以查看下面 `自定义路径限制` 的相关内容。



### <name || regexp> 

路径片段也可以使用正则式进行匹配。如果有一个路径需要特殊的匹配规则，而这个规则又只使用一次的话，这种需求并不值得写一个参数约束。用正则式是最简单的一种方式。

注意正则式的约束是在`name` 和 `regexp` 中间有两道竖杠 `||`，这个是正则式约束和参数具名约束的最大区别。

下面举一个例子

```c++
$GetMapping(hello, hello/<path||(\\w+)>)
QString hello(QString $Path(path)){
    return path;
}

GetMapping(world, world/<path||abc.*>
QString world(QString $Path(path)){
    return path;
}
```

第一个路由请求是捕获任意的字符，第二个路由是捕获以 `abc` 开头的名字。

在正则式路由片段中，name 可以省略写成 `<||regexp>`.这个表示该路由片段只做正则式匹配验证，不做参数的捕获。

用户也可以省略 regexp，写成 `<name||>`, 这样是匹配所有的路径，捕获成为 name 变量。用户也可以省略全部内容，路由片段写成 `<||>`, 这个功能和 `<>` 一致。   

### “/” 根目录

如果用户想将一个路径匹配到根目录，则需要将 mapping 的参数写成 `/`，如下所示

```
$GetMapping(index, /)
QString index();
```

这样 index() 函数就会和 我们url 请求的根目录绑定。如果在Controller 中有 `$AsController` 定义的前缀，则 index 会映射到前缀所在的url 上面。



### 函数名作为路径

如果映射关系中中只有函数名称，而没有路径，则该函数的名称就是映射路径。

```
$GetMapping(index)
QString index();
```

在这个情况下，index函数的映射路径是 `/index`。这样省略路径可以减少用户的输入和心智负担。



### 注意事项

- 在路径的书写中，路径片段不可以为 `..` 和 `.`。

- - `..` 表示 上级目录，`.` 表示本目录，这两个片段都不可以作为路径片段。

- 最前面的 `/` 可以省略不写，不影响路径的解析。

- Mapping 的函数名词一定要和函数能够对应起来，如果对应不起来，在运行初期会报异常。

- 函数目前禁止使用 重载函数。也就是说一个函数名只能在 Controller 中出现一次。如果有重载函数，程序运气初期将会报错。

- 对于多级目录的通配符，目前框架并不支持。这个功能将在后续进行支持。

## 自定义路径限定



在上面的路由片段限制中，除了框架提供的限定方式之外，用户也可以通过继承 `IHttpPathValidatorInterface` 这个类来添加自定义的路径限制规则。 

### IHttpPathValidatorInterface

该类的声明可以简化如下：

```c++
template<typename T, bool enabled=true>
class IHttpPathValidatorInterface : public ITaskWareUnit<T, IHttpTaskCatagory, enabled>, public ISoloUnit<T>
{
public:
    using Validator = std::function<bool(IStringView)>;

public:
    virtual void $task() final;
    virtual double $order() const final;

public:
    virtual QString marker() const  = 0;
    virtual Validator validator() const  = 0;
};
```

这是一个 `CRTP` 模版基类。用户可以继承该基类来定义自己的限定条件。 模版基类的第一个模版参数是子类的名称，这个是 CRTP 的基础。 第二个参数是 bool 类型参数，默认为 `true`，表示启用该类型限定。如果参数值为 false，则这个类型限定就不会被启用，他的任务就不会被执行，用户也无法使用该类型。



在这个类中，定义有两个纯虚函数，这两个函数需要被子类重载。`maker()` 函数的返回值是表示路由片段的限定名称。`validator()` 函数返回的是一个函子，他是一个可调用对象 类型为 `std::function<bool(IStringView)>`。用户需要返回一个可调用对象，这个对象可以是一个静态函数，可以是`lambda` 表达式，也可以是一个 封装后的成员函数。



### 举例

下面举一个例子，我们定义一个 gender 的路由限定。这个限定只允许用户输入两种性别 `male` 和 `female`，如果输入的不是这两种性别，则路由无法匹配。实现代码如下：



> GenderValidator.h

```c++
#pragma once

#include "http/path/IHttpPathValidatorInterface.h"

class GenderValidator : public IHttpPathValidatorInterface<GenderValidator>
{
public:
    GenderValidator() = default;

public:
    virtual QString marker() const final;
    virtual Validator validator() const final;
};
```



> GenderValidator.cpp

```c++
#include "GenderValidator.h"

QString GenderValidator::marker() const
{
    return "gender";
}

GenderValidator::Validator GenderValidator::validator() const
{
    return [](IStringView value) -> bool{
        return value == "male" || value == "female";
    };
}
```

这样gender 类型就注册好了，写一组路由映射，验证一下

```c++
    $GetMapping(gender, /gender/<gender|gender>)
    QString gender(QString $Path(gender))
    {
        return gender;
    }
```

上面的代码编译通过，单元测试也通过，能够正常拦截非 male 和 female 数据的内容。