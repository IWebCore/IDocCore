# Using Example 2: IHttp Static File Service

> This document describes how to use IHttp's static file service.

In the previous document, we integrated the nlohmann/json library as an example. This document continues with a small demo, writing a static HTTP file server with minimal code.

---

## Configure Dependencies

First, create a project supported by IMakeCore. The project name is `staticMapping_demo`. Add IMakeCore support by running `ipc init`.

### pro File

The content of the project's `.pro` file is as follows:

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

The changes to this file compared to the original are as follows:

- Removed redundant configurations and comments for clearer documentation.
- Added support for the `_WIN32_WINNT` macro. Without this macro, the asio library may generate warnings when compiled with Mingw.
- Added support for the `ws2_32` and `mswsock` libraries.
  - These libraries are optional for MSVC compilers but are required for Mingw and LLVM compilers.
- Added IMakeCore support, which is the last three lines of code.

### packages.json Configuration

After running `qmake`, the `packages.json` file is generated. We now add some libraries to this file.

Modify the `packages.json` file as follows:

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

The six libraries added in this `packages.json` are:

- ICore: This library is the foundation of the IWebCore framework, supporting features such as reflection, configuration, and runtime management.
- nlohmann.json: A JSON library chosen for the IWebCore project, balancing performance and usability.
- asio: A fundamental network library.
- ITcp: A layer built on top of asio for managing TCP content.
- IHttp: The HTTP service package.
- IHttp.assets: This library is the static file service we will use today.

After executing `qmake` on the project, the screenshot of the project is as follows:

![image-20260214122853507](assets/image-20260214122853507.png)

In the screenshot, we see the six libraries used, along with paths such as `C:\Users\Yue\IMakeCore\.lib`, which points to the location of the code for these six libraries.

---

## Writing a Static File Server

### Start a Server

Modify the `main.cpp` file as follows:

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

In this file, we include the `IApplication.h` header file and create an instance of `IApplication`. The `IApplication` class serves a similar purpose to `QApplication` in Qt, providing additional encapsulation.

Next, we include the `IHttpServer.h` header file and create an instance of `IHttpServer`. This instance is used to create an HTTP server.

When we run the project, the output is as follows:

```
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___/

"IWebCore::IHttpDefaultAssets"  is not registered due to its invalid
server started, listen at  "127.0.0.1:8550"
```

First, we see the IWebCore banner.

`"IWebCore::IHttpDefaultAssets"  is not registered due to its invalid` is a warning because we added the `IHttp.assets` library but did not use it. This warning will disappear after we use the library.

The last line confirms that the server has started on port `8550`. We can test it with a curl request:

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

The server returns a `404 Not Found` status with the content `IWebCore::IHttpNotFoundInvalid`. This is because no content has been defined, so the server defaults to returning a 404.

---

### Add Static File Service

Modify the `main.cpp` file again as follows:

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

We added three lines of code to this file.

First, we included the `IHttpAssetsAnnomacro.h` header file. Then, we added two lines before the `main` function:

```cpp
$SetHttpAssetsEnabled(true)
$SetHttpAssetsPath("./")
```

These two lines are macro annotations, similar to annotations in Java. The first line enables the static file service, and the second line sets the path for the static file service.

The path we set here is the runtime directory of the program. Developers can modify it to any valid path, including Qt resource paths.

In addition, we create an `index.html` file in this directory:

```html
<h1>hello IWebCore</h1>
```

Now, the output is as follows:

```
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___/

server started, listen at  "127.0.0.1:8550"
```

The previous warning about `IHttp.assets` is gone.

Now, let's request the URL again:

```shell
C:\Users\Yue>curl -i  127.0.0.1:8550
HTTP/1.1 200 OK
Server: IWebCore
Connection: keep-alive
Content-Length: 23
Content-Type: text/html; charset=UTF-8
Keep-Alive: timeout=10, max=50

<h1>hello IWebCore</h1>
```

We also request another URL:

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

Both requests return the expected content. The static file service is now running.

---

### Notes

If the response is not as expected, it might be because the `index.html` file is placed in the wrong directory. In this case, check the runtime directory of the project. Alternatively, you can specify an absolute path.