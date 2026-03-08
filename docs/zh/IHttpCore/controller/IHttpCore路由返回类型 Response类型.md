#  IHttpCore路由返回类型 Response类型

在IHttpCore中，我们定义了一系列的Response 类型作为 函数的返回值类型，用户可以使用这些类型来返回数据。

## Response 类型概述

> 这里还有返回 尾缀的概念， 和 $json: 这个东西。

在我们上述简单类型的返回过程中，我们可以返回一系列的类型，上面的类型有一系列的不足之处，比如他不能设置 返回状态，不能设置一系列Header 状态，不能添加cookie 类型，如果我们在数据处理的过程中出现异常了，也没有办法向客户端返回一个异常指示。所以我们引入了 Response 类型的概念。

Response 类型的命名是以 `I` 开头， 以 `Response` 结尾。比如 IFileResponse， IHtmlResponse等等。用户也可以定义自己的返回类型。IHttpCore 也提供一个插件 INodyResponse， 这个插件支持用户返回一个Html模版名称 和一组用于渲染的数据，模版和渲染数据结合一起，生成一个完整的 html内容再返回给用户。

同时我们的基础的返回类型在实际的解析过程中，也会被包装成相应的Response 类型。比如当返回类型是 IJson 类型的时候，IHttpCore 在对返回类型的解析时，会将 IJson 的值包装成 IJsonResponse 类型。我们的 IHttpStatus 类型会被包装成 IStatusResponse 类型。QString 一般会被包装成 IPlainTextRespponse。之所以是`一般`，是因为字符串类型会有一些特殊处理的内容,在这里我们会列举出来。

有一点就是我们的 Response 类型前缀是 `I`,没有带上 我们的库限制 `Http`,`IHtmlResponse` 不是 `IHttpHtmlResponse`。这样做固然打破的我们的命名限制，但好处就是开发者在写命名的时候可以缩短代码。而且http 模块是在之后使用最频繁的模块，这便值得我们为此这样命名。如果之后有其他的模块需要 response, 则此时我们的Response 就需要添加上前缀了。比如之后有一个模块是 Abc， 那么模块的Response 就应该是 `IAbcFileResponse`, 而不是 IFileResponse。



### IHttpResponseInterface和 IHttpResponseWare

IHttpResponseInterface 是所有的 Response 类型的CRTP基类，如果开发者想写自己的 Response，则可以继承该基类。关于扩展Repsonse的内容，可以参考下面的内容。

IHttpResponseWare 是 IHttpResponseInterface 的一个父类。IResponseWare是具体存储返回内容的基类。在IHttpResponseWare 中，可以设置 mime，status， header, session, content 等一系列返回给客户端的内容。



### 尾缀类型

在IHttpCore 中，针对Response 类型，我们定义了很多的字符串字面量。比如：

```
IFileResponse operator"" _file(const char* str, size_t size);
IHtmlResponse operator"" _html(const char* str, size_t size);
```

这些字面量可以构造对应的 Response 类型。这样在返回的过程中，用户可以直接使用字面量后缀来构造对象。比如：

```
$GetMapping(fileResponse)
IFileResponse fileResponse(){
    return ":/resource/defaultWebConfig.json"_file;
}
```



### 前缀类型

函数返回一个 String 类型的时候，IHttpCore 定义了一系列的前缀，这些前缀可以将String的数据转换成其他的类型，如文件类型，html 类型等等一系列的类型。比如:

```
$GetMapping(fileResponse)
QString fileResponse()
{
    return "$file::/resource/defaultWebConfig.json";
}
```

这个函数返回了 QString 的类型的数据`"$file::/resource/defaultWebConfig.json"`。这个数据在实际解析的时候会拆分成两个部分，`$file:` 和  `:/resource/defaultWebConfig.json`。前面的 `$file:` 一个数据类型前缀，这个前缀会在解析的时候判断和匹配。所以这条返回的数据会被解析成一个 IFileResponse 类型，并使用 `:/resource/defaultWebConfig.json` 来构造这个IFileResponse。这个就是前缀类型。



