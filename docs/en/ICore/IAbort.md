<译文内容>  
# IAbort Module Documentation  

## Module Overview  

During the development of IWebCore, user code is task-based and modular. The code written by developers represents individual functional points within the entire codebase, which are encapsulated into individual tasks (Task). Initialization of all these tasks occurs at the beginning of the project's execution. Once all tasks have been initialized, the program starts providing services. Therefore, for IWebCore, users can perform preliminary logic checks during task execution. If the code adheres to certain logical conditions, it can continue executing. If it does not meet the logical conditions, the task will fail directly.  

Within IWebCore, IAbort is used to define and invoke qFatal to notify developers of program exceptions. Users define an Abort by inheriting from IAbortInterface. In the Abort, they define the name and information of the error. They also use macros to generate corresponding static member functions for developers to call.  

### The Abort Exception Mechanism  

The Abort module is a **lightweight fatal error handling solution** with the following advantages:  

-   **Immediate Termination**: Directly terminates the program upon triggering an error, preventing the propagation of undefined states.  
-   **Information Aggregation**: Automatically collects key information such as error codes, descriptions, and triggering locations.  
-   **Scalability**: Quickly define new error types using templates and macros, supporting custom error types and descriptions.  
-   **Error Standardization**: Standardizes error information through macros, preventing user input errors.  
-   **Early Runtime Overhead**: Performs checks before the program provides services, without occupying program service time and costs.  
-   **Error Information Collection**: Automatically records error codes, descriptions, and triggering locations.  
-   **Code Location Tracking**: Automatically captures the filename, function name, and line number where the error occurred.  

## IAbortInterface  

### How to Define an Abort  

#### Inheriting from IAbortInterface  

To define their own Abort, users must inherit from the IAbortInterface macro.  

```cpp  
template<typename T>  
class IAbortInterface : public ISoloUnit<T>  
{  
public:  
    IAbortInterface() = default;  

public:  
    void abort(int code, const char* data, const QString& description, ISourceLocation location);  
    void abort(int code, const char* data, ISourceLocation location);  
    virtual QMap<int, QString> abortDescription() const = 0;  
    virtual QString abortComment() { return {}; }  

private:  
    void checkAbortInfoLength();  
};  
```  

IAbortInterface provides a pure virtual function, `abortDescription`, for describing the type of abort. Additionally, the `$AsAbort` macro must be added in the subclass to define the fields and functions of the abort.  

#### `$AsAbort` Macro  

-   **Purpose**: Declares error enumerations and automatically generates corresponding `abortXXX()` methods.  
-   **Syntax**:  

    ```cpp  
    class CustomAbort : public IAbortInterface<CustomAbort> {  
        $AsAbort(Error1, Error2, ...)  // Define error enumerations  
    public:  
        // Must implement abortDescription()  
        QMap<int, QString> abortDescription() const override {  
            return {  
                {Error1, "Description1"},  
                {Error2, "Description2"}  
            };  
        }  
    };  
    ```  

-   **Principle**: After macro expansion, static member methods `abortError1()`, `abortError2()`, etc., are generated, which can be called directly.  
-   **Note**: The `$AsAbort` is followed by parentheses, not curly braces. It is essentially a macro and its parameters.  

#### `description` Implementation  

-   **Responsibility**: Returns a mapping of error codes to descriptions via the `abortDescription()` method. This informs developers why the exception occurred and how to handle the exception information.  
-   **Example**:  

    ```cpp  
    QMap<int, QString> CustomAbort::abortDescription() const {  
        return {  
            {NetworkError, "Network connection failed"},  
            {InvalidInput, "Invalid input format"}  
        };  
    }  
    ```  

-   **Note**: The keys and values in the returned map must correspond one-to-one with the fields defined in `$AsAbort`. The Abort system checks during initialization for missing fields or extra fields. If there is a mismatch, an error will be reported.  

### How to Use Abort  

#### 1. Triggering Predefined Errors (Example using `IGlobalAbort`)  

```cpp  
// Throwing an exception, passing user-provided exception information  
void ISoloUnitDetail::abortError(QString content)  
{  
    IGlobalAbort::abortSingletonInstanceCreateError(content);  
}  

// Throwing an exception, providing location information  
if(m_pathFunValidators.contains(name)){  
    auto info = name + "IHttpManage::registerPathValidator, path validator already registered";  
    IGlobalAbort::abortDuplicatedKey(info, $ISourceLocation);  
}  
```  

