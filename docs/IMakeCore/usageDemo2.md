# 使用示例2: IHttp静态文件服务

> 本篇文档描述如何使用 IHttp 的静态文件服务。

在上篇文档我们集成了 nlohmann/json 这个库作为展示，这篇文档依然是写一个小的demo,用最少的代码写一个静态的 http 文件服务器。



## 配置依赖库

首先我们创建一个IMakeCore的支持的项目,项目名称是staticMapping_demo, 通过 `ipc init` 添加 IMakeCore 支持。

### pro 文件

该项目的 pro 文件内容如下。

```pro
QT = core

CONFIG += c++17 cmdline

SOURCES += \
        main.cpp

win32 {
    DEFINES += _WIN32_WINNT=0x0A00
    LIBS += -lws2_32
    LIBS += -lmswsock
}

include($$(IQMakeCore))
IQMakeCoreInit()
include($$PWD/.package.pri)

```

这个文件相对于原始的文件，修改如下：

- 删除了多余的配置项和注释的内容，让文档显示更清晰。
- 添加了 `_WIN32_WINNT` 这个宏的支持。如果没有这个宏，在 mingw 编译器下 asio 会报 warning异常。
- 添加了 `ws2_32` 和 `mswsock` 这两个库的支持。
  - 这两个库在编译的时候，如果是 msvc 编译器的情况下是不需要的，但是对于 mingw 和 llvm 编译器，这两个库是必须填写上的。

- 添加了 IMakeCore支持，也就是最后三行的代码。



### packages.json 配置

在项目上执行 qmake 之后，会创建 packages.json 文件，现在我们要添加一些库到这个文件夹里面。

修改packages.json文件如下：

```json
{
    "packages":{
        "ICore" : "1.1.0",
        "nlohmann.json" : "3.12.0",
        "asio" : "1.30.2",
        "ITcp" : "1.0.0",
        "IHttp" : "1.0.0",
        "IHttp.assets" : "1.0.0"
    }
}
```

在这个packages.json 中，我们添加了六个库他们依次是：

- ICore
  - 这个库是 IWebCore 框架的基础，它支持反射，配置，运行时等一系列的内容。

- nlohmann.json
  - nlohmann.json 是IWebCore 项目中所选择的json库，相对与其他的库，这个库兼顾了性能和可用性。
- asio
  - 基础网络库。
- ITcp
  - 在 asio 的基础之上做了一层封装，用于管理 tcp 内容。
- IHttp 
  - http 服务包。
- IHttp.assets
  - 这个库就是我们今天要使用的静态文件服务的库了。  



在项目执行qmake 后，这个项目的截图如下：

![image-20260214122853507](assets/image-20260214122853507.png)

在这个上面我们看到了我们所使用的六个库，在头文件和源文件中也有 `C:\Users\Yue\IMakeCore\.lib` 这个路径，这个路径就是我们上面六个库的代码文件所在的地方。



## 编写静态文件服务器



### 开启一个服务器

现在我们修改 main.cpp 文件，内容如下：

```cpp
#include <core/application/IApplication.h>
#include <http/IHttpServer.h>

int main(int argc, char *argv[])
{
    IApplication app(argc, argv);

    IHttpServer server;
    server.listen();

    return app.exec();
}
```



在文件中，我们引入了 IApplication.h 这个头文件，并创建了 IApplication 的实例。IApplication 的作用类似于 Qt 中的 QApplication，它做了更多的封装。



之后我们引入了 IHttpServer.h这个头文件，并创建了一个 IHttpServer 的实例。这个实例的目的是创建一个 http 的服务器。



此时我们运行这个项目，项目的输出如下：

```
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

"IWebCore::IHttpDefaultAssets"  is not registered due to its invalid
server started, listen at  "127.0.0.1:8550"

```

在输出中首先看到的是一个 IWebCore 的banner。

`"IWebCore::IHttpDefaultAssets"  is not registered due to its invalid` 这个是由于我们添加了 IHttp.assets 这个库，但是没有用它，而报的一个警告。接下来我们会用到这个库，这个警告也会消失。

最后一行看到我们的服务器启动起来了，端口是 8550。我们使用curl请求一下这个路径,它的输出如下：

```shell
C:\Users\Yue>curl -i  127.0.0.1:8550
HTTP/1.1 404 Not Found
Server: IWebCore
Connection: keep-alive
Content-Length: 30
Content-Type: text/plain; charset=UTF-8
Keep-Alive: timeout=10, max=50

IWebCore::IHttpNotFoundInvalid
```

他返回了 404 的状态，内容是 `IWebCore::IHttpNotFoundInvalid`,这个是因我我们啥也没定义，它就只能进行 404 的返回了。



### 添加 静态文件服务

再次修改 main.cpp 如下：

```cpp
#include <core/application/IApplication.h>
#include <http/IHttpServer.h>
#include <http/assets/IHttpAssetsAnnomacro.h>

$SetHttpAssetsEnabled(true)
$SetHttpAssetsPath("./")
int main(int argc, char *argv[])
{
    IApplication app(argc, argv);

    IHttpServer server;
    server.listen();

    return app.exec();
}
```

我们在这个文件中添加了三行代码。

首先我们导入了IHttpAssetsAnnomacro.h 这个头文件，其次我们写了两行在 main 函数前面的代码：

```cpp
$SetHttpAssetsEnabled(true)
$SetHttpAssetsPath("./")
```

这两行代码叫做宏注解，它类似于 java 中的注解。第一行的意思是开启 静态文件服务，第二行是设置一个静态文件服务的路径。

此时我们设置的文件路径就是程序的运行路径。开发者也可以修改为其他的任意的合法的路径，包括 Qt Resource 资源路径等。



除了这个之外，我们再写一个 index.html 文件放到这个目录下面：

```html
<h1>hello IWebCore<h1>
```

对，就是这一行内容，放到程序目录下面。此时输出如下：

```
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

server started, listen at  "127.0.0.1:8550"
```

可以看到之前的 assets 相关的提示消失了。

我们再请求一下这个url

```
C:\Users\Yue>curl -i  127.0.0.1:8550
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 23
Content-Type: text/html; charset=UTF-8
Keep-Alive: timeout=10, max=50

<h1>hello IWebCore</h1>
```

我们也请求一下另外一个路径

```bash
C:\Users\Yue>curl -i  127.0.0.1:8550/index.html
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 23
Content-Type: text/html; charset=UTF-8
Keep-Alive: timeout=10, max=50

<h1>hello IWebCore</h1>
```

看到这两个文件都能正常返回内容。我们的静态文件服务启动起来了。



### 注意事项

如果你在请求中，没有正确返回，可能是把 index.html 文件放错位置了，这个时候就需要查看项目的运行目录是在哪里。或者直接写一个绝对路径也可以。



## 下载

用户也可以直接下载该项目的代码，运行：

[staticMapping_demo](./assets/staticMapping_demo.zip)

注意这里的路径配置是使用了资源路径,不在需要用户去创建 index.html 文件。