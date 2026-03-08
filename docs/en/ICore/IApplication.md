<译文内容>
# IApplication User Documentation


## Quick Start

### Creating Application Instance

To get started with IApplication, let's create a simple example:

```c++
#include "core/application/IApplication.h" // Include the header file

int main(int argc, char* argv[]) {
    IApplication app(argc, argv); // Initialize the application instance
    return app.run();             // Start the event loop
}
```

**Description**:

- The constructor automatically parses command-line arguments and initializes the ASIO context.
- `run()` starts the event loop, blocking until the application exits (e.g., receiving `Ctrl+C`).

When the above code runs, the console output is as follows:

```
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
 
```

This outputs the IWebCore banner content in the console.

### Adding Detailed Task Output

We add one line to the code as follows:

```cpp
#include "core/application/IApplication.h"

$EnableTaskOutput(true)
int main(int argc, char* argv[]) {
    IApplication app(argc, argv); // Initialize the application instance
    return app.run();             // Start the event loop
}
```

The `$EnableTaskOutput(true)` is a macro annotation. For details on macro annotations, refer to the specific documentation. After adding this line, the console output is as follows:

```
[+] 0   IWebCore::IConfigTaskCatagory
    [√] 1   IWebCore::IHttpDefaultProfileTask
    [√] 99  IWebCore::IProfileLoadJsonTask


[+] 1   IWebCore::IStartupTaskCatagory
    [√] 0   IWebCore::IBannerTask



 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

[+] 2   IWebCore::IInitializationTaskCatagory
    [√] 50  IWebCore::IHttpFileServiceTask
    [√] 50  IWebCore::IHttpPathValidatorsTask


[+] 45  IWebCore::IRdbCatagory


[+] 49  IWebCore::ITcpTaskCatagory


[+] 50  IWebCore::IHttpTaskCatagory
    [√] 1   IWebCore::IHttpCachedSession
    [√] 50  IWebCore::IHttpControllerActionMapping
    [√] 50  IWebCore::IHttpSessionCreateFilter
    [√] 50  IWebCore::IHttpSessionDumpFilter


[+] 99  IWebCore::ITestCatagory


[+] 100 IWebCore::IEndupTaskCatagory
    [√] 1   IWebCore::IUnitTestTask
    [√] 2   IWebCore::IFunctionTestTask
    [√] 3   IWebCore::IIntegrationTestTask
    [√] 50  IWebCore::IHttpPrintTraceTask
    [√] 99  IPubCore::IHttpPythonTest::IHttpPythonTestTask
```

The additional content above is task information, which are all tasks pre-registered by default in ICore. Normally, they are not displayed unless the `$EnableTaskOutput(true)` macro annotation is present. The user can understand why we did not add any output statements and why IApplication does not contain any output related to IWebCore but the information is still outputted because `IWebCore::IBannerTask` is registered in the system and executed during task execution.

For details on macro annotations and tasks, we will delve deeper in the following sections.

## About IApplication

### Why Do We Need an Application

In many programs, the concept of an Application exists. The Application starts the program at the beginning, using exec() or run() to start the event loop, preventing the program from exiting unexpectedly. Before the event loop, the Application also initializes the necessary runtime environment for the entire program.

ICore is no different. It is the core framework of an application, providing the following core capabilities:

- **Standardized Initialization Process**: Automatically parses command-line arguments (`argc, argv`), loads basic configurations (such as thread count, unit test switches), and creates a Qt environment compatibility layer (`QCoreApplication`).
- **Asynchronous Task Scheduling**: Implements high-concurrency processing based on the ASIO event-driven model.
- **Centralized Resource Management**: Ensures the uniqueness of core resources such as ASIO context, timers, and asynchronous tasks through singleton patterns (`IAsioContext`, `ITaskManage`), avoiding duplicate creation and resource leaks.
- **Cross-Platform Support**: Encapsulates the handling of Windows `Ctrl+C` signals and Linux `SIGINT/SIGTERM`, providing a unified graceful exit mechanism.
- **Infrastructure Integration**: Provides ready-to-use components such as timers, configuration management, and unit testing.
- **Event Loop Provision**: Uses asio's event loop to prevent program exit and provides asynchronous execution capabilities.

### IAsioApplication

In ICore, IAsioApplication is named as IApplication.

It is the core application class based on ASIO, inheriting from `IApplicationInterface`, providing complete event loop capabilities. The declaration is as follows:

```c++
class IAsioApplication : public IApplicationInterface<IAsioApplication> {
public:
    IAsioApplication(int argc, char** argv); // Initializes ASIO context during construction
    void setThreadCount(int threadCount);     // Sets the number of event loop threads
    virtual int run() final;                  // Starts the event loop
};
```

### IApplicationInterface

This is a template class defining the basic framework specifications. The declaration is as follows:

