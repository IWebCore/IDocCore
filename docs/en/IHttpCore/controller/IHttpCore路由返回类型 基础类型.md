# IHttpCore Routing Return Type Basic Types

The IHttpCore Controller provides an extremely rich set of function return types. Through these return types, users can return any content they wish to the client. Users do not need to go through cumbersome steps to write content item by item; instead, by using our series of return types, they can save a significant amount of coding work.

Additionally, users can customize return types to meet business requirements.

---

## Qt Return Type Reflection

In Qt, if a class is marked with `Q_GADGET`, the class will be scanned by the `MOC` tool during compilation to generate a series of metadata, which is stored in a `moc_xxx.cpp` file. We can retrieve this scanned information through the class's static `staticMetaObject()` function.

If a function in the reflection class is marked with `Q_INVOKABLE`, then the function's name, return type, parameter types, parameter names, and invocation method will be recorded. In this document, we focus on the return value type name and return value type ID from the metadata.

When we know the return value type's name and ID, we can process these return values and convert them into the desired content. In the IHttpCore framework, the returned object is processed into an HTTP response. This is why we can achieve routing returns of different types.

---

## String Type

The string return type returns a string, using UTF-8 encoding uniformly. The default return status is `200 OK`, and the default `Content-Type` is `text/plain; charset=UTF-8`. If you want to return a different HTTP status or modify the return type, consider using `IPlainTextResponse`.

### QString

`QString` is the most commonly used return type and is also the default supported type in Qt. Example code is as follows:

```c++
$GetMapping(qstring)
QString qstring()
{
    return "QString";
}
```

### std::string

`std::string` is a type supported by the C++ standard library. Example code is as follows:

```c++
$GetMapping(stdString)
std::string stdString()
{
    return "stdString";
}
```

Note: Here, you must use `std::string` and cannot omit the `std::` prefix by using `using namespace std;`. This is invalid.

```c++
using namespace std; // Importing the std namespace

$GetMapping(stringFun)
string stringFun()
{
    return "string";
}
```

The above code compiles successfully but will throw an error at runtime, informing the developer that the `string` type cannot be resolved. Therefore, `std::string` is a valid type for return values, while `string` is invalid.

### IString

The `IString` type is a string type defined in the framework, aimed at reducing the copying of string types and improving software efficiency. For more details, refer to the `core/IString` documentation. Its usage is identical to `QString` and `std::string`. Below is an example of its usage:

```c++
$GetMapping(istring)
IString istring()
{
    return "IString";
}
```

### QByteArray

The `QByteArray` type returns a `Content-Type` of `application/octet-stream`, indicating that this type is not text-based but a character stream. Therefore, if you need to explicitly return a string, you cannot use `QByteArray`. However, in some special scenarios, `QByteArray` is an excellent choice. The example is as follows:

```c++
$GetMapping(qbytearray)
QByteArray qbytearray()
{
    return "IStringView";
}
```

---

## Numeric Types

IHttpCore supports returning numeric types. The returned value will be converted to a string and sent to the client. The return status is `200 OK`, and the `Content-Type` is `text/plain`.

### Native Numeric Types

The native numeric types include the following:

- short, ushort, unsigned short
- int, uint, unsigned int
- long, ulong, unsigned long
- long long, qlonglong, qulonglong, unsigned long long
- float, double

Example code is as follows:

```c++
$GetMapping(uintVal)
uint uintVal(){
    return std::numeric_limits<uint>::max();
}

$GetMapping(unsignedlonglongVal)
unsigned long long unsignedlonglongVal(){
    return std::numeric_limits<unsigned long long>::max();
}
```

Note: In the above types, such as `ushort` and `unsigned short`, they represent the same type. However, `unsigned short` is the standard C++ type name, while `ushort` is a redefined type name in `qglobal.h`. Both can be used as return types. The same applies to other type names.

Also, note that in C++ standards, `signed short` can be written. However, this is not supported in our return types. You cannot write code like the following:

```c++
$GetMapping(hello)
signed short hello();
```

This could be supported easily, but it is unnecessary. No one would intentionally use such a type. Therefore, types like `signed short` are invalid in IHttpCore. If users use such types, the program will throw an error during initialization.

Another point users should be aware of is the issue of type length. For example, the `int` type has varying lengths in different environments, from 16-bit to 64-bit. Users need to determine the range of the returned value and ensure it matches the size supported by the return type. If used incorrectly, this can lead to data corruption and forced type conversion issues. For this, the following approach can be referenced.

### std::int Types

C standards support types like `int16_t`, and C++ standards further encapsulate them with `std::int16_t`. These indicate that the data length is 16 bits. All IHttpCore-supported data types are as follows:

- int16_t, std::int16_t, uint16_t, std::uint16_t
- int32_t, std::int32_t, uint32_t, std::uint32_t
- int64_t, std::int64_t, uint64_t, std::uint64_t

Users can use these types with precise bit lengths to return a numeric value, avoiding issues like forced type conversion. Example code is as follows:

```c++
$GetMapping(stdUInt32_t)
std::uint32_t stdUInt32_t(){
    return std::numeric_limits<std::uint32_t>::max();
}

$GetMapping(stdUInt64_t)
std::uint64_t stdUInt64_t(){
    return std::numeric_limits<std::uint64_t>::max();
}
```

### char-Related Types

The types above lack a category of types with a length of 8 bits. They can be named as follows:

- char, signed char, schar, unsigned char, uchar
- int8_t, std::int8_t, uint8_t, std::uint8_t

Currently, these types are not supported as return values and will be supported in the future. The reason for the delay is that the author hesitated; adding these types is simple, but the author hasn't done it yet.

Note: In general, the `char` type is used to represent a character. Therefore, if the type is `char`, it indicates that the developer wants to return a single character. Other signed types and types like `int8_t` represent `numeric types` and return the corresponding numerical value.

If users want to return a character, they should convert it into a string of length one. If they want to return a numerical value, use larger types like `short`.

---

## HTTP Response Status

If users simply want the server to respond with a status without any additional information, they can set the return type to `IHttpStatus` or directly use `int`.

However, this is not a common requirement. Users are better off returning an `IStatusResponse` type.

### IHttpStatus

For an introduction to `IHttpStatus`, refer to the `IHttpCore status` documentation. Its usage is as follows:

```c++
$GetMapping(httpStatus)
IHttpStatus httpStatus()
{
    return IHttpStatus::ACCEPTED_202;
}
```

Its response status is `202`, and the response content is empty.

---

## Composite Structures

In C++, composite types refer to types formed by combining basic data types. Composite types include pointers, references, arrays, structs, unions, and classes. These types allow developers to build more complex data structures to meet various programming needs.

In the IHttpCore framework, we can directly return composite structure types, and during the request-response process, these composite types will be converted into JSON data and returned to the client.

### Bean

In IHttpCore, we introduce the concept of Bean. A Bean is a specific struct that can be converted into and out of JSON. For more information about Beans, refer to the `core/bean` documentation.

During actual application use, Bean types will be further encapsulated into database tables (Table) and views (View). This allows users to directly query Bean data from the database and return it to the client. For details, refer to the `IRdbCore` documentation.

#### Defining a Bean

The Bean we define is as follows:

> MyBean.h

```c++
#pragma once

#include "core/bean/IBeanInterface.h"

class MyBean : public IBeanInterface<MyBean>
{
    Q_GADGET
public:
    MyBean() = default;
    MyBean(int id, QString name){
        this->index = id;
        this->name = name;
    }

    $BeanField(int, index, 100)
    $BeanField(QString, name, "yuekeyuan")
};
```

The above Bean inherits from `IBeanInterface`, contains two fields—an `int` field `index` with a default value of `100`, and a `QString` field `name` with a default value of `"yuekeyuan"`.

#### Bean Type

Next, write a return object of the Bean type:

```c++
$GetMapping(getBean)
MyBean getBean(){
    return {};
}
```

The test case is as follows:

```c++
def test_bean():
    val = requests.get(serverAddress + "/ReturnTypeController/getBean")
    assert val.status_code == 200
    assert val.json() == {"index":100,"name":"yuekeyuan"}
    assert val.headers["Content-Type"]  == "application/json; charset=UTF-8"
    print(val.text)
    print(val.headers)
```

In the above, we directly return the default data of the `MyBean` type. The test case passes. As seen in the test, the return type is `application/json; charset=UTF-8`, the status is `200 OK`, and the content is `{"index":100,"name":"yuekeyuan"}`.

This type of return value avoids developers having to manually perform type conversions, saving time and effort.

#### Bean Sequence Containers

Based on the Bean defined by users, we can wrap Bean types in sequence containers to return sequences of Bean types.

The IHttpCore framework supports the following sequence container types:

- QList
- std::list
- QVector
- std::vector

| **Category** | **Qt Type** | **Standard Library Type** |
|--------------|-------------|---------------------------|
| **Linked List** | QList<Bean> | std::list<Bean> |
| **Dynamic Array** | QVector<Bean> | std::vector<Bean> |

These four container types are supported because we develop on the Qt system, supporting both Qt's container types and standard library container types. Their usage is as follows:

```c++
$GetMapping(getBeanQList)
QList<MyBean> getBeanQList()
{
    return QList<MyBean>{
        MyBean{1, "hello"},
        MyBean{2, "world"}
    };
}

$GetMapping(getBeanStdList)
std::list<MyBean> getBeanStdList()
{
    return std::list<MyBean>{
        MyBean{1, "hello"},
        MyBean{2, "world"}
    };
}
```

The usage for `QVector` and `std::vector` is consistent and will not be listed separately.

The above requests return a status of `200 OK` and a content type of `application/json; charset=UTF-8`. The content is `[{"index":1,"name":"hello"},{"index":2,"name":"world"}]`, which is a JSON array with correct content.

Note: These aliases must be written exactly as shown in the table. If they are inconsistent, the code will not compile, but during runtime, due to reasons related to Qt reflection, the framework will report an error to the user.

#### Bean Associative Containers

IHttpCore currently supports two types of associative containers: `QMap` and `std::map`. The current key types for these containers can be `QString`, `std::string`, or `IString`. Therefore, a Bean type can be specialized into six types of associative containers.

