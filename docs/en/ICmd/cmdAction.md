<译文内容>
# Defining Commands

> This document describes how to define commands.

## Example

We will copy the `VersionCmd` example from the [guide](./overview.md) directly, and then we will explain how to define command-line arguments for Cmd based on this example.

To prevent users from forgetting what the code looks like, it is copied as follows:

=== "VersionCmd.h"

    ```cpp
    #pragma once
    
    #include "cmd/ICmdInterface.h"
    
    class VersionCmd : public ICmdInterface<VersionCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        VersionCmd();
    
    public:
        $CmdMappingMemo(version, "print imakecore version info")
        $CmdMapping(version)
        void version();
    };
    ```

=== "VersionCmd.cpp"

    ```cpp
    #include "VersionCmd.h"
    
    VersionCmd::VersionCmd()
    {
    
    }
    
    void VersionCmd::version()
    {
        qDebug() << "v1.0.0";
        quick_exit(0);
    }
    ```

## ICmdInterface
Defining a Cmd class requires inheriting from `ICmdInterface`.

The `ICmdInterface` class is located in the `ICmd package` under the path `cmd/ICmdInterface.h`. Users must include this header file in their class.

=== "Header File Inclusion"
    ```cpp
    #include "cmd/ICmdInterface.h"
    ```

`ICmdInterface` is a `CRTP` template base class, and its definition is as follows:

=== "ICmdInterface Class Definition"

    ```cpp
    template<typename T, bool enabled=true>
    class ICmdInterface : public ICmdWare, public ITaskWareUnit<T, ICmdCatagory, enabled>, public ISoloUnit<T>
    {
    public:
        ICmdInterface() = default;
    
    public:
        virtual void $task() final;
    };
    ```

The base classes of `ICmdInterface` are not something users need to worry about. What matters is the two template parameters `T` and `enabled` of `ICmdInterface`.

<br>

The first template parameter `typename T` is the name of the subclass we are implementing. For example, in the `VersionCmd` class, the parameter for `ICmdInterface` is `VersionCmd`.

=== "VersionCmd Class Definition"
    ```cpp
    class VersionCmd : public ICmdInterface<VersionCmd>
    ```

<br>

The second template parameter `bool enabled` has a default value of `true`, indicating whether the Cmd is enabled. If set to `false`, the Cmd will not be used.

Users generally do not need to set this value, but if a user wants to disable the class, a better approach than deleting the class is to set `enabled` to `false` in the class definition.

For example, if we do not want to use `VersionCmd`, we can define it as follows:

=== "Disable VersionCmd"
    ```cpp
    class VersionCmd : public ICmdInterface<VersionCmd, false>
    ```

This way, users cannot use this Cmd anymore.

## Q_GADGET

`Q_GADGET` is a macro used to declare a class as a `Qt meta type`. Classes declared with `Q_GADGET` can be reflected through Qt's meta system to obtain additional information about the class, which is used in the parsing of commands, parameters, and options.

For more information about `Q_GADGET`, please refer to the Qt official documentation.

## $AsCmd

`$AsCmd` is a macro annotation. Its main purpose is to assist in reflection and to define the prefix command path.

A complete command line is composed of the program name, the prefix command path defined by `$AsCmd`, and the command path defined by `$CmdMapping`.

In `$AsCmd`, if the user does not want to use a prefix command, they can set the macro parameter to `/`.

For example, in our `VersionCmd`, we set the parameter of `$AsCmd` to `/`. At this point, the parsed command path is `some-exe version`, where `some-exe` is the program name.

If the content set is not `/`, for example, `abc`:

=== "$AsCmd(abc)"
    ```
    #pragma once

    #include "cmd/ICmdInterface.h"
    
    class VersionCmd : public ICmdInterface<VersionCmd>
    {
        Q_GADGET
        $AsCmd(abc)
    public:
        VersionCmd();
    
    public:
        $CmdMappingMemo(version, "print imakecore version info")
        $CmdMapping(version)
        void version();
    };
    ```

Then the command path for this command is `some-exe abc version`.

<br>

Users can also set multiple command prefixes. The command prefixes are separated by commas. For example, we can set parameters like `abc def, ghi`:

=== "$AsCmd(abc def, ghi)"
    ```
    #pragma once

    #include "cmd/ICmdInterface.h"
    
    class VersionCmd : public ICmdInterface<VersionCmd>
    {
        Q_GADGET
        $AsCmd(abc, def, ghi)
    public:
        VersionCmd();
    
    public:
        $CmdMappingMemo(version, "print imakecore version info")
        $CmdMapping(version)
        void version();
    };
    ```

At this point, the command path for this command is `some-exe abc def version`.

## $CmdMapping

`$CmdMapping` is used to define the specific command function. For example, in `VersionCmd`, we define a `version` command mapping and function:

=== "$CmdMapping(version)"

    ``` 
        //...
        $CmdMappingMemo(version, "print imakecore version info")
        $CmdMapping(version)
        void version();
        //...
    ```

### Mapping Function

The parameter of the `$CmdMapping` macro must be the name of the response function, and the macro annotation must be followed by the response function.

If there is no response function after `$CmdMapping`, the program will crash before running. If the function name does not match the first parameter of the macro annotation, the program will crash during runtime.

For the response function, ICmd has the following requirements:

- The return type of the response function must be `void` and cannot be any other return type.

- The response function can have no parameters. If it has parameters, the parameter type must be `ICmdRequest&` or `const ICmdRequest&`.

### Mapping Path

The mapping path of `$CmdMapping` has the following cases:

#### Default Mapping Path

If `$CmdMapping` has only one parameter, like `version` in the example, then this parameter is both the function name and the mapping path.

In this example, `$CmdMapping(version)` defines a `version` mapping function, and the mapping path for this function is `version`.

A complete command line is composed of the program name, the prefix command path defined by `$AsCmd`, and the command path defined by `$CmdMapping`. Thus, the origin of the command `some-exe version` is formed by combining these parts.

#### Custom Mapping Path

Users can also customize commands.

`$CmdMapping` can have up to nine parameters. If there is more than one parameter, the list of parameters starting from the second one is the mapping path defined by `$CmdMapping`.

Therefore, `$CmdMapping(version)` and `$CmdMapping(version, version)` are equivalent.

If the definition is `$CmdMapping(version, abc, def, ghi)`, then the mapping path defined by `$CmdMapping` is `abc def ghi`, which, combined with the path defined by `$AsCmd`, forms the complete mapping path.

#### `/` Mapping Path

The parameter of `$CmdMapping` can be `/`, which indicates that `$CmdMapping` does not define a path. In this case, the path of the mapping function is the path defined by `$AsCmd`.

Therefore, `VersionCmd.h` can be written as follows, which is equivalent to the initial `VersionCmd.h`:

=== "VersionCmd.h" 

    ```cpp
    #pragma once
    
    #include "cmd/ICmdInterface.h"
    
    class VersionCmd : public ICmdInterface<VersionCmd>
    {
        Q_GADGET
        $AsCmd(version)
    public:
        VersionCmd();
    
    public:
        $CmdMappingMemo(version, "print imakecore version info")
        $CmdMapping(version, /)
        void version();
    };
    ```

## $CmdMappingMemo

`$CmdMappingMemo` is used to define the description of a command. This information is output in the program's help.

The first parameter of `$CmdMappingMemo` must be the name of the mapping function, and the second parameter is a string enclosed in double quotes, as shown in the example.

=== "$CmdMappingMemo"

    ```cpp
        $CmdMappingMemo(version, "print imakecore version info")	
    ```

At this point, if we use the command `some-exe version -?` to view this content, we can see the relevant output:

=== "some-exe version -? Output"

    ```
    C:\Users\Yue>ipc version -?
    
    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        ipc version
    [Memo]:
        print imakecore version info
    ```

## Defining Multiple Commands in a Class

A Cmd class can define multiple commands. Each command must be defined using `$CmdMapping`.

For example, we can define `add` and `sub` commands.

=== "AddSubCmd.h"

    ```cpp
    #pragma once
    
    #include "cmd/ICmdInterface.h"
    
    class AddSubCmd : public ICmdInterface<AddSubCmd>
    {
        Q_GADGET
        $AsCmd(addsub)
    public:
        AddSubCmd();
    
    public:
        $CmdMappingMemo(add, "add two numbers")
        $CmdMapping(add)
        void add();
    
        $CmdMappingMemo(sub, "sub two numbers")
        $CmdMapping(sub)
        void sub();
    };
    ```

=== "AddSubCmd.cpp"
    ```cpp
    #include "AddSubCmd.h"
    
    AddSubCmd::AddSubCmd()
    {
    }
    void AddSubCmd::add()
    {
        qDebug() << "add created";
        quick_exit(0);
    }
    
    void AddSubCmd::sub()
    {
        qDebug() << "sub created";
        quick_exit(0);
    }
    ```

In the above example, we define two commands in a class: `add` and `sub`. The commands `some-exe addsub add` and `some-exe addsub sub` call the `add` and `sub` functions of the `AddSubCmd` class, respectively.

However, in actual applications, it is not recommended to define multiple commands in one class because the class not only defines commands but also contains content for parameters and options. Commands defined in one class will share the same options and parameters.

Therefore, we recommend defining one command per class.

However, there are exceptions, such as when we define a command like `some-exe package list`, and we want to use `some-exe list` as a shortcut. In such cases, we can define two mapping functions, and call one from the other.