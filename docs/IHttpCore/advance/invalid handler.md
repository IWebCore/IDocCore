# invalid handler

## 前言

在 IHttpCore 中，Invalid 是一个很有用的设计。可以让正在执行流程的http请求可以随时进入错误处理的块车道，而这个正是满足 http 请求在解析执行过程中的诸多不确定性的特点。

但是，在默认的 invalid 中，比如 IHttpNotFoundInvalid 中，他的默认输出 状态是 200， mime 是 text/plain, 而且内容更是  `IWebCore::IHttpNotFoundInvalid` 这个invalid的程序名称这样的内容。

输出是正确的，没有问题的。但是对于开发者和终端用户而言，则希望能够可以定制，更有个性化。而不是输出一个 `IWebCore::IHttpNotFoundInvalid`。 本文档描述如何修改 invalid 返回内容。



## 继承一个新的 invalid

IHttpInvalidInterface 的内容如下：

```cpp
template<typename T, bool enabled=true>
class IHttpInvalidInterface : public IHttpInvalidWare
{
public:
    IHttpInvalidInterface(IHttpStatus code);
    IHttpInvalidInterface(IHttpStatus code, const std::string& description);
};
```

我们实现的 IHttpNotFoundInvalid 如下：

```cpp
// IHttpNotFoundInvalid.h
#pragma once

#include "core/util/IHeaderUtil.h"
#include "http/invalid/IHttpInvalidInterface.h"

$PackageWebCoreBegin

class IHttpNotFoundInvalid : public IHttpInvalidInterface<IHttpNotFoundInvalid>
{
public:
    IHttpNotFoundInvalid();
    IHttpNotFoundInvalid(const std::string& description);
};

$PackageWebCoreEnd

// .cpp
#include "IHttpNotFoundInvalid.h"
#include "http/detail/IHttpResponseRaw.h"

$PackageWebCoreBegin

IHttpNotFoundInvalid::IHttpNotFoundInvalid()
    : IHttpInvalidInterface(IHttpStatus::NOT_FOUND_404)
{
}

IHttpNotFoundInvalid::IHttpNotFoundInvalid(const std::string& description)
    : IHttpInvalidInterface(IHttpStatus::NOT_FOUND_404, description)
{
}

$PackageWebCoreEnd

```

### 调用的时候传入 我们想要返回的内容

所以如果我们想直接返回一个自己的字符串，则可以直接在 invalid 中写入原因即可

```cpp
request.setInvalid(IHttpNotFoundInvalid("view is empty"));
```

这样，用户得到的就是 view is empty 这个string

### 重载 process 函数

这里还可以继承这个基类，自己写一个 自己的 NotFound, 实现自己的 process 函数

```cpp
class MyNotFoundInvalid : public IHttpInvalidInterface<MyNotFoundInvalid>
{
public:
    MyNotFoundInvalid();
    MyNotFoundInvalid(const std::string& description);

public:
    virtual void process(const IHttpInvalidWare&, IHttpResponseRaw&) const final;
};

// .cpp
MyNotFoundInvalid::MyNotFoundInvalid()
    : IHttpInvalidInterface(IHttpStatus::NOT_FOUND_404)
{
}

MyNotFoundInvalid::MyNotFoundInvalid(const std::string& description)
    : IHttpInvalidInterface(IHttpStatus::NOT_FOUND_404, description)
{
}

void MyNotFoundInvalid::process(const IHttpInvalidWare &ware, IHttpResponseRaw & raw) const
{
    raw.setContent(new IHttpResponseContent(ware.description.toStdString()));
}
```

程序在最后生成要返回给客户端的字符串的时候，会调用这个 process 函数。此时用户可以在process 中修改结果。

注意这里修改结果是在 IHttpResponseRaw 中进行修改的，可以修改 mime, status, headers 等各种内容。

如果用户想修改返回的具体的内容，此时需要调用 raw.setContent(), 添加一个新的内容，返回给用户即可。而且在process 中，不论如何都要有一个新的 content 被设置进去。



## InvalidHandler

用户可以有第二个选择，通过继承 InvalidHandler 来修改返回的结果，

### 声明

InvalidHandlerWare 声明如下：

```cpp
class IHttpResponseRaw;
class IHttpInvalidWare;
class IHttpInvalidHandlerWare
{
public:
    IHttpInvalidHandlerWare() = default;

public:
    virtual void handle(const IHttpInvalidWare&, IHttpResponseRaw&) const;
};
```

注意这里有一个 handle 函数，他的用法和上述的 process 的用法是一致的。

InvalidHandlerInterface 声明如下：

```cpp
template<typename T, typename Invalid, bool enabled=true>
class IHttpInvalidHandlerInterface : public IHttpInvalidHandlerWare, public ITaskWareUnit<T, IHttpTaskCatagory, enabled>, public ISoloUnit<T>
{
public:
    virtual double $order() const override;
    virtual void $task() final;
};
```

注意模板参数的第二项是 Invalid 参数。这个参数就是你要拦截的那个 Invalid。

### 示例

我们写一个示例：

```cpp
// .h
class IHttpBadRequestInvalidHandler : public IHttpInvalidHandlerInterface<IHttpBadRequestInvalidHandler, IHttpBadRequestInvalid, true>
{
public:
    IHttpBadRequestInvalidHandler();

public:
    virtual void handle(const IHttpInvalidWare&, IHttpResponseRaw&) const override final;
};

// .cpp
IHttpBadRequestInvalidHandler::IHttpBadRequestInvalidHandler()
{
}

void IHttpBadRequestInvalidHandler::handle(const IHttpInvalidWare &ware, IHttpResponseRaw &raw) const
{
    raw.setMime(IHttpMime::APPLICATION_JSON_UTF8);
    raw.setContent(new IHttpResponseContent("hello world"));
}
```

这里需要注意的是第2 行，父类的模板参数中是  IHttpBadRequestInvalid。 这时就将 这个 handler 绑定到 IHttpBadRequestInvalid 上面去了。

注意一点，handler 的优先级高于 process!