再举一个例子：

```
$GetMapping(htmlResponse)
IString htmlResponse()
{
    return "$html:<h1>hello world</h>";
}
```

这个请求在实际响应的过程中，会构建一个 IHtmlResponse， 内容是 `<h1>hello world</h>`，返回给客户端的Content-Type 是 `text/html; charset=UTF-8`,而不是 `text/plain`。



### 返回 Invalid



### 返回 Status



下面说明我们在框架中定义的各类的Response。

## IFileResponse

IFileResponse 支持用户将一个文件返回给客户端。

```c++
$GetMapping(fileResponse)
IFileResponse fileResponse(){
    return ":/resource/defaultWebConfig.json";
}
```

IFileResponse 会在解析的过程中尝试查找一个对应的mime类型，如果找到了，就使用查找的mime，如果没有找到，则使用`application/octet-stream`， 表示这个是一个二进制流文件。关于mime 类型，请参考 `http/mime` 相关的内容。

用户可以返回Qt 的资源文件，也可以Qt 的resource 资源文件，这些文件可以和 代码一起编译到可运行的程序里面， 这些文是以 `:/` 开头的文件，如上面的代码所示。用户也可以给定一个相对或者绝对的地址，这个地址指向一个文件。



IFileResponse 的类型定义如下：

```c++
class IFileResponse : public IResponseInterface<IFileResponse>
{
    $AsResponse(IFileResponse)
public:
    using IResponseInterface::IResponseInterface;
//    using IResponseInterface::operator [];

public:
    IFileResponse() = default;
    IFileResponse(const char* data);
    IFileResponse(const QString& path);
    IFileResponse(IString&& path);
    IFileResponse(const IString& path);
    IFileResponse(const std::string& path);

public:
    void enableContentDisposition();

public:
    virtual std::string prefixMatcher() final;

private:
    IFileResponseContent* m_fileResponseContent{};
};

IFileResponse operator"" _file(const char* str, size_t size);
```

我们的构造函数没有添加 explict， 所以用户可以直接返回一个字符串类型，IFileResponse 会自动构造,并解析相关内容。



### contentDisposition

注意类中有一个 `enableContentDisposition` 函数。这个函数可以在返回的时候设置进去。如果调用该函数，发送给客户端的头中将添加 `Content-Disposition`内容的 Header。该Header 的作用是在客户端如浏览器请求的时候，会直接将文件保存下来，而不会在客户端进行显示。



```c++
$GetMapping(fileResponse)
IFileResponse fileResponse(){
    IFileResponse data(":/resource/defaultWebConfig.json"_file);
    data.enableContentDisposition();
    return data;
}
```



### 文件失效问题

如果用户提供的地址当中并没有文件，则会返回 `IHttpNotFoundInvalid` 也就是 500 的状态。这里之所以不返回`404` 状态，是因为在请求过程中匹配到了相应的URL， 但是处理函数内部指向的文件失效，所以这里是 服务器响应的问题，而不易url 查找的问题。



### 前缀

IFileResponse 的前缀是 `$file:`, 也就是 `prefixMatcher()` 所定义的内容。

```c++
$GetMapping(fileResponse)
QString fileResponse(){
    return "$file::/resource/defaultWebConfig.json";
}
```

### 后缀

在第26行定义一个 `_file` 的 字面量。这个字面量将 const char* 的内容转换成 IFileResponse。所以上面的例子也可以写成

```c++
$GetMapping(fileResponse)
IFileResponse fileResponse(){
    return ":/resource/defaultWebConfig.json"_file;
}
```



## IHtmlResponse

IHtmlResponse 支持用户返回 html 类型的数据，数据返回到客户端会被解析成 html 并进行后续的操作，比如渲染等。IHtmlResponse 返回状态是 `200 OK`，返回的类型是`text/html; charset=UTF-8` 。

