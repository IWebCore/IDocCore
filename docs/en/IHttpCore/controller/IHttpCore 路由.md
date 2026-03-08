. Therefore, the character set in path segments should include:
> - **Letters**: `a-z`, `A-Z`
> - **Digits**: `0-9`
> - **Special characters**: `-`, `_`, `.`, `~`, etc. (These are common valid characters in URIs)
> - **Separators**: `!`, `$`, `&`, `'`, `(`, `)`, `*`, `+`, `,`, `;`, `=`, etc.
> - **Encoded characters**: (e.g., `%20` for space)
> - **Path segments cannot contain slashes `/`**, as `/` is used as a separator between path segments. If a slash is needed within a path segment, it must be URL-encoded as `%2F`.

Additionally, Chinese characters and other content can also be part of route segments. Chinese characters are URL-encoded into ordinary route segments during server request transmission and URL-decoded back into Chinese characters upon server receipt. However, it is not recommended to use Chinese characters during development.

Below are some examples of valid path segments:

1. Letters and digits:

> Example: `abc123`, `HelloWorld`, `file2025`

2. Special characters (common valid characters):

- Hyphen (`-`)
- Underscore (`_`)
- Period (`.`)
- Tilde (`~`)
- At symbol (`@`)
- Plus (`+`)
- Comma (`,`), Semicolon (`;`), Equals (`=`)

> Example: `product-name`, `user_profile`, `file.name`, `folder~1`

3. Chinese characters (no encoding needed):

Modern browsers and servers support Chinese characters as part of path segments:

> Example: `/产品`, `/手机/价格`

4. Combinations of numbers and symbols:

> Example: `product-123`, `data_2025`, `name~version`

5. Path segments with encoded characters:

Some special characters (e.g., space, `#`, `?`, `&`, etc.) cannot appear directly in path segments and must be URL-encoded.

> Example: Space: `%20`

### <> Path

This path is a wildcard used to match any segment in the path. Note that it can only and must match one path segment. If the path segment is empty or if there are multiple path segments, it cannot match.

- **Example**: `/products/<>`
  - Matches: `/products/123`, `/products/abc`
  - Does not match: `/products/123/details`, `/products`

- **Usage Example**:

```c++
$GetMapping(fun, /products/<>)
QString fun();

$GetMapping(hello, /products/<>/hello)
QString hello();
```

Note that this wildcard only matches the path and does not capture it. If the user wants to match a path without caring about its content, they can directly use `<>`. If the user wants to capture the path segment or impose format constraints on the path, then refer to the following section on route segment matching formats.

### <name>

The `<name>` segment is similar to the `<>` wildcard in that it matches any content in the path segment. The difference is that `<name>` not only matches the URL path segment but also captures its content, which can be placed as a function parameter or queried using the `IRequest` class.

Below is an example:

```c++
$GetMapping(hi, hi/<your>/<name>)
QString hi(QString $Path(your), QString $Path(name)) {
    return your + name;
}
```

In the above example, we capture the second and third path segments and concatenate them. Note that the function parameters are prefixed with `$Path`, indicating that `your` and `name` must be retrieved from the captured path parameters. For details on request parameter constraints, see the relevant section on `IHttpCore function parameters`.

For the request above, the request path is `/hi/yue/keyuan`, and the return content is `yuekeyuan`, achieving perfect interception.

### <name | restrict>

In practical applications, users not only want to capture parameters but also want the parameters to meet certain criteria. For example, the parameter must be a number, must match a specific regular expression, or must adhere to user-defined rules. The `<name|restrict>` route segment is designed to impose constraints on parameters, ensuring they meet certain requirements, and requests with invalid parameters cannot be routed to the handler.

In this route rule, `name` represents the captured parameter name. If the user only wants parameter constraints and omits the `name` content, the path segment becomes `<|restrict>`. This path segment only validates the URL and does not capture the segment.

Additionally, the `restrict` part can be omitted, making the wildcard `<name|>` or `<|>`, which matches any URL segment.

IHttpCore provides a series of predefined restrictions. They are as follows:

- **Numeric Types**:

> `short`, `ushort`, `int`, `uint`, `long`, `ulong`, `longlong`, `ulonglong`, `float`, `double`

These are numeric types. If the queried parameter is numeric and within the range of the selected type, the match succeeds; otherwise, it fails.

- **Date and Time Types**:

> `date`, `QDate`, `time`, `QTime`, `datetime`, `QDateTime`

These are date and time types. The input must be convertible to Qt-supported date/time formats, such as `date/QDate`. If the input can be converted to this type, the match succeeds.

- **String Types**:

> `string`, `QString`

These are placeholders. Any content can be matched by these, and they are included for completeness.

- **Special Types**:

> `uuid`, `base64`

The `uuid` type is for values matching the QUUid format. `base64` refers to values that are base64-encoded.

Below are examples illustrating the above:

```c++
$GetMapping(datetimeVal, /datetimeVal/<val|datetime>)
QString datetimeVal(QDateTime $Path(val)) {
    return val.toString(Qt::DateFormat::ISODate);
}

$GetMapping(doubleVal, /doubleVal/<val|double>)
QString doubleVal(double $Path(val)) {
    return QString::number(val);
}

$GetMapping(uuidVal, /uuidVal/<val|uuid>)
QString uuidVal(QString $Path(val)) {
    return val;
}
```

Additionally, users can define their own restrictions to meet development needs. For details, see the relevant section on "Custom Path Restrictions."

### <name || regexp>

Path segments can also be matched using regular expressions. If a path requires a special matching rule that is only used once, defining a parameter constraint might not be worth it. Using a regular expression is a simpler approach.

Note that the regular expression constraint uses `||` between `name` and `regexp`, which is the key difference between regular expression constraints and named constraints.

Below is an example:

```c++
$GetMapping(hello, hello/<path||(\\w+)>)
QString hello(QString $Path(path)) {
    return path;
}

$GetMapping(world, world/<path||abc.*>)
QString world(QString $Path(path)) {
    return path;
}
```

The first route captures any word characters, and the second route captures names starting with `abc`.

In regular expression route segments, the `name` can be omitted, becoming `<||regexp>`. This indicates that the route segment only performs regular expression matching and does not capture parameters.

Users can also omit `regexp`, writing `<name||>`, which matches all paths and captures them as the `name` variable. Users can also omit both, resulting in `<||>`, which functions the same as `<>`.

### "/" Root Directory

If the user wants to map a path to the root directory, the mapping parameter must be written as `/`, as shown below:

```c++
$GetMapping(index, /)
QString index();
```

This will bind the `index()` function to the root directory of the URL. If a prefix is defined with `$AsController` in the Controller, the `index` will be mapped to the URL under the prefix.

### Function Name as Path

If the mapping relation includes only the function name and no path, the function name itself is the mapped path.

```c++
$GetMapping(index)
QString index();
```

In this case, the mapped path for the `index` function is `/index`. This shorthand reduces user input and cognitive load.

### Precautions

- Path segments cannot be `..` or `.`.
- `..` denotes the parent directory, and `.` denotes the current directory. These segments are not allowed.
- The leading `/` can be omitted without affecting path parsing.
- The function name in the mapping must correspond to the actual function. If they do not match, an exception will be thrown during runtime.
- Overloaded functions are currently not supported. Each function name can appear only once in the Controller. If overloaded functions are used, the program will throw an error.

## Custom Path Restrictions

Besides the built-in restrictions provided by the framework, users can also add custom path restriction rules by inheriting from the `IHttpPathValidatorInterface` class.

### IHttpPathValidatorInterface

The declaration of this class can be simplified as follows:

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

This is a CRTP template base class. Users can inherit from this base class to define their own restrictions. The first template parameter is the name of the subclass, which is the foundation of CRTP. The second template parameter is a boolean, defaulting to `true`, indicating whether the restriction is enabled. If set to `false`, the restriction is not enabled, and its task is not executed.

In this class, there are two pure virtual functions that must be overridden by subclasses. The `marker()` function returns the marker for the route segment restriction. The `validator()` function returns a functor of type `std::function<bool(IStringView)>`, which can be a static function, a lambda expression, or a wrapped member function.

### Example

Below is an example defining a `gender` route restriction. This restriction only allows input of two genders, `male` and `female`. If the input does not match, the route cannot be matched. The implementation code is as follows:

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

The `gender` type is now registered. Below is a set of route mappings for verification:

```c++
    $GetMapping(gender, /gender/<gender|gender>)
    QString gender(QString $Path(gender))
    {
        return gender;
    }
```

The code compiles successfully, passes unit tests, and can handle non-male and non-female inputs properly.