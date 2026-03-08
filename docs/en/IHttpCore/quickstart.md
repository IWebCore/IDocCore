# Quick Start

IHttpCore can also be referred to as IHttp. It is an HTTP framework based on reflection and macro annotations.

Want to quickly understand what IHttpCore is? This document provides a simple perspective on the features of IHttpCore.

## The Smallest Server

### Step 1: Create a New Project

IHttp currently supports use in CMake projects and Qt projects. We use Qt as an example. By default, create a Qt console project. As follows. The project content is as follows:

=== "server.pro"
    ```pro
    QT -= gui

    CONFIG += c++11 console
    CONFIG -= app_bundle
    
    DEFINES += QT_DEPRECATED_WARNINGS
    
    SOURCES += \
            main.cpp
    ```

=== "main.cpp"
    ```cpp
    #include <QCoreApplication>

    int main(int argc, char *argv[])
    {
        QCoreApplication a(argc, argv);
    
        return a.exec();
    }
    ```

The content in server.pro has been slightly trimmed.

A simple Qt console project is now ready.

### Step 2: Integrate IMakeCore

IHttpCore depends on IMakeCore. IMakeCore is a package management tool based on CMake and qmake. Many packages for IHttp can be downloaded and imported via IMakeCore.

Users need to install IMakeCore to perform subsequent package import tasks. Content about IMakeCore can be found in the [IMakeCore](../IMakeCore/quick_start.md) documentation.

By default, users have already installed and understood the features of IMakeCore (if not, you can consider it similar to npm, Maven, or Cargo for subsequent reading, and delve into the details of IMakeCore during actual operations).

In the project directory, execute the following command:

```bash
ipc init
qmake
```

The `ipc init` command adds a few lines of code to the server.pro file, enabling the Qt project to use the package management capabilities of IMakeCore. The `ipc` tool is a command-line tool built into IMakeCore.

If users fail to execute qmake from the command line, they can right-click on the project in the project panel and select `Run qmake` to manually execute the qmake command to refresh the project.

After executing the above commands, the entire project content is as follows:

=== "server.pro"
    ```pro
    QT -= gui

    CONFIG += c++11 console
    CONFIG -= app_bundle
    
    DEFINES += QT_DEPRECATED_WARNINGS
    
    SOURCES += \
            main.cpp
    
    include($$(IQMakeCore))
    IQMakeCoreInit()
    include($$PWD/.package.pri)
    ```

=== "main.cpp"
    ```cpp
    #include <QCoreApplication>

    int main(int argc, char *argv[])
    {
        QCoreApplication a(argc, argv);
    
        return a.exec();
    }
    ```

=== "packages.json"
    ```json
    {
        "packages":{
            
        }
    }
    ```

The changes to our project are three lines of IMakeCore-supported code added to the `server.pro` file, and an additional `packages.json` file.

If users use QtCreator, the changes to the project panel are as follows:

=== "Before Integrating IMakeCore"
	![Project panel before integrating IMakeCore](assets/image-20250715165313691.png)

=== "After Integrating IMakeCore"
	![Project panel after integrating IMakeCore](assets/image-20250715165434705.png)

### Step 3: Add Packages

Modify the `packages.json` file as follows:

=== "packages.json"
    ```json
    {
        "packages":{
            "asio" : "*",
            "nlohmann.json":"*",
            "ICore": "1.0.0",
            "ITcp" : "1.0.0",
            "IHttp" : "1.0.0"
        }
    }
    ```

Execute qmake, and the changes to the project panel are as follows:

=== "Project Panel"
    ![Project Panel](assets/image-20250715170932760.png)

The IHttp-related packages are now integrated. Note that five packages are imported here because `IHttp` depends on `ITcp` and `ICore`, and `ICore` depends on `asio` and `nlohmann.json`. If these are not imported together, IMakeCore will report an error when parsing package dependencies.

Adding packages is this simple.

One thing to note is that we need to modify the `server.pro` file, changing `c++11` to `c++17`. `IHttp` uses `c++17`, so users should modify this or adjust if errors occur; we won't list the `server.pro` file again for brevity.

### Step 4: Start a Server

Modify the `main.cpp` file and add server code as follows:

=== "main.cpp"
    ```cpp
    #include "core/application/IApplication.h"
    #include "http/IHttpServer.h"
    
    int main(int argc, char *argv[])
    {
        IApplication app(argc, argv);
    
        IHttpServer server;
        server.listen();
    
        return app.run();
    }
    ```

At this point, a server is started. Executing the program produces the following output:

=== "Console Output"
    ```txt
    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    server started, listen at  "127.0.0.1:8550"
    ```

Entering `127.0.0.1:8550` in the browser results in:

=== "Browser Result"
    ![Browser Return Result](assets/image-20250715172850506.png)

=== "Browser Request"
    ```
    GET / HTTP/1.1
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    Accept-Encoding: gzip, deflate, br, zstd
    Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
    Connection: keep-alive
    Host: 127.0.0.1:8550
    Sec-Fetch-Dest: document
    Sec-Fetch-Mode: navigate
    Sec-Fetch-Site: none
    Sec-Fetch-User: ?1
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
    sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    
    ```

=== "Browser Response"
    ```
    HTTP/1.1 404 Not Found
    Server: IWebCore
    Connection: keep-alive
    Content-Length: 30
    Content-Type: text/plain; charset=UTF-8
    Keep-Alive: timeout=10, max=50
    
    IWebCore::IHttpNotFoundInvalid
    
    ```