IHtmlResponse 的声明如下：

```c++
class IHtmlResponse : public IHttpResponseInterface<IHtmlResponse>
{
    $AsResponse(IHtmlResponse)
public:
    using IHttpResponseInterface::IHttpResponseInterface;

public:
    IHtmlResponse();
    IHtmlResponse(const QString& data);
    IHtmlResponse(std::string&&);
    IHtmlResponse(const std::string&);
    IHtmlResponse(QByteArray&&);
    IHtmlResponse(const QByteArray&);

public:
    virtual std::string prefixMatcher() final;
};

IHtmlResponse operator"" _html(const char* str, size_t size);
```

### 构造

在上述的代码中，我们可以看见 IHtmlResponse 可以被 String 类型进行隐式构造。所以用户可以返回一个String 类型或者字符串即可。

```c++
$GetMapping(htmlResponse)
IHtmlResponse htmlResponse(){
    return "<h1>hello world</h1>";
}
```

### 前缀

IHtmlResponse 的前缀是  $html:

```c++
$GetMapping(htmlResponsePrefix)
QString htmlResponsePrefix(){
    return "$html:<h1>hello world</h1>";
}
```

### 后缀

IHtml 的后缀类型字面量是 `_html`

```
$GetMapping(htmlResponseSurfix)
IHtmlResponse htmlResponseSurfix(){
    return "<h1>hello world</h1>"_html;
}
```

## IJsonResponse

IJsonResponse 用于返回json数据给用户，返回的状态是 `200 OK`， 返回的 mime 是`application/json; charset=UTF-8`。

### 类声明

IJsonResponse 的声明如下：

```c++
class IJsonResponse : public IHttpResponseInterface<IJsonResponse>
{
    $AsResponse(IJsonResponse)
public:
    using IHttpResponseInterface::IHttpResponseInterface;
//    using IResponseInterface::operator [];

public:
    IJsonResponse();
    IJsonResponse(const char*);
    IJsonResponse(const QString&);

    IJsonResponse(IJson&&);
    IJsonResponse(const IJson&);

    IJsonResponse(std::string&&);
    IJsonResponse(const std::string&);

    IJsonResponse(IString&&);
    IJsonResponse(const IString&);

    IJsonResponse(QByteArray&&);
    IJsonResponse(const QByteArray&);

    template<typename T>
    IJsonResponse(T value);

public:
    virtual std::string prefixMatcher() final;
};

IJsonResponse operator"" _json(const char* str, size_t size);
```

### 构造参数

#### String 类型构造

在上面的代码中，可以看到可以通过传入 String 类型数据，IJson类型数据来 构造一个IJsonResponse 对象。如下：

```c++
$GetMapping(jsonResponseArray)
IJsonResponse jsonResponseArray(){
    return R"(["apple", "banana", "cherry"])";
}

$GetMapping(jsonResponseObject)
IJsonResponse jsonResponseObject(){
    return R"({"name": "John", "age": 30, "city": "New York"})";
}
```

注意一点，这里如果构造的内容是 String类型 （QString， std::string, const char*, QByteArray）的话，IJsonResponse 是不会检查数据内容是否是正确，会直接将传入的String 数据发送给客户端。也就是说，如果开发者构造 IJsonResponse 的字符串参数是一个非法的json 数据的话，客户端也将接收到一个非法的 json 数据。所以这里开发者需要保证 json 数据的正确性，完整性。



#### IJson 构造

用户可以传入一个 IJson 对象来构造 IJsonResponse

```c++
$GetMapping(jsonTypeResponse)
IJsonResponse jsonTypeResponse(){
    return IJson::parse(R"({"name": "John", "age": 30, "city": "New York"})");
}
```



#### 模版构造

在上述的代码中，定义了一个模版构造函数，用户可以通过这个构造函数传递 Bean/复合类型的数据给 IJsonResponse， IJsonResponse 在构造函数内将对象转换成 json 数据，返回给客户端。

