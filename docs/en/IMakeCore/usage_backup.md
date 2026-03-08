#### Creating a qmake Project

We create the simplest Qt project.

At this point, the project's file structure is as follows:
    ```
    demo/
    ├── demo.pro
    └── main.cpp
    ```

The project contents are as follows:
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

#### Integrating IMakeCore into the Project

There are two methods to integrate IMakeCore into the project.

##### Method 1: Manual Integration

The first method is to manually copy the following content into the `.pro` file and paste it into the `.pro` file:

```pro
include($$(IQMakeCore))
IQMakeCoreInit()
include($$PWD/.package.pri)
```

##### Method 2: Integration using IPC Command

The second method is to open the command-line tool in the current project directory and enter the following command:

```bash
ipc init
```

The content displayed in the command line is as follows:

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

At this point, IMakeCore support for the project is complete.

#### Changes to the Project After Adding IMakeCore

After executing the `qmake` command on the project,
the project's file structure is now as follows:

```
demo/
|-- .data/
|   ├── dump.json
├── .lib/
├── demo.pro
├── main.cpp
├── .package.pri
└── packages.json
```

A screenshot of the project management in QtCreator is as follows:

![image-20250713150534562](assets/image-20250713150534562.png)

The changes to the project contents are as follows:

=== "demo.pro"
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

=== ".package.pri"
    ```pri
    ###################################
    # SYSTEM CONFIGURED, DO NOT EDIT!!!
    ###################################

    # include packages.json to project
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
At this point, the IMakeCore package management system is integrated into the QMake project.

### CMake Integration

Integrating IMakeCore into a CMake project is fundamentally similar to integrating it into a qmake project. The difference lies in the configuration file for CMake projects, which is `CMakeLists.txt`.

#### Creating a CMake Project

We create the simplest CMake project.

At this point, the project's file structure is as follows:
    ```
    demo/
    ├── CMakeLists.txt
    └── main.cpp
    ```

The project contents are as follows:

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

#### Integrating IMakeCore into the Project

There are two methods to integrate IMakeCore into the project.

##### Method 1: Manual Integration

The first method is to manually copy the following content into the `CMakeLists.txt` file and paste it into the file:

```cmake
include($ENV{ICMakeCore})
ICMakeCoreInit(test)
```

##### Method 2: Integration using IPC Command

The second method is to open the command-line tool in the current project directory and enter the following command:

```bash
ipc init
```

The content displayed in the command line is as follows:

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

At this point, IMakeCore support for the project is complete.

#### Changes to the Project After Adding IMakeCore

After executing the `cmake` command on the project,
the project's file structure is now as follows:

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

A screenshot of the project management in VS Code is as follows:

![image-20250713152514871](assets/image-20250713152514871.png)

The changes to the project contents are as follows:

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

=== ".package.cmake"
    ```cmake
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
At this point, the IMakeCore package management system is integrated into the CMake project.

### Adding a Package to the Project

#### CMake Project

##### Adding a Package to the Project

We will now add a package to the project. Modify the `packages.json` file to add a package.

=== "packages.json"
    ```json
    {
        "packages":{
            "nlohmann.json" : "*"
        }
    }
    ```

In the above code, we added a JSON library named `nlohmann/json`, with version `*`, indicating the use of the latest version.

After executing `cmake` or `qmake`, IMakeCore will automatically download the package and integrate it into the project.

##### Project Changes

The following is a screenshot of the CMake project panel. Compared to the previous content, there is an additional folder `nlohmann.json@3.12.0`, which is the package we have integrated.

![image-20250713153533730](assets/image-20250713153533730.png)

We can see that the `nlohmann.json` version has been integrated.

The project's file structure is now as follows:

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

The changes to the file system are as follows:

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

=== ".package.cmake"
    ```cmake
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

##### Testing

To test whether the added package can be used normally, modify the `main.cpp` file and add the following code:

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

Compile and run the project, and the output is as follows:

![image-20250713154933558](assets/image-20250713154933558.png)

The package has been successfully imported into the project.

#### qmake Project

The usage of IMakeCore in a qmake project is identical to that in a CMake project. No further details are provided.