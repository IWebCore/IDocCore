# IRdbValueGeneratorInterface

## 代码接口

`IRdbValueGeneratorInterface` 这个接口如下：

```c++
template<typename T, bool enabled=true>
class IRdbValueGeneratorInterface : public ITaskInstantUnit<T, enabled>
{
public:
    IRdbValueGeneratorInterface() = default;

public:
    virtual QString name() const = 0;
    virtual QVariant generator() const = 0;

private:
    virtual void $task() final;
};
```

该基类的 `QString name() const` 函数返回的名称是我们`generator`的名称，可以被用于 `$Generator` 宏注解中。`QVariant generator() const` 则是具体的生成函数，他的返回值是 `QVariant`,意思是用户可以返回任何合法的，可以转换的值，比如 `int`, `QString` 等一系列的类型。

`$task` 则是用于具体注册功能的函数。



这是一个`CRTP`模板类。第一个参数 T 是实现类的名称。第二个模板参数是 bool 类型，表示当前类是否启用。如果启用，则程序会将自身注册到系统当中，没启用，则不注册，在 `$GenerateValue` 宏中则不能使用该`generator`。



## 举例

下面我们举例

```c++
// PrefixGenerator.h
#include "rdb/entity/IRdbValueGeneratorInterface.h"

class PrefixGenerator : public IRdbValueGeneratorInterface<PrefixGenerator>
{
public:
    virtual QString name() const final;
    virtual QVariant generator() const final;
}

// PrefixGenerator.cpp
#include "IRdbUuidValueGenerator.h"

QString IRdbUuidValueGenerator::name() const
{
    return "prefixGen";
}

QVariant IRdbUuidValueGenerator::generator() const
{
    static int value{};
    return "prefix_" + QString::number(value);
}
```

上面的代码不规范，因为如果软件重启的话，计数又会从零开始。所以用户设计自己的`Generator`时需要慎重考虑。



如下我们粘贴上uuid 的代码

- IRdbUuidValueGenerator.h

```c++
#pragma once

#include "rdb/entity/IRdbValueGeneratorInterface.h"
using namespace IWebCore;

class IRdbUuidValueGenerator : public IRdbValueGeneratorInterface<IRdbUuidValueGenerator>
{
public:
    IRdbUuidValueGenerator() = default;

public:
    virtual QString name() const final;
    virtual QVariant generator() const final;
};
```

- IRdbUuidGenerator.cpp

```c++
#include "IRdbUuidValueGenerator.h"

QString IRdbUuidValueGenerator::name() const
{
    return "uuid";
}

QVariant IRdbUuidValueGenerator::generator() const
{
    return QUuid::createUuid().toString();
}
```