```c++
// 返回 {'index': 30, 'name': 'yuekeyuan'}
$GetMapping(jsonBean)
IJsonResponse jsonBean(){
    return MyBean(30, "yuekeyuan");
}

// 返回 [{'index': 30, 'name': 'yuekeyuan'}, {'index': 2, 'name': 'yueqichu'}]
$GetMapping(jsonBeans)
IJsonResponse jsonBeans(){
    return QList<MyBean>{
        MyBean(30, "yuekeyuan"),
        MyBean(2, "yueqichu")
    };
}

// 返回 [1, 2, 4, 5]
$GetMapping(jsonIntList)
IJsonResponse jsonIntList(){
    return QList<int>{
        1, 2, 4, 5
    };
}
```

具体有哪些类型可以转换，可以参考  `IHttpCore 路由返回类型 基础类型` 的文档。



### 前缀

IJsonResponse 的前缀是 `$json:` 用户可以通过该前缀将一个String 类型转换成 json 类型返回给用户

```c++
$GetMapping(jsonPrefix)
QString jsonPrefix()
{
    return R"($json:{"name": "John", "age": 30, "city": "New York"})";
}
```



### 后缀

用户可以通过 _json 字面量后缀将一个字符串转换成 IJsonResponse

```c++
$GetMapping(jsonSuffix)
IJsonResponse jsonSuffix()
{
    return "{\"name\": \"John\", \"age\": 30, \"city\": \"New York\"}"_json;
}
```

## IBytesResponse

IBytesResponse 将一段数据返回给请求端，状态是 `200 OK`, Content-Type是 `application/octet-stream`， 表示这个是一段字节流。他的定义如下：

```c++
class IBytesResponse : public IHttpResponseInterface<IBytesResponse>
{
    $AsResponse(IBytesResponse)
public:
    using IHttpResponseInterface::IHttpResponseInterface;
//    using IResponseInterface::operator [];

public:
    IBytesResponse();
    IBytesResponse(const char* data);
    IBytesResponse(const QString& data);

    IBytesResponse(QByteArray &&data);
    IBytesResponse(const QByteArray &data);

    IBytesResponse(std::string&&);
    IBytesResponse(const std::string&);

    IBytesResponse(IString&&);
    IBytesResponse(const IString&);

public:
    virtual std::string prefixMatcher() final;
};

IBytesResponse operator"" _bytes(const char* str, size_t size);
```

### 构造

如上所示，IBytesResponse 传入构造函数的是一系列的 String 类型。这些数据传入构造函数，然后被发送给请求方。

注意一点，构造函数支持 QString 类型的数据。在实际的处理中，IHttpCore 会将 QString 类型的数据通过 `toUtf8()` 这个函数转换成 QByteArray 类型。也就是说，这里我们默认的数据类型是 `utf-8` 类型的数据。如果用户传递的数据不是utf-8类型的，则需要用户自己手动转换。

举例如下：

```c++
$GetMapping(bytes)
IBytesResponse bytes(){
    return "hello world";
}

$GetMapping(bytesQString)
IBytesResponse bytesQString(){
    return QString(QStringLiteral("岳克远"));
}
```

### 前缀

IBytesResponse 的前缀是 `$bytes:`

```c++
$GetMapping(bytesPrefix)
IString bytesPrefix(){
    return "$bytes:hello world";
}
```



### 后缀

IBytesResponse 的后缀是 _bytes

```c++
$GetMapping(bytesSuffix)
IBytesResponse bytesSuffix(){
    return "hello world"_bytes;
}
```



## IPlainTextResponse

IPlainTextResponse 是用于返回一个 `text/plain` 类型数据的类型，返回状态是 `200 OK`。他的类型声明如下：

