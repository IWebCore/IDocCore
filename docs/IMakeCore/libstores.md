# libstores 包查找路径



## globalLibStore

还记得我们调用 `ipc packages` 这个命令么？

```
C:\Users\Yue>ipc packages

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

`ipc package` 这个命令会输出在 IMakeCore 中缓存的包。这些包的存储位置默认是在 .lib 文件夹里面。`.lib` 文件夹是在 `IMakeCore/.data/config.json` 这个文件中配置的, 这个文件默认内容如下：

```json
{
    "globalLibStore":".lib",
    "libstores": [
    ],
    "servers": [
	"http://115.191.52.106",
        "https://pub.iwebcore.org"
    ],
    "user": "default"
}
```

 注意配置中的第一项：`globalLibStore` 这个配置，它指向的是 `.lib` ，在IMakeCore 中会映射为 `IMakeCore/.lib` 这个文件夹。在IWebCore 中自带的包都会放置到这个目录下面。 用户从网络上自动下载的包也会放置在这个文件夹下面。这个路径是 IMakeCore 的默认包路径。



用户可以使用 `ipc libstore` 命令查看当前有哪些的包路径

```
yuekeyuan@Yue:~$ ipc libstores

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

/opt/IMakeCore/.lib

```

如上所示，`ipc libstores` 命令执行之后，会显示一个路径。由于我们在 config.json 中没有配置其他的路径，这里的路径只有 `globalLibStore` 的包路径，也就是 `/opt/IMakeCore/.lib` 这个路径。



## 程序级包路径

在我们创建一个 支持 IMakeCore 的项目之后，我们在项目目录下执行 `ipc libstores`  这个命令，他会多输出一个路径:

```
D:\code\demo\cmake_demo>ipc libstores

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

D:/code/demo/cmake_demo/.lib
C:/Users/Yue/IMakeCore/.lib
```

在上面的输出中，多了一个IMakeCore `globalLibStore` 之外的路径： `D:/code/demo/cmake_demo/.lib` 这个就是程序级的包路径。如果一个路径没有IMakeCore 的支持，它不会输出这个路径。



在 `ipc init` 命令执行完成，除了配置 `packages.json`,修改cmake / pro 文件之外，它还会在程序的目录下面创建一个 `.lib` 的空文件夹。IMakeCore在导入包的时候，也会扫描这个文件夹中的包，进行导入。

程序级包查找路径的优先级是最高的。 比如同一个包如果在其他路径中出现，也在程序级的包路径中存在，那么IMakeCore会优先导入程序级的包路径。



### forceLocal

在程序的`packages.json` 配置中，有一个 `forceLocal` 字段。这个字段会将程序在其他地方的包拷贝到程序级的包路径下面，如下配置：

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

在执行 cmake / qmake 命令的时候，nlohmann.json 这个包会从 `globalLibStore` 路径下面拷贝到 程序级的包路径下面。

```
# yuekeyuan@nlohmann.json@3.12.0
# json library for C++
include(D:/code/demo/qmake_demo/.lib/yuekeyuan@nlohmann.json@3.12.0.pri)
```

上面是 .package.pri 的内容截取，`D:/code/demo/qmake_demo/.lib` 是程序级的包路径，这里可以看到 qmake_demo 项目引用的路径是自己程序目录下面的 .lib 路径，也就是程序级包路径。

这里为什么会有这一个的设计呢？其中一个原因是我们的包都是以源码的形式进行发布的，如果我们想修改一个包的内容，可以直接修改它的源码。但是如果直接在 `globalLibStore` 路径下修改的话，会污染全局的包，这个时候我们可以将这个包拷贝到我们的程序目录下面进行修改，这个时候就不会污染全局的包。

此外，如果我们在和别人共享程序源代码的时候，如果想把程序连同程序的包一同给别人，这个时候就可以考虑将包放置到程序目录下面。这样就可以将程序代码连同包一同给出去。这个时候，我们可以设置一个全局的 `forceLocal`字段，程序所有的依赖的包都会拷贝到程序目录下面。

```json
{
    "forceLocal" : true,
    "packages":{
        "nlohmann.json" : "*"
    }
}
```

此时在 packages 中配置的所有包都会拷贝到程序集的包目录下面。

此外，用户也可以自己把包拷贝到 程序级的包目录下面。



## 自定义包路径

除了上面的两个路径之外，IMakeCore 也支持自定义的包路径。用户可以在IMakeCore 的 `config.json` 中添加包路径，也可以在 程序的 `packages.json` 中添加包路径。

在 `config.json` 文件中有一个空的字段 `libstores` 用户可以将自己使用的包路径添加到这个 字段列表中去。

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

在程序目录下面的 `packages.json` 文件中也可以添加 libstores 字段：

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

这样如果在 packages.json 中配置的包在这些包路径中存在，它就会自动从这些包路径中导入这些包。



## 包路径优先级

上面我们描述了四种包路径，他们的优先级为：

1. 程序级包路径
2. 程序定义的额外包路径
3. IMakeCore配置中定义的包路径
4. globalLibStore 路径

如果在优先级更高的路径下面找到了包，程序就不会引用优先级更低路径下面的包。



## ipc 中的libstore 管理

ipc 程序种有如下的关于 libstore 的命令：

- ipc libstore add 

  add libstore to system. default to local if pwd path is imakecore project, otherwise global path

- ipc libstore remove

  remove the libstore from either local or global. default local if exist, else global

- ipc libstores 

  - print all libstore paths

用户可以使用这些命令来管理 libstore



