# IHttpCore Route Return Type: Response Type

In IHttpCore, we define a series of Response types as the return value types for functions. Users can use these types to return data.

## Overview of Response Types

> There is also the concept of suffixes here, along with `$json:`.

In the above simple return type process, we can return a series of types. However, the types mentioned above have several shortcomings. For example, they cannot set the return status, cannot set a series of header statuses, cannot add cookie types, and if an exception occurs during data processing, there is no way to return an exception indicator to the client. Therefore, we introduced the concept of Response types.

Response types are named with `I` as the prefix and `Response` as the suffix. For example, `IFileResponse`, `IHtmlResponse`, etc. Users can also define their own return types. IHttpCore also provides a plugin called `INodyResponse`, which supports users in returning an HTML template name and a set of data for rendering. The template and rendering data are combined to generate a complete HTML content and returned to the user.

At the same time, our basic return types are also wrapped into corresponding Response types during actual parsing. For example, when the return type is `IJson`, IHttpCore will wrap the value of `IJson` into an `IJsonResponse` type during parsing. Our `IHttpStatus` type will be wrapped into an `IStatusResponse` type. `QString` is generally wrapped into `IPlainTextResponse`. The reason it is "general" is that there are some special handling contents for string types, which will be listed here.

One thing to note is that the prefix of our Response types is `I`, without the library restriction of `Http`. For example, `IHtmlResponse` is not `IHttpHtmlResponse`. Although this breaks our naming convention, the benefit is that developers can shorten the code when writing. Since the http module is the most frequently used module, this is worth doing. If other modules need response types in the future, we will need to add the prefix. For example, if there is a module called Abc in the future, its Response type should be `IAbcFileResponse`, not `IFileResponse`.

### IHttpResponseInterface and IHttpResponseWare

`IHttpResponseInterface` is the CRTP base class for all Response types. If developers want to write their own Response, they can inherit from this base class. For details on extending Response, refer to the following content.

`IHttpResponseWare` is a parent class of `IHttpResponseInterface`. `IResponseWare` is the base class for storing the returned content. In `IHttpResponseWare`, a series of content for returning to the client, such as mime, status, header, session, and content, can be set.

### Suffix Types

In IHttpCore, we define many string literals for Response types. For example:

```cpp
IFileResponse operator"" _file(const char* str, size_t size);
IHtmlResponse operator"" _html(const char* str, size_t size);
```

These literals can construct the corresponding Response types. This allows users to directly use the literal suffixes to construct objects during returns. For example:

```cpp
$GetMapping(fileResponse)
IFileResponse fileResponse(){
    return ":/resource/defaultWebConfig.json"_file;
}
```

### Prefix Types

When a function returns a String type, IHttpCore defines a series of prefixes that can convert the String data into other types, such as file type, html type, etc. For example:

```cpp
$GetMapping(fileResponse)
QString fileResponse()
{
    return "$file::/resource/defaultWebConfig.json";
}
```

This function returns a QString type data `"$file::/resource/defaultWebConfig.json"`. During actual parsing, this data is split into two parts: `$file:` and `:/resource/defaultWebConfig.json`. The prefix `$file:` is a data type prefix that is matched during parsing. Therefore, this returned data is parsed into an `IFileResponse` type, using `:/resource/defaultWebConfig.json` to construct it. This is the prefix type.

Another example:

```cpp
$GetMapping(htmlResponse)
IString htmlResponse()
{
    return "$html:<h1>hello world</h>";
}
```

During actual response, this request constructs an `IHtmlResponse` with the content `<h1>hello world</h>`, and returns it to the client with the Content-Type set to `text/html; charset=UTF-8`, not `text/plain`.

### Returning Invalid

### Returning Status

Below is an explanation of the various Response types defined in our framework.

## IFileResponse

`IFileResponse` supports users in returning a file to the client.

```cpp
$GetMapping(fileResponse)
IFileResponse fileResponse(){
    return ":/resource/defaultWebConfig.json";
}
```

`IFileResponse` attempts to find a corresponding MIME type during parsing. If found, it uses the found MIME type; if not, it uses `application/octet-stream`, indicating that this is a binary stream file. For details on MIME types, refer to the `http/mime` documentation.