```c++
template<typename T>
class IApplicationInterface {
public:
    static T& instance();           // Gets the singleton instance
    static QString applicationPath(); // Gets the application execution path
    static const QStringList& arguments(); // Gets the startup parameters
    static int64_t time();          // Gets a non-precise timestamp (nanosecond precision, updates every second)
    virtual int run() = 0;          // Pure virtual function, must be implemented by derived classes
};
```

## Features

### Run Registered Tasks

The primary purpose of IApplication is to run tasks that have been registered in the program. These tasks are the main body of the program, providing individual functionality points, such as the IBannerTask mentioned above, which outputs IWebCore information to the console. For specific details, refer to the **Task** documentation. The way to run these tasks is simple: call the following code in the run function:

```c++
template<typename T>
void IApplicationInterface<T>::init()
{
    m_instance = dynamic_cast<T*>(this);
    return ITaskManage::run();
}
```

Through the fifth line of the above code, any functionality registered by the user can be invoked within the framework. For example, if a database is registered by the user, it will be initialized here; if a Controller object is registered, it will be mounted into the ControllerMapping for subsequent querying and invocation by HTTP requests; if a Bean is registered, it can be used for automatic JSON conversion; if a system task like IBannerTask is registered, the IWebCore banner will be outputted in the console.

### Provide Asio-Based Event Loop

ICore's IApplication initially used QCoreApplication, which is provided by Qt for the event loop. During development, it gradually transitioned to an asio-based event loop. This provides a more robust multi-core event loop mechanism and is more universal.

If the user needs a Qt event loop or any other type of event loop, they can implement their own IApplication.

In ICore, the asio event loop is encapsulated in IAsioContext. In IAsioApplication, the asio event loop is invoked as follows:

```c++
int IAsioApplication::run()
{
    detail::SignalHandler signal_handler;

    if(!m_threadCount){
        $ContextInt count{"/system/threadCount", static_cast<int>(std::thread::hardware_concurrency() * 2)};
        m_threadCount = *count;
    }
    IAsioContext::instance().run(m_threadCount);
     return 0;
}
```

On line 3, we add a signal handler to allow program exit via `ctrl c`. Lines 5-8 calculate an appropriate number of threads. On line 9, the event loop begins, and services registered in the program can now be provided.

#### Thread Count

If the user does not set the thread count, the default is `std::thread::hardware_concurrency() * 2`, which is twice the number of hardware-supported threads. The user can set the thread count using the following methods:

```c++
#include "core/application/IApplication.h"

$SetAppThreadCount(5)
int main(int argc, char* argv[]) {
    IApplication app(argc, argv); 
    app.setThreadCount(4);
    return app.run(); 
}
```

This example shows two ways to set thread count. On line 3, the thread count is set via a macro annotation: `$SetAppThreadCount(5)`. On line 6, the thread count is set programmatically: `app.setThreadCount(4);`. The programmatically set value has higher priority, so the thread count is set to 4.

Additionally, the user can set the thread count via configuration. For details on configuration, refer to the `Config` module.

### Parameters and Application Path

ICore automatically parses command-line arguments. The user can retrieve the input parameters using arguments, as follows:

```c++
// Get the list of arguments
QStringList args = IApplication::arguments();
// Example output: ["/path/to/app", "--debug", "input.txt"]
```

ICore also provides an applicationPath to inform the user of the current executable path.

### Provide Non-Precise Timestamp

For high-performance C++ programs, obtaining time is an expensive operation. However, programs often do not need precise time but rather a relative, approximate time. The concept of approximate time means the time is accurate to a certain granularity (e.g., seconds). The concept of relative time means that each retrieval must return a different time, and the time must be later than the previous one.

ICore's application provides such a timestamp. It is a 64-bit atomic integer, where a number represents 1 nanosecond. The time is relative to the epoch (January 1, 1970). This timestamp updates automatically every second. Each time the user requests it, the number increments by 1 and is returned.

The reason for using nanoseconds is that no program is expected to request 1 billion times per second (10^9 requests per second). If such a requirement exists, it is beyond the scope of ICore.

This timestamp can be obtained via `IApplication::time()`, suitable for non-high-precision needs such as logging timestamps.

## Other Content

### IAsioContext

A partial declaration of IAsioContext is as follows:

```c++
class IAsioContext : public ISoloUnit<IAsioContext>
{
public:
    using Task = std::function<void()>;
public:
    static void post(Task);
    static std::ptrdiff_t startTimer(std::chrono::milliseconds duration, Task);
    static void stopTimer(std::ptrdiff_t ptr);
};
```

In this function, note the following:

- Line 6 provides an asynchronous task posting capability.
- Line 7 starts a timer and returns a handle.
- Line 8 stops the timer using the handle.

The reason for using `std::ptrdiff_t` is that we essentially create an object, convert its address to `std::ptrdiff_t`, and return it. The `stopTimer` function reconverts the `std::ptrdiff_t` back to a pointer for subsequent operations.

The example is as follows:

```c++
auto timerId = IAsioContext::startTimer(1000ms, [](){
    std::cout << "每秒触发" << std::endl;
});
// Stop the timer
IAsioContext::stopTimer(timerId);