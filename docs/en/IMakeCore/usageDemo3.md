# Example Usage 3: IHttp Dynamic Routing

> This document describes how to use the dynamic routing feature of IHttp.

In the previous two documents, we integrated the nlohmann/json library and implemented static file services. This document will demonstrate how to use the dynamic routing feature of IHttp, capturing and validating path parameters to achieve flexible URL routing.

## Configuring Dependency Libraries

This time, we are creating a CMake project, not a qmake project.

First, we create an IMakeCore-supported project named `dynamicMapping_demo`. Add IMakeCore support by running `ipc init`.

### CMakeLists.txt

The content of this project's CMakeLists.txt file is as follows:

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

Compared to the original file, the following changes were made:

- Added support for the `_WIN32_WINNT` macro. Without this macro, the asio library will throw a warning when compiled with mingw.
- Added support for the `ws2_32` and `mswsock` libraries.
  - These libraries are not required when using the MSVC compiler, but they must be included when using the mingw or llvm compilers.
- Added IMakeCore support, which is the last two lines of code.

Additionally, we added the main.cpp file and the `IndexController` class. The `IndexController` class is the class where we will handle the main logic today.

### packages.json Configuration

After executing cmake on the project, a packages.json file is created. We now need to add some libraries to this file.

Modify the packages.json file as follows:

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

In this packages.json file, we added five libraries, which are:

- ICore
  - This library is the foundation of the IWebCore framework. It supports reflection, configuration, runtime functionality, and more.
- nlohmann.json
  - nlohmann.json is the JSON library chosen for the IWebCore project. It balances performance and usability compared to other libraries.
- asio
  - A fundamental network library.
- ITcp
  - A layer built on top of asio for managing TCP content.
- IHttp
  - The HTTP service package.

We did not add the `IHttp.assets` library because this project no longer uses static file services.

## Writing the main.cpp File

Create the main.cpp file:

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

In this file, we included the IApplication.h and IHttpServer.h header files and created the corresponding instances. The `$EnableHttpPrintTrace(true)` macro annotation is used to enable HTTP request printing, which facilitates debugging.

The `$EnableHttpPrintTrace(true)` macro annotation allows the program to print our routes. Without this macro annotation, the program will not print HTTP routes. In the following content, there will be server log output, which includes route-related information.

## Writing the Dynamic Routing Controller

### Creating IndexController

Now, let's create a controller that supports dynamic routing. First, create the IndexController.h file:

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

On line 5, we inherited from the `IHttpControllerInterface` class using CRTP.

On line 7, the `Q_GADGET` macro is introduced, which is the foundation for implementing reflection.

On line 8, `$AsController(/)` must be defined. This indicates that the prefix path for the routes defined in this class is `/`.

Lines 13-14 define an `index` function, mapping it to the root route `/` using the GET method.

Lines 16-17 define a `hello` function, mapping it to the route `hello`. If the route is omitted, the function name becomes the route. Here, we also define a `name` parameter, which the HTTP request will look for in the parameters, headers, cookies, or session. If the parameter is not found, the program returns a 404 status.

Lines 19-20 define a POST request to the `/welcome` path. The parameter `name` must be queried via a path parameter.

### Implementing IndexController

Next, create the IndexController.cpp file:

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

## Running the Project

### Running Output

Now, we can compile and run the project. The output is as follows:

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

In this log output, there is information about the routes:

```
IHttpControllerMapping:
 |
     |::GET / ==> QString IndexController::index()
     |welcome
         |::POST /welcome ==> QString IndexController::welcome(QString name)
     |hello
         |::GET /hello ==> QString IndexController::hello(std::string name)

```

We can refer to this content along with the code above to see the defined request methods, routes, corresponding class member functions, and mapped function content.

### Request Testing

Next, we use curl to write a series of requests.

- Normal request to `/`

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

- A POST request to `/` returns a 404 status.

```bash
C:\Users\Yue>curl -i -X POST 127.0.0.1:8550
HTTP/1.1 404 Not Found
Server: IWebCore
Connection: keep-alive
Content-Length: 30
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

IWebCore::IHttpNotFoundInvalid
```

- Requesting the `hello` content and adding a path parameter.

```bash
C:\Users\Yue>curl -i 127.0.0.1:8550/hello?name=yuekeyuan
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 15
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

hello yuekeyuan
```

- Requesting the `hello` content via header.

```bash
C:\Users\Yue>curl -i -H "name: yuekeyuan" 127.0.0.1:8550/hello
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 15
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

hello yuekeyuan
```

- Requesting `/welcome`.

```bash
C:\Users\Yue>curl -i -X POST 127.0.0.1:8550/welcome?name=yuekeyuan
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 17
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

welcome yuekeyuan
```

- Invalid request.

```bash
C:\Users\Yue>curl -i -X POST 127.0.0.1:8550/welcome
HTTP/1.1 500 Internal Server Error
Server: IWebCore
Connection: keep-alive
Content-Length: 24
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

query argument not found
```

```bash
C:\Users\Yue>curl -i -X GET 127.0.0.1:8550/welcome?name=yuekeyuan
HTTP/1.1 404 Not Found
Server: IWebCore
Connection: keep-alive
Content-Length: 30
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

IWebCore::IHttpNotFoundInvalid
```

```bash
C:\Users\Yue>curl -i -H "name: yuekeyuan" 127.0.0.1:8550/welcome
HTTP/1.1 404 Not Found
Server: IWebCore
Connection: keep-alive
Content-Length: 30
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

IWebCore::IHttpNotFoundInvalid
```

## Download

Users can also directly download the project code and run it:

[dynamicMapping_demo](./assets/dynamicMapping_demo.zip)

Note: The project includes the complete dynamic routing example code and can be compiled and run directly.

The example has now been concluded. If users wish to learn more in depth, please refer to the IHttp-related documentation.