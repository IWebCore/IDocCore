# 使用示例3: IHttp动态路由

> 本篇文档描述如何使用 IHttp 的动态路由功能。

在前两篇文档中，我们分别集成了 nlohmann/json 库和实现了静态文件服务。本篇文档将展示如何使用 IHttp 的动态路由功能，通过路径参数捕获和参数验证来实现灵活的 URL 路由。

## 配置依赖库

这次我们创建的是 cmake 的项目，而不是 qmake 的项目。

首先我们创建一个 IMakeCore 支持的项目，项目名称是 dynamicMapping_demo，通过 `ipc init` 添加 IMakeCore 支持。

### CMakeLists.txt

该项目的 CMakeLists.txt 文件内容如下。

```cmake
cmake_minimum_required(VERSION 3.16)

project(dynamicMapping_demo LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core)

add_executable(dynamicMapping_demo
  main.cpp
  IndexController.h IndexController.cpp
)
target_compile_definitions(dynamicMapping_demo PRIVATE _WIN32_WINNT=0x0601)
target_link_libraries(dynamicMapping_demo Qt${QT_VERSION_MAJOR}::Core)
target_link_libraries(dynamicMapping_demo ws2_32 mswsock)

include($ENV{ICMakeCore})
ICMakeCoreInit(dynamicMapping_demo)
```

这个文件相对于原始的文件，修改如下：

- 添加了 `_WIN32_WINNT` 这个宏的支持。如果没有这个宏，在 mingw 编译器下 asio 会报 warning 异常。
- 添加了 `ws2_32` 和 `mswsock` 这两个库的支持。
  - 这两个库在编译的时候，如果是 msvc 编译器的情况下是不需要的，但是对于 mingw 和 llvm 编译器，这两个库是必须填写上的。
- 添加了 IMakeCore 支持，也就是最后两行的代码。

另外，我们添加了 main.cpp 文件，和 IndexController 这个类。IndexController 就是我们今天要处理主要逻辑的类。



### packages.json 配置

在项目上执行 cmake 之后，会创建 packages.json 文件，现在我们要添加一些库到这个文件夹里面。

修改 packages.json 文件如下：

```json
{
    "packages":{
        "ICore" : "1.1.0",
        "nlohmann.json" : "3.12.0",
        "asio" : "1.30.2",
        "ITcp" : "1.0.0",
        "IHttp" : "1.0.0"
    }
}
```

在这个 packages.json 中，我们添加了五个库他们依次是：

- ICore
  - 这个库是 IWebCore 框架的基础，它支持反射，配置，运行时等一系列的内容。
- nlohmann.json
  - nlohmann.json 是 IWebCore 项目中所选择的 json 库，相对于其他的库，这个库兼顾了性能和可用性。
- asio
  - 基础网络库。
- ITcp
  - 在 asio 的基础之上做了一层封装，用于管理 tcp 内容。
- IHttp 
  - http 服务包。



这里我们没有再添加 IHttp.assets 这个库，因为这个项目不再使用静态文件服务。



## main.cpp 文件的编写

创建 main.cpp 文件：

```cpp
#include <core/application/IApplication.h>
#include <http/IHttpServer.h>
#include <http/IHttpAnnomacro.h>

$EnableHttpPrintTrace(true)
int main(int argc, char *argv[])
{
    IApplication a(argc, argv);

    IHttpServer server;
    server.listen();

    return a.exec();
}
```

在这个文件中，我们引入了 IApplication.h 和 IHttpServer.h 头文件，并创建了相应的实例。`$EnableHttpPrintTrace(true)` 宏注解用于启用 HTTP 请求打印，方便调试。

``$EnableHttpPrintTrace(true)` 这个宏注解可以让程序打印我们的路由。如果没有这个宏注解，则程序不会打印 http 的路由。在接下来的内容中会看到服务器的打印日志，其中就有路由相关的内容。



## 编写动态路由控制器

### 创建 IndexController

现在我们来创建一个支持动态路由的控制器。首先创建 IndexController.h 文件：

```cpp
#pragma once

#include <http/controller/IHttpControllerInterface.h>

class IndexController : public IHttpControllerInterface<IndexController>
{
    Q_GADGET
    $AsController(/)
public:
    IndexController();

public:
    $GetMapping(index, /)
    QString index();

    $GetMapping(hello)
    QString hello(std::string name);