Note the use of the parameter `$ISourceLocation` here. This is a macro encapsulating the current file location, function name, and error line information. See the following section for details on `$ISourceLocation`.  

#### 2.2 Custom Error Types  

**Steps**:  

1.  Inherit from the `IAbortInterface` template class:  

    ```cpp  
    class NetworkAbort : public IAbortInterface<NetworkAbort>   
    {  
        $AsAbort(ConnectionTimeout, DNSResolutionFailed)  
    public:  
        QMap<int, QString> abortDescription() const override {  
            return {  
                {ConnectionTimeout, "Connection timeout (no response within 30 seconds)"},  
                {DNSResolutionFailed, "Domain name resolution failed"}  
            };  
        }  
    };  
    ```  

2.  Trigger the error:  

    ```cpp  
    NetworkAbort::abortConnectionTimeout("api.example.com", $ISourceLocation);  
    ```  

Upon triggering the error, the log will be output in the following format:  

```
NAME: [Error Name]  
ABORT: [Error Description]  
ABORT CLASS: [Error Class Name]  
ABORT COMMENT: [Global Comment (Optional)]  
DESCRIPTION: [Custom Description (Optional)]  
SOURCE_LOCATION: FILE [Filename] FUNCTION [Function Name] LINE [Line Number]  
```  

## IGlobalAbort  

### Purpose  

-   **Predefined Global Errors**: Provides a set of common fatal error types covering typical scenarios.  
-   **Direct Usage**: Can be called directly without inheritance, e.g., `IGlobalAbort::abortDuplicatedKey()`.  

### Content  

**Predefined Error Codes and Descriptions**:  

| Error Code (Enumeration)                 | Trigger Scenario Example                           | Description                                     |  
| :--------------------------------------- | :-------------------------------------------------- | :---------------------------------------------- |  
| `UnVisibleMethod`                        | Reflection calling a Qt meta-system hidden method   | "The method is prohibited from being called, but required by Qt meta-system." |  
| `UnReachableCode`                        | Uncovered branch in a Switch-Case statement         | "Code branch that should not be executed."       |  
| `UnimplementedMethod`                    | Calling an unimplemented virtual method             | "Function not yet implemented, expected completion in v2.0." |  
| `SingletonInstanceCreateError`           | Singleton class instantiated multiple times         | "Singleton class prohibits creating multiple instances." |  
| `DuplicatedKey`                          | Attempting to insert a duplicate primary key into the database | "Key 'user_id=1001' already exists."           |  

**Usage Scenario Examples**:  

```cpp  
// Checking instance existence in a singleton class constructor  
if (instanceExists) {  
    IGlobalAbort::abortSingletonInstanceCreateError(  
        "ConfigManager",   
        $ISourceLocation  
    );  
}  
```  

## Source Location  

In C++20, the standard library supports `std::source_location`. The compiler has patched `std::source_location`, which helps users locate code positions effectively. However, since IWebCore uses the C++17 standard, `std::source_location` cannot be used here. Therefore, we have defined our own `ISourceLocation`.  

```cpp  
struct ISourceLocation  
{  
    const char* filename{nullptr};  
    const char* function{nullptr};  
    int line{0};  
};  
```  

And defined the macro `$ISourceLocation` to simulate the initialization of `std::source_location`:  

```cpp  
#define $ISourceLocation ISourceLocation{__FILE__, __FUNCTION__, __LINE__}  
```  

This explains why we use the `$ISourceLocation` macro.  

During the continuous iteration of IWebCore, `$ISourceLocation` will be replaced by `std::source_location`.  

## Best Practices  

1.  **Error Code Naming**: Use `PascalCase` format (e.g., `InvalidRequest`), avoiding magic numbers.  
2.  **Location Tracking**: Always pass the `$ISourceLocation` macro to ensure logs are locatable.  
3.  **Error Description**: Provide clear solution suggestions in `abortDescription()` (e.g., "Please check your network configuration").  

Through this module, developers can quickly implement **high-maintainability** fatal error management, particularly suitable for framework development and scenarios requiring high reliability.