Users can return Qt resource files or Qt resource files, which can be compiled into the executable program together with the code. These files start with `:/`, as shown in the code above. Users can also specify a relative or absolute path pointing to a file.

The type definition of `IFileResponse` is as follows:

```cpp
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

Our constructor is not marked as explicit, so users can directly return a string type, and `IFileResponse` will automatically construct and parse the relevant content.

### contentDisposition

Note that the class has a `enableContentDisposition` function. This function can be called during return to add a `Content-Disposition` header to the client's response. The purpose of this header is that when the client, such as a browser, requests the file, it will directly save the file instead of displaying it in the client.

```cpp
$GetMapping(fileResponse)
IFileResponse fileResponse(){
    IFileResponse data(":/resource/defaultWebConfig.json"_file);
    data.enableContentDisposition();
    return data;
}
```

### File Expiration Issue

If the file provided by the user does not exist, it will return `IHttpNotFoundInvalid`, i.e., a 500 status. We do not return a `404` status here because the URL was matched during the request process, but the file pointed to by the handler is invalid. This is a server response issue, not a URL lookup issue.

### Prefix

The prefix of `IFileResponse` is `$file:`, which is defined by `prefixMatcher()`.

```cpp
$GetMapping(fileResponse)
QString fileResponse(){
    return "$file::/resource/defaultWebConfig.json";
}
```

### Suffix

A `_file` literal suffix is defined on line 26. This literal converts const char* content into an `IFileResponse`. Therefore, the example above can also be written as:

```cpp
$GetMapping(fileResponse)
IFileResponse fileResponse(){
    return ":/resource/defaultWebConfig.json"_file;
}
```

## IHtmlResponse

`IHtmlResponse` supports users in returning HTML type data. The data returned to the client is parsed as HTML and further operations, such as rendering, are performed. The return status of `IHtmlResponse` is `200 OK`, and the return type is `text/html; charset=UTF-8`.

The declaration of `IHtmlResponse` is as follows:

```cpp
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

### Construction

In the code above, it can be seen that `IHtmlResponse` can be implicitly constructed from String type data. Therefore, users can return a String type or string data.

```cpp
$GetMapping(htmlResponse)
IHtmlResponse htmlResponse(){
    return "<h1>hello world</h1>";
}
```

### Prefix

The prefix of `IHtmlResponse` is `$html:`.

```cpp
$GetMapping(htmlResponsePrefix)
QString htmlResponsePrefix(){
    return "$html:<h1>hello world</h1>";
}
```

### Suffix

The suffix literal for `IHtmlResponse` is `_html`.

```cpp
$GetMapping(htmlResponseSurfix)
IHtmlResponse htmlResponseSurfix(){
    return "<h1>hello world</h1>"_html;
}
```

## IJsonResponse

`IJsonResponse` is used to return JSON data to users. The return status is `200 OK`, and the MIME type is `application/json; charset=UTF-8`.

### Class Declaration

The declaration of `IJsonResponse` is as follows:

```cpp
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

### Construction Parameters

#### String Type Construction

In the code above, it can be seen that `IJsonResponse` can be constructed by passing String type data. For example:

```cpp
$GetMapping(jsonResponseArray)
IJsonResponse jsonResponseArray(){
    return R"(["apple", "banana", "cherry"])";
}

$GetMapping(jsonResponseObject)
IJsonResponse jsonResponseObject(){
    return R"({"name": "John", "age": 30, "city": "New York"})";
}
```

Note that if the constructed content is a String type (QString, std::string, const char*, QByteArray), `IJsonResponse` will not check the content of the data and will directly send the passed String data to the client. That means if the developer constructs an `IJsonResponse` with a String parameter that is not a valid JSON, the client will also receive invalid JSON data. Therefore, developers need to ensure the correctness and completeness of the JSON data.

#### IJson Construction

Users can pass an `IJson` object to construct `IJsonResponse`.

```cpp
$GetMapping(jsonTypeResponse)
IJsonResponse jsonTypeResponse(){
    return IJson::parse(R"({"name": "John", "age": 30, "city": "New York"})");
}
```

#### Template Construction

In the code above, a template constructor is defined. Users can use this constructor to pass bean/composite type data to `IJsonResponse`. `IJsonResponse` converts the object into JSON data inside the constructor and returns it to the client.

```cpp
// Return {'index': 30, 'name': 'yuekeyuan'}
$GetMapping(jsonBean)
IJsonResponse jsonBean(){
    return MyBean(30, "yuekeyuan");
}

