# IApplication 用户文档


## 快速入门

### 创建应用实例

为了快速了解IApplication，我们以实例入手，写一个最简单的例子：

```c++
#include "core/application/IApplication.h" // 引入头文件

int main(int argc, char* argv[]) {
    IApplication app(argc, argv); // 初始化应用实例
    return app.run();             // 启动事件循环
}
```

**说明**：

- 构造函数自动解析命令行参数，初始化 ASIO 上下文。
- `run()` 启动事件循环，阻塞直到应用退出（如收到 `Ctrl+C`）。

在上述代码运行的时候，console 输出如下：

```
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
 
```

在 console 中输出了 IWebCore 的变体内容。

### 添加详细的任务输出

我们将代码添加一句，如下：

```cpp
#include "core/application/IApplication.h"

$EnableTaskOutput(true)
int main(int argc, char* argv[]) {
    IApplication app(argc, argv); // 初始化应用实例
    return app.run();             // 启动事件循环
}
```

`$EnableTaskOutput(true)` 这是一句宏注解，关于宏注解的内容，可以参考具体的文档。当添加这一句话之后，在console中输出如下：

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

上述内容多出来的是任务信息，这个都是在 ICore 中默认注册的任务。 平时他是不显示的，但如果有`$EnableTaskOutput(true)`这一句宏注解的话，这些任务信息都被输出出来。

所以用户可以理解，为什么我们没有添加任何的输出语句，而且 IApplication 中也没有输出 IWebCore 的相关代码，但是这个信息却被输出出来。就是因为`IWebCore::IBannerTask` 被注册到系统当中，在任务执行的时候执行了出来。

关于宏注解和 任务，我我们接下来会深入的讲解.



## 关于 IApplication

### 为什么要有 Application

在很多的程序中，都有 Application 的概念，Application 在程序一开始启动，以 exec() 或者 run() 开启事件循环，防止程序意外退出。在事件循环之前，Application 同样会初始化整个程序必要的运行环境。

 ICore 中的程序也是一样， 是应用程序的核心框架，提供以下核心能力：

- **初始化流程规范化**：自动解析命令行参数（`argc, argv`）、加载基础配置（如线程数、单元测试开关）、创建 Qt 环境兼容层（`QCoreApplication`）。
- **异步任务调度** 基于 ASIO 的事件驱动模型实现高并发处理
- **资源集中管理**：通过单例模式（`IAsioContext`、`ITaskManage`）保证 ASIO 上下文、定时器、异步任务等核心资源全局唯一，避免重复创建和资源泄漏。
- **跨平台支持**：封装 Windows 的 `Ctrl+C` 信号和 Linux 的 `SIGINT/SIGTERM` 处理逻辑，提供统一的优雅退出机制。
- **基础设施集成**：提供定时器、配置管理、单元测试等开箱即用的组件
- **提供事件循环**: 通过 asio 的事件循环来防止程序退出，并提供一些异步执行功能。

### IAsioApplication

在 ICore 中，我们将 IAsioApplication 命名为 IApplication。

ASIO 实现的核心应用类，继承自 `IApplicationInterface`，提供完整的事件循环能力。如下是他的声明

```c++
class IAsioApplication : public IApplicationInterface<IAsioApplication> {
public:
    IAsioApplication(int argc, char** argv); // 构造时自动初始化 ASIO 上下文
    void setThreadCount(int threadCount);     // 设置事件循环线程数
    virtual int run() final;                  // 启动事件循环
};
```

### IApplicationInterface

应用程序接口模板类，定义基础框架规范，如下是他的声明：

```c++
template<typename T>
class IApplicationInterface {
public:
    static T& instance();           // 获取单例实例
    static QString applicationPath(); // 获取应用执行路径
    static const QStringList& arguments(); // 获取启动参数
    static int64_t time();          // 获取非精确时间戳（纳秒级，每秒更新）
    virtual int run() = 0;          // 纯虚函数，需子类实现
};
```



## 功能

### 运行注册任务（Task）

在IApplication 中，最重要的一个目的就是运行已经注册到程序当中的任务，这些任务是程序运行的主体，提供一个个功能点, 如我们上述 IBannerTask， 他的功能就是 输出 IWebCore信息到 console 当中。 具体的内容可以参考 **Task** 相关的文档. 而运行这个任务的方式也很简单,在 run 函数中调用如下的代码:

```c++
template<typename T>
void IApplicationInterface<T>::init()
{
    m_instance = dynamic_cast<T*>(this);
    return ITaskManage::run();
}
```

