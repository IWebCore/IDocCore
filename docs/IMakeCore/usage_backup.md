

#### 创建 qmake 的项目

我们创建一个最简单的 qt 项目

此时项目的文件结构如下：
    ```
    demo/
    ├── demo.pro
    └── main.cpp
    ```

项目的内容如下：
=== "demo.pro"
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

#### 集成 IMakeCore 到项目中去

集成 IMakeCore 到项目中去有两种方法

##### 方法一：手动集成

第一种方法是在 .pro 文件中手动复制如下内容， 粘贴到 .pro 文件中：

```pro
include($$(IQMakeCore))
IQMakeCoreInit()
include($$PWD/.package.pri)
```

##### 方法二：使用 ipc 命令集成

第二种方法是在项目当前目录下面打开命令行工具，输入如下命令：

```bash
ipc init
```

此时命令行中的内容显示如下：

```bash
C:\Users\Yue\demo>ipc init

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

add imake support succeed
```

此时我们的项目 IMakeCore 支持就完成了。



#### 添加 IMakeCore 后的项目变化

我们在项目上执行 qmake 命令之后，
此时项目的文件结构如下：

```
demo/
|-- .data/
|   ├── dump.json
├── .lib/
├── demo.pro
├── main.cpp
├──.package.pri
└── packages.json
```

QtCreator 中的项目管理截图如下：

![image-20250713150534562](assets/image-20250713150534562.png)


项目的内容变化为以下的内容

=== "test.pro"
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

=== ".packages.pri"
    ```pri
    ###################################
    # SYSTEM CONFIGURED, DO NOT EDIT!!!
    ###################################

    # inclue packages.json to project
    OTHER_FILES += packages.json 
    ```

=== "packages.json"
    ```json
    {
        "packages":{
            

        }
    }
    ```

=== "./data/dump.json"
    ```json
    []
    ```
​此时我们在QMake项目中就集成好了 IMakeCore 包管理系统。

### cmake 集成

cmake 集成 IMakeCore 与 qmake 集成 IMakeCore 基本相同，不同之处在于 cmake 项目的配置文件是 CMakeLists.txt 文件。

#### 创建 cmake 的项目

我们创建一个最简单的 cmake 项目

此时项目的文件结构如下：
    ```
    demo/
    ├── CMakeLists.txt
    └── main.cpp
    ```

项目的内容如下：

=== "CMakeLists.txt"
    ```cmake
    cmake_minimum_required(VERSION 3.5)

    project(test LANGUAGES CXX)
    
    set(CMAKE_CXX_STANDARD 11)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    
    add_executable(test main.cpp)
    ```

=== "main.cpp"
    ```cpp
    #include <iostream>

    using namespace std;
    
    int main()
    {
        cout << "Hello World!" << endl;
        return 0;
    }
    ```

#### 集成 IMakeCore 到项目中去

集成 IMakeCore 到项目中去有两种方法

##### 方法一：手动集成

第一种方法是在  CMakeLists.txt 文件中手动复制如下内容， 粘贴到  CMakeLists.txt 文件中：

```cmake
include($ENV{ICMakeCore})
ICMakeCoreInit(test)
```

##### 方法二：使用 ipc 命令集成

第二种方法是在项目当前目录下面打开命令行工具，输入如下命令：

```bash
ipc init
```

此时命令行中的内容显示如下：

```bash
C:\Users\Yue\test>ipc init
_____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

add imake support succeed
```

此时我们的项目 IMakeCore 支持就完成了。

#### 添加 IMakeCore 后的项目变化

我们在项目上执行 cmake 命令之后，
此时项目的文件结构如下：

```
test/
|-- .data/
|   ├── dump.json
├── .lib/
├── CMakeLists.txt
├── main.cpp
├── .package.cmake
└── packages.json
```

Qt vs Code 中的项目管理截图如下：

![image-20250713152514871](assets/image-20250713152514871.png)

项目的内容变化为以下的内容