```c++
class IPlainTextResponse : public IHttpResponseInterface<IPlainTextResponse>
{
    $AsResponse(IPlainTextResponse)
public:
    using IHttpResponseInterface::IHttpResponseInterface;
//    using IResponseInterface::operator [];

public:
    IPlainTextResponse();
    virtual ~IPlainTextResponse() = default;

    IPlainTextResponse(const char* value);
    IPlainTextResponse(const QString& value);

    IPlainTextResponse(std::string&& value);
    IPlainTextResponse(const std::string& value);

    IPlainTextResponse(QByteArray&& value);
    IPlainTextResponse(const QByteArray& value);

    IPlainTextResponse(IString&& value);
    IPlainTextResponse(const IString& value);

public:
    virtual std::string prefixMatcher() final;
};

IPlainTextResponse operator"" _text(const char* str, size_t size);
```

### 构造

IPlainTextResponse 可以使用String 类型进行数据构造，示例代码如下：

```c++
$GetMapping(plain)
IPlainTextResponse plain(){
    return "hello world";
}

$GetMapping(plainIString)
IPlainTextResponse plainIString(){
    return IString("hello world");
}
```

### 前缀

IPlainTextResponse 的前缀是 `$text:`, 示例如下：

```c++
$GetMapping(plainPrefix)
QString plainPrefix(){
    return "$text:hello world";
}
```

### 后缀

IPlainTextResponse 的字面量后缀是 `_text`, 示例如下：

```c++
$GetMapping(plainSuffix)
IPlainTextResponse plainSuffix(){
    return "hello world"_text;
}
```

## IRedirectResponse

在IHttpCore中支持服务重定向的功能，开发者可以手动写状态码，写 header 中的 location内容，也可以使用 IRedirectResponse 这个Response 类。

IRedirectResponse 的返回状态是 `302 FOUND`。返回内容不存在，但是会在Header 中添加 `Location` 字段。IRedirectResponse 的声明如下：

```c++
class IRedirectResponse : public IHttpResponseInterface<IRedirectResponse>
{
    $AsResponse(IRedirectResponse)
public:
    using IHttpResponseInterface::IHttpResponseInterface;
//    using IResponseInterface::operator [];

public:
    IRedirectResponse();
    IRedirectResponse(const char* data);
    IRedirectResponse(const QString &path);
    IRedirectResponse(const std::string& path);
    IRedirectResponse(const QByteArray&& path);
    IRedirectResponse(const IString&& path);

public:
    virtual std::string prefixMatcher() final;
    void updateLocationPath();

private:
    QString m_redirectPath;
};
```

### 构造

IRedirectResponse 可以使用 IString构造。 IString 的内容必须是合法的`路径格式`。IRedirectResponse 不会检查路径的内容是否合法，所以开发者需要主动保证路径的合法性。示例如下：

```c++
$GetMapping(redirect)
IRedirectResponse redirect(){
    return "http://www.baidu.com";
}
```

