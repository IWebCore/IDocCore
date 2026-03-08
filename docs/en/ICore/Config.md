# Configuration Module

## Introduction

ICore provides a set of highly useful configuration modules. Users can simply add configuration information and conveniently reference it. For example, the macro annotation used in ICore, `$SetAppThreadCount(4)`, writes configuration information to the system:

```cpp
$SetAppThreadCount(4)
int main(int argc, char* argv[]) {
    IApplication app(argc, argv);
    return app.run();
}
```

When you need to reference this configuration information, it's equally simple:

```cpp
int IAsioApplication::run()
{
    detail::SignalHandler signal_handler;

    if(!m_threadCount){
        auto defaultCount = std::thread::hardware_concurrency() * 2;
        $ContextInt count{"/system/threadCount", defaultCount};
        m_threadCount = *count;
    }
    IAsioContext::instance().run(m_threadCount);

    return 0;
}
```

On line 7, we use the `$ContextInt` type to construct an object. The first parameter is the location of the configuration information, and the second is the default value.

During execution, the `count` object will look up a JSON value at the JSON Pointer location `/system/threadCount`. If found, it automatically converts it to an integer and assigns it to `count`. If not found, it uses the default value.

Let's explain the contents step by step below.

## Configuration Types

In ICore, configuration information is divided into two categories:

- Context configuration
- Profile configuration

Context configuration is systemic and effective before the program fully starts. For example, setting whether to start tests, whether to disable a specific task, or setting the number of threads to run the program.

Profile configuration is a constraint on functionality after the program fully starts. For example, if I start an HTTP server, the maximum length of received HTTP information and header information depends on profile configuration. Or, if I start an `IHttpPythonTest`, its working directory depends on profile configuration.

Distinguishing between context configuration and profile configuration clearly separates framework configurations from specific functional configurations. Users will primarily use context configuration during operations without modifying it, while profile configuration will be defined by users based on their needs and referenced accordingly.

## Referencing Configuration

Whether it's profile or context configuration, the container for storing configuration is of type `IJson`. Users add fields to the `IJson` type when adding configuration. When retrieving configuration, the system attempts to query the `IJson` object. If the query succeeds, it tries to convert the object to the type the user expects. If the conversion is successful, the user finds the configuration in the `IJson` object. If the query fails, the object stores information about the failure and attempts to use the provided default value. If no default value is provided, it constructs an object using the default constructor.

### Referencing Profile Configuration

Profile defines a class for obtaining references:

```cpp
template<typename T>
class IProfileImport : public IConfigImportInterface<T>
{
public:
    IProfileImport(std::string path);
    IProfileImport(std::string path, T value);

public:
    IProfileImport& operator =(const T& value) = delete;

protected:
    virtual IConfigManageInterface& getConfigManage() const final;
};
```

Users can pass a `std::string` type `path` to retrieve data. The path type is JSON Pointer from the nlohmann/json library. Users can also provide a default value for `IProfileImport`. If the configuration query fails, the default value can be used.

The JSON Pointer in the nlohmann/json library provides a concise way to locate and manipulate specific nodes in JSON data. Using path strings like `/foo/bar/0` (following RFC 6901 standard), users can directly access nested structures, such as retrieving the first element `42` from `{"foo": {"bar": [42, 43]}}`. Special characters like `/` and `~` must be escaped as `~1` and `~0`. After constructing the path with `json_pointer`, users can access data using `at()` or `operator[]`. If the path is invalid, a `out_of_range` exception is thrown. This simplifies reading and writing deeply nested data while adhering to the standard.

Therefore, users must ensure their paths comply with the RFC 6901 standard.

Here's an example using profile configuration:

```cpp
IProfileImport<int> port{"/http/port", 8088};
server.setPort(*port);
```

Note that when using `port`, users must use the dereference operator `*` to access the actual value stored internally.

#### Simple Tags

The code above can be cumbersome. To simplify accessing the desired configuration information, we redefine `IProfileImport`, as follows:

```cpp
template<typename T>
using $Profile = IProfileImport<T>;

template<typename T>
using $ProfileMap = IProfileImport<std::map<std::string, T>>;

using $ProfileIJson = $Profile<IJson>;
using $ProfileBool = $Profile<bool>;
using $ProfileChar = $Profile<char>;
using $ProfileUChar = $Profile<uchar>;
using $ProfileSChar = $Profile<signed char>;
using $ProfileShort = $Profile<short>;
using $ProfileUShort = $Profile<ushort>;
using $ProfileInt = $Profile<int>;
using $ProfileUInt = $Profile<uint>;
using $ProfileLong = $Profile<long>;
using $ProfileULong = $Profile<qulonglong>;
using $ProfileLongLong = $Profile<long long>;
using $ProfileULongLong = $Profile<qulonglong>;
using $ProfileFloat = $Profile<float>;
using $ProfileDouble = $Profile<double>;
using $ProfileLongDouble = $Profile<long double>;

using $ProfileMapStdString = $ProfileMap<std::string>;
using $ProfileQString = $Profile<QString>;
using $ProfileStdString = $Profile<std::string>;
using $ProfileQStringList = $Profile<QStringList>;

using $IJson = $ProfileIJson;
using $Bool = $ProfileBool;
using $Char = $ProfileChar;
using $UChar = $ProfileUChar;
using $SChar = $ProfileSChar;
using $Short = $ProfileShort;
using $UShort = $ProfileUShort;
using $Int = $ProfileInt;
using $UInt = $ProfileUInt;
using $Long = $ProfileLong;
using $ULong = $ProfileULong;
using $LongLong = $ProfileLongLong;
using $ULongLong = $ProfileULongLong;
using $Float = $ProfileFloat;
using $Double = $ProfileDouble;
using $LongDouble = $ProfileLongDouble;

using $MapStdString = $ProfileMapStdString;
using $QString = $ProfileQString;
using $StdString = $ProfileStdString;
using $QStringList = $ProfileQStringList;
```

In the code above, we list all types that might be used. The definition is straightforward—just prepend a `$` to the type name in uppercase.

With the code above, the following can be used instead:

```cpp
$Int port{"/http/port", 8088};
server.setPort(*port);
```

This makes the configuration more concise and easier to understand.

#### Query Exceptions

In the code above, if a query exception occurs—for example, if there is no data corresponding to the JSON Pointer `/http/port` in the `IJson` object, or if the data at `/http/port` is a string and cannot be converted to an integer, or if the conversion to an integer exceeds the integer type's range—how can this be determined?

For `IProfileImport` objects, there are three possible states for the result:

- **InitializedValue**: This state indicates that the query or conversion of the JSON value failed, and no default value was provided by the user. The configuration object then stores a default value. Correspondingly, `$Bool` is `false`, `$Int` is `0`, and `$QString` is an empty string.

  Users can use the function `bool isInitializedValue() const;` to check if the current value is an initialized value.

- **DefaultValue**: If the user provides a default value when constructing the `IProfileImport` object, this state is used if the JSON query or conversion fails.

  Users can use `bool isDefaultedValue() const;` to check if the value is a default.

- **LoadedValue**: If the JSON query and conversion are successful, `IProfileImport` changes to the `LoadedValue` state.

  Users can use `bool isLoadedValue() const` to check if the current value is loaded.

#### Using Configuration Values

For an `IProfileImport` object, users can use the value in two ways:

1. Dereference the object to get the value.
2. Use the `value()` function to get the value.

Here's an example:

```cpp
$Int port{"/http/port", 8088};

// Method 1
//server.setPort(*port);

// Method 2
server.setPort(port.value());
```

### Referencing Context Configuration

#### Redefining Context

The redefinition of context is as follows:

```cpp
template<typename T>
using $Context = IContextImport<T>;

template<typename T>
using $ContextMap = IContextImport<std::map<std::string, T>>;

using $ContextJson = $Context<IJson>;
using $ContextBool = $Context<bool>;
using $ContextChar = $Context<char>;
using $ContextUChar = $Context<uchar>;
using $ContextSChar = $Context<signed char>;
using $ContextShort = $Context<short>;
using $ContextUShort = $Context<ushort>;
using $ContextInt = $Context<int>;
using $ContextUInt = $Context<uint>;
using $ContextLong = $Context<long>;
using $ContextULong = $Context<qulonglong>;
using $ContextLongLong = $Context<long long>;
using $ContextULongLong = $Context<qulonglong>;
using $ContextFloat = $Context<float>;
using $ContextDouble = $Context<double>;
using $ContextLongDouble = $Context<long double>;

using $ContextMapStdString = $ContextMap<std::string>;
using $ContextQString = $Context<QString>;
using $ContextStdString = $Context<std::string>;
using $ContextQStringList = $Context<QStringList>;
```

There's no need to redefine `Context` characters here; instead, add the string `Context` between `$` and the type. Since context configuration queries are not as common or developer-oriented as profile queries, shorter configuration queries are left for profile configurations.

The operation for querying context configuration is the same as for profile configuration, so it is not repeated here.

## Registering Configuration

### Context Configuration Registration

#### IContextTaskInterface

The foundation for registering context configuration is the `IContextTaskInterface` class, declared as follows:

```cpp
template<typename T, bool enabled = true>
class IContextTaskInterface : public ITaskWareUnit<T, IConfigTaskCatagory, enabled>, public ISoloUnit<T>
{
public:
    IContextTaskInterface() = default;

public:
    virtual IJson config() = 0;
    virtual std::string path() const;

protected:
    virtual void $task() final;
};
```

By inheriting this class, users can register their own configuration in the context configuration.

The `config()` function returns the configuration information.

### Profile Configuration Registration

[Note: The content for "Profile Configuration Registration" is not provided in the source text.]