    $PostMapping(welcome)
    QString welcome(QString $Query(name));
};
```



代码的第5行，我们通过 CRTP 继承了 `IHttpControllerInterface`类。

在第7行，引入 Q_GADGET 这个宏，他是实现反射的基础。

在第8行，`$AsController(/)` 中，这个是必须定义的，这个也指示当前的文件的前置路径是 `/`, 这个是在这个类中定义的其他路由的前置路径。

13-14行，我们定义了一个 index 函数，把这个函数指向的路由是 `/`,也就是根路由，使用 GET 方法进行请求。

16-17行，我们定义了一个 hello 函数，指向的路由是 hello。如果路由省略，那么函数名称就是这个路由。这里我们也定义一个 name 的参数，http 会在参数中，header， cookie 或者session 中查找这个参数。如果没有找到这个参数，程序就会返回 404 的状态。

19-20行，通过POST 方法请求 /welcome 这个路径。其中参数 name 必须通过路径参数来查询。



### 实现 IndexController

接下来创建 IndexController.cpp 文件：

```cpp
#include "IndexController.h"

IndexController::IndexController()
{

}

QString IndexController::index()
{
    return "hello world";
}

QString IndexController::hello(std::string name)
{
    return "hello " + QString::fromStdString(name);
}

QString IndexController::welcome(QString $Query(name))
{
    return "welcome " + name;
}
```



## 运行

### 运行输出

现在我们可以编译并运行这个项目。项目的输出如下：

```
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

IHttpControllerMapping:
 |
     |::GET / ==> QString IndexController::index()
     |welcome
         |::POST /welcome ==> QString IndexController::welcome(QString name)
     |hello
         |::GET /hello ==> QString IndexController::hello(std::string name)


server started, listen at  "127.0.0.1:8550"
```



在这个日志输出中有关于路由的内容：

```
IHttpControllerMapping:
 |
     |::GET / ==> QString IndexController::index()
     |welcome
         |::POST /welcome ==> QString IndexController::welcome(QString name)
     |hello
         |::GET /hello ==> QString IndexController::hello(std::string name)

```

我们可以将这个内容与上面的代码一同进行参考，可以看到我们定义的 请求方法，路由，对应的类成员函数，和映射的函数内容。



### 请求测试

接下来我们通过 curl 写一系列的请求。

- 正常请求 `/ `内容

```bash
C:\Users\Yue>curl -i 127.0.0.1:8550
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 11
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

hello world
```



- 通过 POST 请求 `/` 路径，会报 404 状态的问题。

```c++
C:\Users\Yue>curl -i -X POST 127.0.0.1:8550
HTTP/1.1 404 Not Found
Server: IWebCore
Connection: keep-alive
Content-Length: 30
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

IWebCore::IHttpNotFoundInvalid
```



- 请求 hello 的内容,添加路径参数 

```
C:\Users\Yue>curl -i 127.0.0.1:8550/hello?name=yuekeyuan
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 15
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

hello yuekeyuan
```



- 请求 hello 的内容，通过 header 的内容

```
C:\Users\Yue>curl -i -H "name: yuekeyuan" 127.0.0.1:8550/hello
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 15
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

hello yuekeyuan
```



- 请求 `/welcome` ,

```
C:\Users\Yue>curl -i -X POST 127.0.0.1:8550/welcome?name=yuekeyuan
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 17
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

welcome yuekeyuan
```



- 非法的请求。

```
C:\Users\Yue>curl -i -X POST 127.0.0.1:8550/welcome
HTTP/1.1 500 Internal Server Error
Server: IWebCore
Connection: keep-alive
Content-Length: 24
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

query argument not found
```

```
C:\Users\Yue>curl -i -X GET 127.0.0.1:8550/welcome?name=yuekeyuan
HTTP/1.1 404 Not Found
Server: IWebCore
Connection: keep-alive
Content-Length: 30
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

IWebCore::IHttpNotFoundInvalid
```

```
C:\Users\Yue>curl -i -H "name: yuekeyuan" 127.0.0.1:8550/welcome
HTTP/1.1 404 Not Found
Server: IWebCore
Connection: keep-alive
Content-Length: 30
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

IWebCore::IHttpNotFoundInvalid
```



## 下载

用户也可以直接下载该项目的代码，运行：

[dynamicMapping_demo](./assets/dynamicMapping_demo.zip)

注意：该项目已经包含了完整的动态路由示例代码，可以直接编译运行。

示例展示到此结束，如果用户有兴趣更深一步的了解，请参考 IHttp 相关的文档。