# IRdbValueGeneratorInterface

## Code Interface

The `IRdbValueGeneratorInterface` interface is defined as follows:

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

The `QString name() const` function in the base class returns the name of the `generator`, which can be used in the `$Generator` macro annotation. The `QVariant generator() const` function returns a concrete generated value, and its return value is a `QVariant`, meaning the user can return any valid and convertible value, such as `int`, `QString`, etc.

The `$task` function is used for specific registration functionality.

This is a `CRTP` template class. The first parameter `T` is the name of the implementing class. The second template parameter is a `bool` type, indicating whether the current class is enabled. If enabled, the program will register itself to the system; if not enabled, it will not register, and the `generator` cannot be used in the `$GenerateValue` macro.

## Example

The following is an example:

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

The above code is not standardized because if the software restarts, the counter will start from zero again. Therefore, when users design their own `Generator`, they need to carefully consider this.

The following is the code for the UUID generator:

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