在上述的示例中，客户端请求 /redirect 路径的时候，服务器端发送了 redirect 的要求给客户端，重定向的地址是 [`http://www.baidu.com`](http://www.baidu.com)。客户端会随之请求该路径的内容。

### 前缀

IRedirectResponse 的前缀是 `$redirect:` 。示例如下：

```c++
$GetMapping(redirectPrefix)
QString redirectPrefix(){
    return "$redirect:http://www.baidu.com";
}
```

### 后缀

IRedirectResponse 的后缀字面量 是 `_redirect`。示例如下：

```c++
$GetMapping(redirect)
IRedirectResponse redirectSuffix(){
    return "http://www.baidu.com"_redirect;
}
```

### 嵌套使用

IRedirectResponse 有一个非常方便的地方是该类可以返回给任意一个Response 类型。当一个函数在响应的过程中，发现该处理函数不满足条件的时候，就可以直接返回 IRedirectResponse 类型的数据给 Response。这样也可以返回数据，示例如下：

```c++
$GetMapping(redirectFromText)
IPlainTextResponse redirectFromText(){
    return IRedirectResponse("http://www.baidu.com");
}

$GetMapping(redirectFromJson)
IJsonResponse redirectFromJson(){
    return "http://www.baidu.com"_redirect;
}
```

上述不论 IPlainTextResponse 或者 IJsonResponse 或者其他类型的reponse， 在请求执行的时候都会重定位到 http://www.baidu.com 这个路径。



## IStatusResponse

IStatusResponse 返回一个状态码给请求者。如下是他的声明：

```c++
class IStatusResponse : public IHttpResponseInterface<IStatusResponse>
{
    $AsResponse(IStatusResponse)
public:
    using IHttpResponseInterface::IHttpResponseInterface;
//    using IResponseInterface::operator [];

public:
    IStatusResponse() = default;
    IStatusResponse(const QString&);
    IStatusResponse(const std::string&);
    IStatusResponse(int code, const QString& errorMsg="");
    IStatusResponse(IHttpStatus status, const QString& errorMsg="");

public:
    virtual std::string prefixMatcher() final;
};

IStatusResponse operator"" _status(unsigned long long int);
```

### 构造

构造一个 IStatusResponse， 第一个参数是状态码，第二个参数是可选的，是附带的信息。

注意这里的 status 不仅仅可以是 RFC 协议规定的 状态码，也可以是用户自定义的状态码。但是对于用户自定义的状态码而言，他的状态的解释是 UNKNOWN。例如，如果用户返回给的一个code 是 `600`， 这个状态码并没有被 RFC协议所规定和支持。那么他的响应首行可以是 `HTTP/1.1 600 UNKNOWN\r\n `。这种机制给用户提供一定的便捷性，用户自定义状态码。



当用户的第二个参数有内容的时候，也就是说用户想给当前的status 一个内容，这个内容的mime 是 `text/plain`。



如果传入的参数只有一个 String 类型的话，则这个String 类型所存储的内容必须是数字字符串。这样就能转换成 IHttpStatus。



 示例如下：

```c++
$GetMapping(status)
IStatusResponse status(){
    return {500, "hello world"};
}
```



### 前缀

IStatusResponse 的前缀是 `$staus:` 示例如下：

```c++
$GetMapping(statusPrefix)
QString statusPrefix(){
    return "$status:400";
}
```



### 后缀

IStatusResponse 的后缀是 `_status` 。示例如下：

```c++
$GetMapping(statusSuffix)
IStatusResponse statusSuffix(){
    return 400_status;
}
```



### 嵌套使用

IStatusResponse 可以作为其他的数据的返回值。比如，函数原本的返回类型是 IJsonResponse。 但在处理过程中发现有 错误，我想返回500 的错误，这个时候可以使用 IStatusResponse 来指定错误。下面是示例

```c++
$GetMapping(statusFromJson)
IJsonResponse statusFromJson(){
    return IStatusResponse(404);
}

$GetMapping(statusFromBytes)
IBytesResponse statusFromBytes(){
    return 500_status;
}
```



## Invalid 类型

在系统错误处理组件中，我们引入了 `Invalid` 类型， 具体内容可以参考 `http/invalid`。invalid 的目的是解决http协议请求响应的过程中的各种错误问题。开发者可以直接返回预定义的 Invalid 对象来处理函数处理过程中的invaild 对象。Invalid 在实际的应用中比 IStatusResponse 更加好用，方便。

如下是示例代码：

```c++
$GetMapping(notFoundInvalid)
IFileResponse notFoundInvalid(){
    return IHttpNotFoundInvalid("file not found");
}

$GetMapping(badRequest)
IJsonResponse badRequest(){
    return IHttpBadRequestInvalid("json value error");
}
```



直接返回 Invalid 可以在处理http 请求中对错误处理有更灵活的响应，降低编程的难度。



## 用户如何扩展自定义的类型

如果上述的类型不能够满足开发者的需求，开发者也可以自定义数据类型用于返回数据。
