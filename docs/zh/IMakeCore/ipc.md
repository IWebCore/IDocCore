# ipc 工具

> 本文档描述 ipc  命令行工具。

> 由于 ipc 工具仍有大量功能需要开发，本文目前不做详细介绍，用户可以自己通过 `ipc` 相关命令探索已有的功能。

`ipc` 命令行工具是 用于管理 IWebCore 项目的命令行工具。对于IMakeCore而言，它提供了初始化 IMakeCore, 包管理，用户管理等一系列的功能。

`ipc` 工具是由 `IWebCore`中的[ICmd](http://127.0.0.1:8000/ICmd/overview/)框架编写而成，这里推荐用户使用 `ICmd` 工具来进行用户自己的命令行工具的编写，非常的方便和人性化。

用户在命令行中输入 `ipc` 命令会弹出如下内容。

```
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

your input cmd do not match any action
[Avaliable Cmds]:
ipc add               [Memo]: add package to project, same as command 'package add'
ipc email             [Memo]: output user name
ipc email set         [Memo]: set email info
ipc init              [Memo]: add support for imake package system to the existing project
ipc install           [Memo]: install package from remote to system. same as commad 'package install'
ipc libstore add      [Memo]: add libstore to system. default to local if pwd path is imakecore project, otherwise global path
ipc libstore remove   [Memo]: remove the libstore from either local or global. default local if exist, else global
ipc libstores         [Memo]: print all libstore paths
ipc package add       [Memo]: add package to project
ipc package install   [Memo]: install package from remote to system
ipc package remove    [Memo]: remove package from project
ipc package update    [Memo]: update package in project
ipc packages          [Memo]: list package installed in this device
ipc remove            [Memo]: remove package from project. same as command 'package remove'
ipc search            [Memo]: search package online
ipc server add        [Memo]: add server to system. default to local if pwd path is imakecore project, otherwise global path
ipc server remove     [Memo]: remove the server from either local or global. default local if exist, else global
ipc servers           [Memo]: print all server paths
ipc update            [Memo]: update package in project. same as command 'package update'
ipc user              [Memo]: output user name
ipc user set          [Memo]: set name info
ipc version           [Memo]: print imakecore version info
```

这是目前已经实现的功能，用户可以通过 `-?` 帮助探索相关的功能。

## 使用 ipc 进行包管理

### ipc search

该命令的格式如下：

```bash
[CMD]:
    ipc search
[Memo]:
    search package online
[Argx]:
    Index  Name        TypeName  Nullable  Memo
    1      searchText  QString   false     searched text
```

它有一个 searchText 参数

如果使用该命令行，则是如下：

```bash
C:\Users\Yue>ipc search -- tcp

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

ITcp  1.0.0  wrapped asio tcp server

```

用户可以通过此命令搜索网络上的库。



### ipc add

该命令的格式如下：

```bash
[CMD]:
    ipc add
[Memo]:
    add package to project, same as command 'package add'
[Argx]:
    Index  Name     TypeName  Nullable  Memo
    1      name     QString   false
    2      version  QString   true
```

它可以有两个参数，第一个参数是包名称，第二个参数是版本号，第二个参数可以省略，默认是 `*`, 最新版本。

如果省略版本，命令行会自动计算出相应的版本号。

如下是调用示例：

```bash
D:\code\project\IPubCmd>ipc add -- cpr

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

package add success. Name: cpr Version: 1.20.0

```

### ipc remove

该命令行的格式如下：

```bash
[CMD]:
    ipc remove
[Memo]:
    remove package from project. same as command 'package remove'
[Args]:
    Name  TypeName  Nullable  Memo
    name  QString   false     package name you want to remove from project
```

它只有一个必须的参数 name, 包的名称。

如下是调用示例：

```bash
D:\code\project\IPubCmd>ipc remove -- cpr

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

remove package succeed. package name:  "cpr"

```

### ipc update

该命令行的作用是更新包，它的格式如下：

```txt
[CMD]:
    ipc update
[Memo]:
    update package in project. same as command 'package update'
[Argx]:
    Index  Name     TypeName  Nullable  Memo
    1      name     QString   false     package name to be update in project
    2      version  QString   true      package version to be update in project
```

它有两个参数，第一个参数是包名，这个是必须项。第二个参数是版本号，版本号可以是 `*` 或者具体版本，可以省略。如果省略，则版本是 `*`。

如果版本为 `*`， 那么IMakeCore 会查找该包的最高版本，并设置为最高版本。最高版本是查找本地和线上的所有版本，找出所有版本中的最高版本进行设置。

### ipc install

该命令的格式如下：

```txt
[CMD]:
    ipc install
[Memo]:
    install package from remote to system. same as commad 'package install'
[Argx]:
    Index  Name         TypeName  Nullable  Memo
    1      packageName  QString   false     to be installed package name
    2      version      QString   true      to be installed package version
```

它有两个参数，包名和版本号。如果verrsion 省略，则默认是最高版本。

该命令会查找网络上的包，并下载安装包。