// Return [{'index': 30, 'name': 'yuekeyuan'}, {'index': 2, 'name': 'yueqichu'}]
$GetMapping(jsonBeans)
IJsonResponse jsonBeans(){
    return QList<MyBean>{
        MyBean(30, "yuekeyuan"),
        MyBean(2, "yueqichu")
    };
}

// Return [1, 2, 4, 5]
$GetMapping(jsonIntList)
IJsonResponse jsonIntList(){
    return QList<int>{
        1, 2, 4, 5
    };
}
```

For details on which types can be converted, refer to the documentation on `IHttpCore Route Return Type Basic Types`.

### Prefix

The prefix of `IJsonResponse` is `$json:`. Users can use this prefix to convert a String type into JSON type and return it to the user.

```cpp
$GetMapping(jsonPrefix)
QString jsonPrefix()
{
    return R"($json:{"name": "John", "age": 30, "city": "New York"})";
}
```

### Suffix

Users can use the `_json` literal suffix to convert a string into `IJsonResponse`.

```cpp
$GetMapping(jsonSuffix)
IJsonResponse jsonSuffix()
{
    return "{\"name\": \"John\", \"age\": 30, \"city\": \"New York\"}"_json;
}
```

## IBytesResponse

`IBytesResponse` returns a segment of data to the requester. The status is `200 OK`, and the Content-Type is `application/octet-stream`, indicating that this is a byte stream. Its definition is as follows:

```cpp
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

### Construction

As shown above, the constructor of `IBytesResponse` accepts a series of String type data. This data is passed to the constructor and then sent to the requester.

Note that the constructor supports QString type data. During actual processing, IHttpCore converts the QString type data to QByteArray type using the `toUtf8()` function. This means that the default data type is UTF-8 type. If the user passes data that is not UTF-8 type, the user needs to manually convert it.

Example:

```cpp
$GetMapping(bytes)
IBytesResponse bytes(){
    return "hello world";
}

$GetMapping(bytesQString)
IBytesResponse bytesQString(){
    return QString(QStringLiteral("岳克远"));
}
```

### Prefix

The prefix of `IBytesResponse` is `$bytes:`.

```cpp
$GetMapping(bytesPrefix)
IString bytesPrefix(){
    return "$bytes:hello world";
}
```

### Suffix

The suffix of `IBytesResponse` is `_bytes`.

```cpp
$GetMapping(bytesSuffix)
IBytesResponse bytesSuffix(){
    return "hello world"_bytes;
}
```

## IPlainTextResponse

`IPlainTextResponse` is used to return `text/plain` type data. The return status is `200 OK`. Its type declaration is as follows:

```cpp
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

### Construction

`IPlainTextResponse` can be constructed using String type data. Example code is as follows:

```cpp
$GetMapping(plain)
IPlainTextResponse plain(){
    return "hello world";
}

$GetMapping(plainIString)
IPlainTextResponse plainIString(){
    return IString("hello world");
}
```

### Prefix

The prefix of `IPlainTextResponse` is `$text:`. Example is as follows:

```cpp
$GetMapping(plainPrefix)
QString plainPrefix(){
    return "$text:hello world";
}
```

### Suffix

The literal suffix for `IPlainTextResponse` is `_text`. Example is as follows:

```cpp
$GetMapping(plainSuffix)
IPlainTextResponse plainSuffix(){
    return "hello world"_text;
}
```

## IRedirectResponse

IHttpCore supports service redirection functionality. Developers can manually write status codes and location content in the header, or use the `IRedirectResponse` Response type.

The return status of `IRedirectResponse` is `302 FOUND`. The return content does not exist, but a `Location` field is added to the header. The declaration of `IRedirectResponse` is as follows:

```cpp
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

### Construction

`IRedirectResponse` can be constructed using `IString`. The content of `IString` must be in valid path format. `IRedirectResponse` does not check the validity of the path content, so developers need to ensure the path's validity. Example is as follows:

```cpp
$GetMapping(redirect)
IRedirectResponse redirect(){
    return "http://www.baidu.com";
}
```

In the above example, when the client requests the `/redirect` path, the server sends a redirect request to the client with the redirect address `http://www.baidu.com`. The client will then request the content of that path.

### Prefix

The prefix of `IRedirectResponse` is `$redirect:`. Example is as follows:

```cpp
$GetMapping(redirectPrefix)
QString redirectPrefix(){
    return "$redirect:http://www.baidu.com";
}
```

### Suffix

The suffix literal for `IRedirectResponse` is `_redirect`. Example is as follows:

```cpp
$GetMapping(redirect)
IRedirectResponse redirectSuffix(){
    return "http://www.baidu.com"_redirect;
}
```

### Nested Usage

A convenient aspect of `IRedirectResponse` is that it can be returned as a value for any Response type. When a function discovers that it cannot process the request during response, it can directly return an `IRedirectResponse` type data. This can also return data. Example is as follows:

```cpp
$GetMapping(redirectFromText)
IPlainTextResponse redirectFromText(){
    return IRedirectResponse("http://www.baidu.com");
}

$GetMapping(redirectFromJson)
IJsonResponse redirectFromJson(){
    return "http://www.baidu.com"_redirect;
}
```

In the above examples, whether `IPlainTextResponse`, `IJsonResponse`, or other types of response, during request execution, they will all be redirected to `http://www.baidu.com`.

## IStatusResponse

`IStatusResponse` returns a status code to the requester. Its declaration is as follows:

```cpp
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

### Construction

To construct an `IStatusResponse`, the first parameter is the status code, and the second parameter is an optional additional information.

Note that the status can not only be the status codes defined by the RFC protocol but also user-defined status codes. However, for user-defined status codes, their meaning is UNKNOWN. For example, if a user returns a code of `600`, this status code is not defined or supported by the RFC protocol. The response line can then be `HTTP/1.1 600 UNKNOWN\r\n`. This mechanism provides users with some convenience for handling custom status codes.

When the second parameter contains content, i.e., the user wants to provide content for the current status, the MIME type of this content is `text/plain`.

If only a String type parameter is passed, the content stored in the String must be a numeric string. This can be converted into `IHttpStatus`.

Example is as follows:

```cpp
$GetMapping(status)
IStatusResponse status(){
    return {500, "hello world"};
}
```

### Prefix

The prefix of `IStatusResponse` is `$status:`. Example is as follows:

```cpp
$GetMapping(statusPrefix)
QString statusPrefix(){
    return "$status:400";
}
```

### Suffix

The suffix of `IStatusResponse` is `_status`. Example is as follows:

```cpp
$GetMapping(statusSuffix)
IStatusResponse statusSuffix(){
    return 400_status;
}
```

### Nested Usage

`IStatusResponse` can be used as the return value for other data. For example, a function's original return type is `IJsonResponse`, but during processing, an error is found, and the intention is to return a 500 error. In this case, `IStatusResponse` can be used to specify the error. Example is as follows:

```cpp
$GetMapping(statusFromJson)
IJsonResponse statusFromJson(){
    return IStatusResponse(404);
}

$GetMapping(statusFromBytes)
IBytesResponse statusFromBytes(){
    return 500_status;
}
```

## Invalid Type

In the system's error handling component, we introduce the `Invalid` type. For details, refer to `http/invalid`. The purpose of `Invalid` is to address various error issues in the HTTP request-response process. Developers can directly return predefined Invalid objects to handle invalid objects during function processing. `Invalid` is more convenient and easier to use than `IStatusResponse` in practical applications.

The following is an example code:

```cpp
$GetMapping(notFoundInvalid)
IFileResponse notFoundInvalid(){
    return IHttpNotFoundInvalid("file not found");
}

$GetMapping(badRequest)
IJsonResponse badRequest(){
    return IHttpBadRequestInvalid("json value error");
}
```

Directly returning Invalid provides more flexible error handling in HTTP requests, reducing the difficulty of programming.

## How Users Can Extend Custom Types

If the above types do not meet the developers' needs, developers can also define their own data types for returning data.