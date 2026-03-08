# ipc tool

> This document describes the `ipc` command-line tool.

> Since the `ipc` tool still has many features to be developed, this document does not provide a detailed introduction at the moment. Users can explore the existing functionalities by themselves using the `ipc` related commands.

The `ipc` command-line tool is a command-line utility for managing IWebCore projects. For IMakeCore, it provides functionalities such as initialization of IMakeCore, package management, user management, and more.

The `ipc` tool is developed using the [ICmd](http://127.0.0.1:8000/ICmd/overview/) framework within `IWebCore`. It is recommended that users use the `ICmd` tool to write their own command-line tools, as it is very convenient and user-friendly.

When users input the `ipc` command in the command line, the following content is displayed.

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

These are the features currently implemented. Users can explore the related functionalities using the `-?` help command.

## Using IPC for Package Management

### ipc search

The format of this command is as follows:

```bash
[CMD]:
    ipc search
[Memo]:
    search package online
[Argx]:
    Index  Name        TypeName  Nullable  Memo
    1      searchText  QString   false     searched text
```

It has one parameter: `searchText`.

If this command is used, it appears as follows:

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

Users can use this command to search for libraries online.

### ipc add

The format of this command is as follows:

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

It can have two parameters: the first is the package name, and the second is the version number. The second parameter can be omitted, with the default being `*`, the latest version.

If the version is omitted, the command will automatically determine the corresponding version.

The following is a call example:

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

The format of this command is as follows:

```bash
[CMD]:
    ipc remove
[Memo]:
    remove package from project. same as command 'package remove'
[Args]:
    Name  TypeName  Nullable  Memo
    name  QString   false     package name you want to remove from project
```

It has one required parameter: `name`, the package name.

The following is a call example:

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

This command is used to update packages, with the following format:

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

It has two parameters: the first is the package name (required), and the second is the version number, which can be `*` or a specific version and can be omitted. If omitted, the version is `*`.

If the version is `*`, IMakeCore will find the highest version of the package and set it accordingly. The highest version is determined by finding all versions available locally and online, and selecting the highest one.

### ipc install

The format of this command is as follows:

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

It has two parameters: the package name and the version number. If the version is omitted, the default is the highest version.

This command will search for the package online and download and install it.