=== "CMakeLists.txt"
    ```cmake
    cmake_minimum_required(VERSION 3.5)
    ```

    project(test LANGUAGES CXX)
    
    set(CMAKE_CXX_STANDARD 11)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    
    add_executable(test main.cpp)
    
    include($ENV{ICMakeCore})
    ICMakeCoreInit(test)
    ```

=== "main.cpp"
    ```cpp
    #include <iostream>

    using namespace std;
    
    int main()
    {
        cout << "Hello World!" << endl;
        return 0;
    }
    ```

=== ".packages.cmake"
    ```pri
    ###################################
    # SYSTEM CONFIGURED, DO NOT EDIT!!!
    ###################################
    ```

=== "packages.json"
    ```json
    {
        "packages":{
            

        }
    }
    ```

=== "./data/dump.json"
    ```json
    []
    ```

此时我们在CMake项目中就集成好了 IMakeCore 包管理系统。 


在上面的 cmake 或者 qmake 项目中，集成 IMakeCore 包管理之后，都会有一个 packages.json 文件，该文件用于管理项目中所使用的包。 用户如果想继续使用之前的方式操作 cmake 或者 qmake 项目，比如使用 vcpkg 安装包等，不会受到IMakeCore任何影响。


## 添加一个包到项目中

### cmake 项目

#### 添加一个包到项目中

下面我们添加一个包到项目中去，修改 packages.json 文件，添加一个包。

=== "packages.json"
    ```json
    {
        "packages":{
            "nlohmann.json" : "*"
        }
    }
    ```

在上面的代码中，我们添加了一个 json库，名字为 nlohmann/json，版本号为 *，表示使用最新版本。

在项目上执行CMAKE, 或者执行QMAKE, IMakeCore 会自动下载该包，并将其集成到项目中。

#### 项目变化

如下是 cmake 项目面板， 对比与之前的内容，多了一个 nlohmann.json@3.12.0 文件夹，这个就是我们所已经集成进来的包。

![image-20250713153533730](assets/image-20250713153533730.png)

我们看到 nlohmann.json 版本已经被集成进来了。

此时项目的文件结构如下：

```
demo/
|-- .data/
|   ├── dump.json
├── .lib/
	├──	nlohmann.json@3.12.0.cmake
├── CMakeLists.txt
├── main.cpp
├── .package.cmake
└── packages.json
```

此时的文件系统变化如下：

=== "CMakeLists.txt"
    ```cmake
    cmake_minimum_required(VERSION 3.5)
    

    project(test LANGUAGES CXX)
    
    set(CMAKE_CXX_STANDARD 11)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    
    add_executable(test main.cpp)
    
    include($ENV{ICMakeCore})
    ICMakeCoreInit(test)
    ```

=== "main.cpp"
    ```cpp
    #include <iostream>

    using namespace std;
    
    int main()
    {
        cout << "Hello World!" << endl;
        return 0;
    }
    ```

=== ".packages.cmake"
    ```pri
    ###################################
    # SYSTEM CONFIGURED, DO NOT EDIT!!!
    ###################################

    # nlohmann.json@3.12.0
    # json library for C++
    include(C:/Users/Yue/test/.lib/nlohmann.json@3.12.0.cmake)
    
    ```

=== "packages.json"
    ```json
    {
        "packages":{
            "nlohmann.json" : "*"
        }
    }
    ```

=== "./data/dump.json"
    ```json
    [
        {
            "name": "nlohmann.json",
            "version": "3.12.0",
            "path": "D:\\code\\packages\\IMakeCore\\.lib\\nlohmann.json@3.12.0",
            "autoScan": true,
            "summary": "json library for C++",
            "forceLocal": false
        }
    ]
    ```

#### 测试

为了测试我们添加的包是否能正常使用，我们修改 main.cpp 文件，添加如下代码：

```cpp
#include <iostream>
#include "json.hpp"

using namespace std;

int main()
{
    nlohmann::json j = {{"message", "Hello, world!"}} ;
    cout << j.dump(4) << endl;
    return 0;
}
```

编译执行该项目，输出如下：

![image-20250713154933558](assets/image-20250713154933558.png)

项目导入包成功



### qmake 项目

qmake 项目中 IMakeCore 的使用方式和 cmake 项目完全一致。这里不再详细说明。

