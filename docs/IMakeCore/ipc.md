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