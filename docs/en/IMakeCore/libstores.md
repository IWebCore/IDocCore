# libstores Package Lookup Paths

## globalLibStore

Do you remember running the `ipc packages` command?

```bash
C:\Users\Yue>ipc packages
```

```plaintext
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

Name                            Latest Version   Summary
(yuekeyuan/)asio                1.30.2           asio library for C++
(yuekeyuan/)cpp-httplib         0.22.0           A C++11 single-file header-only cross platform HTTP/HTTPS library.
(yuekeyuan/)cpr                 1.20.0           C++ Requests: Curl for People
(yuekeyuan/)HTTPRequest         0.2.0            HTTPRequest is a single-header C++ library for making HTTP requests.
(yuekeyuan/)ICmd                1.1.0            cmd library
(yuekeyuan/)ICore               1.1.0            core library for IWebCore
(yuekeyuan/)IHttp               1.0.0            http mvc server framework by annotation
(yuekeyuan/)IHttp.assets        1.0.0            assets support for IHttp
(yuekeyuan/)IHttp.cors          1.0.0            cors support for IHttp
(yuekeyuan/)IHttp.session       1.0.0            session support for IHttp
(yuekeyuan/)IHttpPythonTest     1.0.0            python test lib embedded in IHttp
(yuekeyuan/)INody               1.0.0            c++ http template egine
(yuekeyuan/)IRdb                1.0.0            relational database operation library
(yuekeyuan/)ITcp                1.0.0            wrapped asio tcp server
(yuekeyuan/)nlohmann.json       3.12.0           json library for C++
(yuekeyuan/)packaging           1.0.0            python-packaging-like lib for c++, used for version management
(yuekeyuan/)stachenov.quazip    1.5.0            cross-platform C++ zip library
(yuekeyuan/)zlib                1.3.1            cross-platform C++ zip library
yuekeyuan/backward              1.6.0            Printing nice Python-styled stack traces with colors and source snippets, especially on crashes.
```

The `ipc package` command outputs the packages cached in IMakeCore. These packages are stored by default in the `.lib` folder. The `.lib` folder is configured in the `IMakeCore/.data/config.json` file, which has the default content as follows:

```json
{
    "globalLibStore":".lib",
    "libstores": [],
    "servers": [
        "http://115.191.52.106",
        "https://pub.iwebcore.org"
    ],
    "user": "default"
}
```

Note the first item in the configuration: `globalLibStore`. This points to `.lib`, which is mapped to `IMakeCore/.lib` in IMakeCore. All built-in packages in IWebCore are placed in this directory. Packages automatically downloaded from the network are also stored in this folder. This is the default package path for IMakeCore.

Users can use the `ipc libstore` command to view the current package paths:

```bash
yuekeyuan@Yue:~$ ipc libstores
```

```plaintext
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

/opt/IMakeCore/.lib
```

As shown above, after executing the `ipc libstores` command, a path is displayed. Since we haven't configured additional paths in the config.json, the only path here is the one for `globalLibStore`, which is `/opt/IMakeCore/.lib`.

## Project-Level Package Path

After creating a project that supports IMakeCore, executing the `ipc libstores` command in the project directory outputs an additional path:

```bash
D:\code\demo\cmake_demo>ipc libstores
```

```plaintext
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

D:/code/demo/cmake_demo/.lib
C:/Users/Yue/IMakeCore/.lib
```

In the output above, there's an additional path besides the global one: `D:/code/demo/cmake_demo/.lib`. This is the project-level package path. If a path lacks IMakeCore support, it won't output this path.

After executing the `ipc init` command, besides configuring `packages.json`, modifying CMake/QtMake files, it also creates an empty `.lib` folder in the project directory. When IMakeCore imports packages, it scans the packages in this folder as well.

The priority of the project-level package path is the highest. For example, if the same package exists in other paths and also in the project-level path, IMakeCore will prioritize importing the package from the project-level path.

### forceLocal

In the `packages.json` configuration for the project, there's a `forceLocal` field. This field copies packages from other locations into the project-level package path, as shown in the following configuration:

```json
{
    "packages":{
        "nlohmann.json" : {
            "forceLocal" : true,
            "version" : "*"
        }
    }
}
```

When executing CMake or QtMake commands, the nlohmann.json package is copied from the `globalLibStore` path to the project-level package path:

```cmake
# yuekeyuan@nlohmann.json@3.12.0
# json library for C++
include(D:/code/demo/qmake_demo/.lib/yuekeyuan@nlohmann.json@3.12.0.pri)
```

The above is a snippet from `.package.pri`. The path `D:/code/demo/qmake_demo/.lib` is the project-level package path, showing that the qmake_demo project references the path in its own directory. This is the project-level package path.

Why is this design included? One reason is that all packages are distributed as source code. If you want to modify a package's content, you can directly edit its source code. However, if you directly modify it in the `globalLibStore` path, it can contaminate the global package store. At such times, you can copy the package to your project directory for modification, thus not affecting the global packages.

Additionally, when sharing program source code with others, if you want to provide the program along with its packages, you can consider placing the packages in the program directory. In this case, you can set a global `forceLocal` field, and all dependencies of the program will be copied to the program directory.

```json
{
    "forceLocal" : true,
    "packages":{
        "nlohmann.json" : "*"
    }
}
```

In this case, all configured packages in `packages.json` will be copied to the program's package directory.

Users can also manually copy packages to the project-level package directory.

## Custom Package Paths

Besides the two paths mentioned above, IMakeCore also supports custom package paths. Users can add package paths in IMakeCore's `config.json` or in the program's `packages.json`.

In the `config.json` file, there's an empty field `libstores`. Users can add the paths of their used packages to this field list:

```json
{
    "globalLibStore":".lib",
    "libstores": [
        "D:/mylib1",
        "D:/mylib2"
    ],
    ......

}
```

In the `packages.json` file under the program directory, the `libstores` field can also be added:

```json
{
    "libstores": [
        "D:/mylib1",
        "D:/mylib2"
    ],
    "packages":{
        "nlohmann.json" : "*"
    }
}
```

If the configured packages in `packages.json` exist in these paths, they will be automatically imported from these paths.

## Package Path Priority

As described earlier, there are four types of package paths with the following priority:

1. Project-level package path
2. Project-defined additional package paths
3. Package paths defined in IMakeCore's configuration
4. globalLibStore path

If a package is found in a higher-priority path, the program will not reference packages from lower-priority paths.

## libstore Management in ipc

The ipc program includes the following commands for managing libstore:

- `ipc libstore add`

  Add a libstore to the system. By default, if the current path is an IMakeCore project, it uses the local path; otherwise, it uses the global path.

- `ipc libstore remove`

  Remove a libstore from either the local or global path. By default, it removes from the local path if it exists; otherwise, from the global path.

- `ipc libstores`

  - Print all libstore paths

Users can use these commands to manage libstore.