通过上述的第五行代码,用户注册的功能,就可以在框架中调用. 比如用户注册了一个数据库,那么这个数据库就会在这里被初始化; 用户注册了一个Controller 对象, Controller对象也会在这里被挂载掉 ControllerMapping 中去,在后续会被 Http 请求查询,调用; 用户注册了一个 Bean, 那么 这个Bean 就可以在之后被用于 json 的自动相互的转换；系统注册了一个 IBannerTask, 在 Console中就会输出 IWebCore 字样的内容。



### 提供基于 Asio 的事件循环

ICore 的 IApplication 在一开始是基于 QCoreApplication, Qt 提供事件循环。在后来的开发过程中，逐渐替换成基于 asio 的事件循环。这样可以提供更为强劲的多核事件循环机制，并且变得更加通用。

如果用户有基于 Qt 事件循环或者其他任意类型的事件循环的需要，可以自行实现自己的 IApplication。

在 ICore中，asio 事件循环被封装在 IAsioContext 中，在 IAsioApplication 中，这样调用 asio 的事件循环：

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

在第3行，我们添加事件响应机制，可以通过 `ctrl c` 退出程序。在5-8行，计算出一个合适的 线程数量。在第9行，则开始事件循环。这个时候，就可以像用户提供相应的，注册在 程序中的服务了。

#### 线程数量

在程序中，如果用户没有设置线程数量，则默认线程数 = `std::thread::hardware_concurrency() * 2` ,硬件支持线程数的2倍。用户设定线程数量可以通过如下的方式：

```c++
#include "core/application/IApplication.h"

$SetAppThreadCount(5)
int main(int argc, char* argv[]) {
    IApplication app(argc, argv); 
    app.setThreadCount(4);
    return app.run(); 
}
```

这里展示两种线程的设置方式。在第三行，我们通过宏注解的方式设置线程数：`$SetAppThreadCount(5)` 在第6行，通过代码的方式设置线程数     `app.setThreadCount(4);`  最终，这里代码的优先级更高一些，线程被设置为4个。

此外，用户可以通过配置的方式设置具体的线程数量。关于配置，请参考 `Config` 模块。



### 参数和 软件路径

ICore 自动解析命令行参数，用户可以通过 arguments 来获取用户输入了什么参数， 如下：

```c++
// 获取参数列表
QStringList args = IApplication::arguments();
// 示例输出: ["/path/to/app", "--debug", "input.txt"]
```

ICore 同样也提供了一个applicationPath 告知用户当前的 exe 路径。

### 提供非精确时间戳

在c++中，对于高性能程序而言，时间的获取是一个昂贵的操作。但是程序往往需要的不是一个精确的，具体的时间，而是一个大致的，相对的时间。这里大致时间的概念是，这个时间精确到一个地步，比如精确到秒，这个单位就行, 相对的时间的概念则是，我每一次获取的时间必须是不同的，后一次获取的时间必须比前一次获取的时间晚一点。

ICore 的application 中提供了这样的时间。它是一个 64位 atomic整型的数据，一个数字表示1纳秒， 时间是相对于 epoch 时间，也就是这个数字是相对于 1970年1月1日0时整 过去了多少纳秒的时间。这个时间数据每秒自动更新一次。当用户每次请求他的时候，他在原本数字的基础上加 1，返回给用户。

所以这里为什么用纳秒，就是因为我判断，没有什么程序能够在1s 中请求1000,000, 000 次 （这个数据时10亿， 10的9次方），如果真的有了，这个需求就不是 ICore所能处理的需求，这个也不在我的考虑范围中了。

这个时间可以通过 `IApplication::time()` 函数来获取，它适合日志时间戳等非高精度需求。



## 其他内容

### IAsioContext

IAsioContext 的部分声明如下：

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

在这个函数中，我们可以看到 第6行，提供一个异步发布任务的功能。

在第7行，可以启动一个 定时器，得到一个句柄。

在第8行可以根据这个句柄来停止这个timer。

为什么是 `std::ptrdiff_t` 类型呢？这个是因为我们本质上是 new 了一个对象，将对象地址转换为  `std::ptrdiff_t` 类型返回的。stopTimer 中也是将这个 `std::ptrdiff_t` 重新转换为指针再进行后续的操作的。

他的示例如下：

```c++
auto timerId = IAsioContext::startTimer(1000ms, [](){
    std::cout << "每秒触发" << std::endl;
});
// 停止定时器
IAsioContext::stopTimer(timerId);
```