| **Container** | **Key Type: QString** | **Key Type: std::string** | **Key Type: IString** |
|---------------|------------------------|---------------------------|------------------------|
| **QMap** | QMap<QString, Bean> | QMap<std::string, Bean> | QMap<IString, Bean> |
| **std::map** | std::map<QString, Bean> | std::map<std::string, Bean> | std::map<IString, Bean> |

Examples are provided below:

```c++
$GetMapping(getBeanQMapQstring)
QMap<QString, MyBean> getBeanQMapQstring()
{
    return QMap<QString, MyBean>{
        {"yue", MyBean{1, "hello"}},
        {"qichu", MyBean{2, "world"}}
    };
}

$GetMapping(getBeanStdStringStdMap)
std::map<std::string, MyBean> getBeanStdStringStdMap()
{
    return std::map<std::string, MyBean>{
        {"yue", MyBean{1, "hello"}},
        {"qichu", MyBean{2, "world"}}
    };
}
```

Note: Here, the type must be a complete type. Aliases defined using `typedef`, `using`, or `#define` cannot be recognized by the IHttpCore framework.

---

### Regular Composite Types

Composite types are not only valid for user-defined Bean types; IHttpCore also supports combinations of regular composite types.

These types include:

- bool
- String types: QString, std::string, IString
- Numeric types: short, ushort, int, uint, long, ulong, float, double, etc.

These types can be combined into composite structures using sequence or associative containers and used as return types in route mapping functions.

#### Sequence Containers

Examples of sequence containers are as follows:

```c++
$GetMapping(intList)
QList<int> intList()
{
    return {1, 2, 4};
}

$GetMapping(intVector)
std::vector<int> intVector()
{
    return {1, 2, 5};
}

$GetMapping(stringList)
std::list<std::string> stringList()
{
    return {"hello", "world", "yuekeyuan"};
}
```

Note: `QStringList` can also be returned by IHttpCore mapping functions.

#### Associative Containers

Similar to Bean associative containers, regular types also support associative containers. Examples are as follows:

```c++
$GetMapping(stdMapstdStringInt)
std::map<std::string, int> stdMapstdStringInt(){
    return std::map<std::string, int>{
        {"hello", 1},
        {"world", 2},
        {"yuekeyuan", 3}
    };
}

$GetMapping(qMapstdStringInt)
QMap<std::string, int> qMapstdStringInt(){
    return QMap<std::string, int>{
        {"hello", 1},
        {"world", 2},
        {"yuekeyuan", 3}
    };
}

$GetMapping(stdMapQStringInt)
std::map<QString, int> stdMapQStringInt(){
    return std::map<QString, int>{
        {"hello", 1},
        {"world", 2},
        {"yuekeyuan", 3}
    };
}

$GetMapping(qMapQStringInt)
QMap<QString, int> qMapQStringInt(){
    return QMap<QString, int>{
        {"hello", 1},
        {"world", 2},
        {"yuekeyuan", 3}
    };
}
```

Note: All type names must not be abbreviated or replaced.

---

## IJson

IHttpCore supports `IJson` as a return value. `IJson` is an alias for the `nolhmann/json` library.

```c++
using IJson = nolhmann::json;
```

We use this alias for consistency with our project code and to simplify operations. Note: Users cannot use `nolhmann/json` or `json` as return value names; they must use `IJson`. Otherwise, runtime errors will occur.

For content about `IJson`, users can refer to [nlohmann/json: JSON for Modern C++](https://github.com/nlohmann/json).

Example:

```c++
$GetMapping(ijson)
IJson ijson(){
    return IJson({"hello", "world"});
}
```

---

## Time Types

IHttpCore supports returning Qt time types to users. During return, the time is converted into a corresponding string and sent to the client.

### QDate

Example for `QDate` as a return type:

```c++
$GetMapping(qDate)
QDate qDate(){
    return QDate(2022,10,12);
}
```

After requesting the above path, the client will receive a return value like `2022-10-12`.

The default format is `yyyy-MM-dd`. If users need additional formats, such as `2022/10/12`, they can customize the configuration in their project to change the value of the `/http/QDateFormat` configuration path to `yyyy/MM/dd`. For configuration options, refer to the `core/config` documentation.

If the returned `QDate` is invalid, a `500 Internal Error` status will be returned.

### QTime

Example for `QTime` as a return type:

```c++
$GetMapping(qTime)
QTime qTime(){
    return QTime(12,12,12);
}
```

The default format for `QTime` is `HH:mm:ss`, so the above path returns the string `12:12:12`. If users need to customize the return format, they can modify the `/http/QTimeFormat` configuration path.

If the returned `QTime` value is invalid, a `500` status will be returned to the client.

### QDateTime

Example for `QDateTime`:

```c++
$GetMapping(qDateTime)
QDateTime qDateTime(){
    return QDateTime(qDate(), qTime());
}
```

The default format for `QDateTime` is `yyyy-MM-ddTHH:mm:ss`. Users can modify the configuration under `/http/QDateTimeFormat` to change the format.

If the returned value is invalid, a `500` status will be returned to the client.