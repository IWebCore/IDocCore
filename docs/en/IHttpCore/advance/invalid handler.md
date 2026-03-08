# invalid handler

## Introduction

In IHttpCore, `Invalid` is a useful design pattern. It allows HTTP requests being processed to seamlessly transition into error-handling segments, which addresses the uncertainties inherent in HTTP request processing.

However, the default `invalid` implementation, such as `IHttpNotFoundInvalid`, has a default output status of 200, MIME type as text/plain, and content that is the program name of `IWebCore::IHttpNotFoundInvalid`. 

While this output is technically correct and functional, developers and end-users often desire customization for more personalized responses. Instead of outputting the program name `IWebCore::IHttpNotFoundInvalid`, they want more tailored responses. This document describes how to modify the return content of an `invalid` handler.

---

## Creating a New Invalid Handler

The content of `IHttpInvalidInterface` is as follows:

```cpp
template<typename T, bool enabled=true>
class IHttpInvalidInterface : public IHttpInvalidWare
{
public:
    IHttpInvalidInterface(IHttpStatus code);
    IHttpInvalidInterface(IHttpStatus code, const std::string& description);
};
```

The implementation of `IHttpNotFoundInvalid` is as follows:

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

### Passing the Desired Return Content During Invocation

If you want to directly return a custom string, you can simply pass the reason in the `invalid` handler:

```cpp
request.setInvalid(IHttpNotFoundInvalid("view is empty"));
```

This way, the user receives the string `view is empty`.

### Overriding the `process` Function

Alternatively, you can inherit from the base class and implement your own `NotFound` handler by overriding the `process` function:

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

During the final step when the program generates the response to return to the client, the `process` function is called. At this point, users can modify the outcome.

Note that modifications occur within the `IHttpResponseRaw` object. Users can adjust the MIME type, status code, headers, and other content-related aspects.

If users wish to modify the specific content returned, they must call `raw.setContent()` to set a new content object. Importantly, the `process` function must set a new content object regardless of the outcome.

---

## InvalidHandler

Users have a second option to customize the return result by inheriting from `InvalidHandler`.

### Declaration

The `IHttpInvalidHandlerWare` class is declared as follows:

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

Note that the `handle` function is used similarly to the `process` function described above.

The `IHttpInvalidHandlerInterface` is declared as follows:

```cpp
template<typename T, typename Invalid, bool enabled=true>
class IHttpInvalidHandlerInterface : public IHttpInvalidHandlerWare, public ITaskWareUnit<T, IHttpTaskCatagory, enabled>, public ISoloUnit<T>
{
public:
    virtual double $order() const override;
    virtual void $task() final;
};
```

Note that the template parameter `Invalid` specifies the `Invalid` handler this class is intended to intercept.

### Example

Here is an example implementation:

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

Note that in line 2, the template parameter `IHttpBadRequestInvalid` specifies that this handler is bound to `IHttpBadRequestInvalid`.

One important point: handlers have higher priority than `process` functions!