A minimal server has now been started.

### Step 5: Add Controller

In Step 3, there is a server that only returns a 404 response for any request. In the following content, we need to define our own request and response mappings.

Create a new FirstController class as follows:

=== "FirstController.h"
    ```cpp
    #pragma once

    #include "http/controller/IHttpControllerInterface.h"
    
    class FirstController : public IHttpControllerInterface<FirstController>
    {
        Q_GADGET
        $AsController(/)
    public:
        FirstController();
    
        $GetMapping(ping)
        QString ping();
    
        $GetMapping(hello)
        std::string hello();
    
        $GetMapping(info)
        IJson info();
    };
    ```

=== "FirstController.cpp"
    ```cpp
    #include "FirstController.h"

    FirstController::FirstController()
    {
    
    }
    
    QString FirstController::ping()
    {
        return "pong";
    }
    
    std::string FirstController::hello()
    {
        return "world";
    }
    
    IJson FirstController::info()
    {
        return IJson::object({{"name", "yuekeyuan"}});
    }
    ```

=== "main.cpp"
    ```cpp
    #include "core/application/IApplication.h"
    #include "http/IHttpServer.h"

    $EnableHttpPrintTrace(true)
    int main(int argc, char *argv[])
    {
        IApplication app(argc, argv);
    
        IHttpServer server;
        server.listen();
    
        return app.run();
    }
    ```

=== "server.pro"
    ```pro
    QT -= gui

    CONFIG += c++17 console
    CONFIG -= app_bundle
    
    DEFINES += QT_DEPRECATED_WARNINGS
    
    SOURCES += \
            FirstController.cpp \
            main.cpp
    
    HEADERS += \
            FirstController.h
    
    include($$(IQMakeCore))
    IQMakeCoreInit()
    include($$PWD/.package.pri)
    ```

One important point to note is that in the `main.cpp` file, we added the line `$EnableHttpPrintTrace(true)`. This macro enables detailed printing of HTTP request and response information.

Recompile and run the program, and the output is as follows:

=== "Console Output"
    ```txt
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
      | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
      | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
     _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
     \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    IHttpControllerMapping:
    |
        |ping
            |::GET /ping   ==> QString FirstController::ping()
        |info
            |::GET /info   ==> IJson FirstController::info()
        |hello
            |::GET /hello  ==> std::string FirstController::hello()


    server started, listen at  "127.0.0.1:8550"
    ```

For browser requests, we can see that the server returns the strings we defined.

=== "ping Request"
    === "Screenshot"
        ![image-20250715192809644](assets/image-20250715192809644.png)

    === "Request"
        ```
        GET /ping HTTP/1.1
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
        Accept-Encoding: gzip, deflate, br, zstd
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
        Connection: keep-alive
        Host: 127.0.0.1:8550
        Sec-Fetch-Dest: document
        Sec-Fetch-Mode: navigate
        Sec-Fetch-Site: none
        Sec-Fetch-User: ?1
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
        sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
        ```

    === "Response"
        ```
        HTTP/1.1 200 OK
        Server: IWebCore
        Connection: keep-alive
        Content-Length: 4
        Content-Type: text/plain; charset=UTF-8
        Keep-Alive: timeout=10, max=50

        pong
        
        ```

=== "hello Request"
    === "Screenshot"
        ![image-20250715192848735](assets/image-20250715192848735.png)

    === "Request"
        ```
        GET /hello HTTP/1.1
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
        Accept-Encoding: gzip, deflate, br, zstd
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
        Connection: keep-alive
        Host: 127.0.0.1:8550
        Sec-Fetch-Dest: document
        Sec-Fetch-Mode: navigate
        Sec-Fetch-Site: none
        Sec-Fetch-User: ?1
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
        sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
        ```

    === "Response"
        ```
        HTTP/1.1 200 OK
        Server: IWebCore
        Connection: keep-alive
        Content-Length: 5
        Content-Type: text/plain; charset=UTF-8
        Keep-Alive: timeout=10, max=50

        world
        
        ```

=== "info Request"
    === "Screenshot"
        ![image-20250715192931663](assets/image-20250715192931663.png)

    === "Request"
        ```
        GET /info HTTP/1.1
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
        Accept-Encoding: gzip, deflate, br, zstd
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
        Connection: keep-alive
        Host: 127.0.0.1:8550
        Sec-Fetch-Dest: document
        Sec-Fetch-Mode: navigate
        Sec-Fetch-Site: none
        Sec-Fetch-User: ?1
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
        sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
        ```

    === "Response"
        ```
        HTTP/1.1 200 OK
        Server: IWebCore
        Connection: keep-alive
        Content-Length: 20
        Content-Type: application/json; charset=UTF-8
        Keep-Alive: timeout=10, max=50

        {"name":"yuekeyuan"}
        
        ```

## Next Content

This is an introduction to the quick start, and no more demonstration content will be written. Users can learn more features by reading the documentation or referring to the sample code.

IHttpCore has many exciting features, such as:

- Writing classes with annotations similar to Java beans, and directly returning class objects or class lists from controller functions.
- Convenient database operations like in Spring JPA, with the ability to switch databases freely and generate various SQL statements automatically.
- A rich set of packages to meet your needs, such as mapping static file routes with just two lines of code.
- A template engine similar to JSP for convenient template rendering.
- A powerful plugin mechanism for easy extension of functionality.
- Comprehensive testing features, allowing users to conveniently test their APIs without relying on external tools.
- ...