<译文内容>
# Command Line Argument Set

> This document describes how to handle argument sets.

A command line is not only composed of commands but also requires parameters. CmdArgs is a command line argument set that can parse command line parameters and provides convenient interfaces to retrieve parameter values.

## Rules for Command Line Parameters

In the ICmd command, the rules for command line parameters are as follows:

- Parameters are introduced by double hyphens `--` followed by one or more parameters. Note that there must be a space between `--` and the parameter; otherwise, it will be parsed as an option rather than a parameter.
- Parameters can be a single word or multiple words. Multiple parameters must be separated by a space.
- If a single parameter contains spaces, the parameter must be enclosed in double quotes.

The following are valid parameters:

```bash
-- abc
-- 123
-- true
-- false
-- abc 124 true hello
-- "c:/program files/hello/world"
```

## Examples

For demonstration purposes, we create a `testCmd` project and define a `PrintCmd` class. The code is as follows:

=== "PrintCmd.h"

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"

    class PrintCmd : public ICmdInterface<PrintCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        PrintCmd();

    public:
        $CmdArgsMemo(args, "argumets to be printed")
        $CmdArgs(QStringList, args)

    public:
        $CmdMappingMemo(print, "print arguments")
        $CmdMapping(print)
        void print();
    };
    ```

=== "PrintCmd.cpp"

    ```cpp
    #include "PrintCmd.h"

    PrintCmd::PrintCmd()
    {

    }

    void PrintCmd::print()
    {
        qDebug() << args;
    }
    ```

=== "main.cpp"

    ```cpp
    #include "PrintCmd.h"

    PrintCmd::PrintCmd()
    {

    }

    void PrintCmd::print()
    {
        qDebug() << args;
        quick_exit(0);
    }
    ```

Run this program. The output is as follows:

=== "-? Help"

    ```bash
    D:\test\cmd>testCmd.exe print -?

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \_ __|

    [CMD]:
        testCmd.exe print
    [Memo]:
        print arguments
    [Args]:
        Name  TypeName     Nullable  Memo
        args  QStringList  false     argumets to be printed
    ```
    This is the help information.

=== "One Argument"

    ```bash
    D:\test\cmd>testCmd.exe print -- hello

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \_ __|

    ("hello")
    ```

=== "Multiple Arguments"

    ```bash
    D:\test\cmd>testCmd.exe print -- hello world

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \_ __|

    ("hello", "world")

    ```

=== "Argument with Spaces"

    ```bash
    D:\test\cmd>testCmd.exe print -- hello world "hello world"

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \_ __|

    ("hello", "world", "hello world")

    ```

=== "No Arguments"

    ```bash

    D:\test\cmd>testCmd.exe print --

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \_ __|

    ERROR OCCURED: Args is defined not empty, but the cmd request arguments is empty [Action Path]: print [Value Name]: args [Cmd Path]: print [Cmd Arg Type]: Args [Cmd Arg Values]:

    [CMD]:
        testCmd.exe print
    [Memo]:
        print arguments
    [Args]:
        Name  TypeName     Nullable  Memo
        args  QStringList  false     argumets to be printed

    ```

In the above examples, the output content for various scenarios can be observed.

## $CmdArgs

The `$CmdArgs` macro annotation is used to declare an argument set. The macro has two parameters: the first is the data type to be parsed, and the second is the name of the argument set. During program execution, users will use this name to retrieve the value of the argument set.

Note that we refer to "argument set" here rather than "parameter" because we have defined macros like `$CmdArgs1`, `$CmdArgs`, etc., for handling individual parameter annotations. Users can see this in subsequent sections.

The name of `$CmdArgs` must be a valid class field name. This is because the `$CmdArgs` macro annotation generates a member variable in the class with the name specified after `$CmdArgs`. Its definition is as follows:

=== "Definition of $CmdArgs"

    ```cpp
    #define $CmdArgs(TYPE, NAME)                                            \
        $CmdArgsDeclare(TYPE, NAME)                                          \
        TYPE NAME {};
    ```

It uses the first parameter `type` and the second parameter `name` to declare a class member variable.

### Parameter Types

The available member types in ICmd can be divided into two categories: simple types and composite types.

#### Simple Types

Simple types include the following:

- **bool type**: Represents a boolean value.
- **Numeric types**: short/int/long/long long/float/double, along with their unsigned versions.
- **String types**: QString, std::string.

If a simple type is used, there must be exactly one parameter in the command line. If more than one parameter is provided, the program will crash with an error during execution.

If a parameter is parsed as a boolean type, the corresponding string must be a "truthy" or "falsy" value. The definitions of truthy and falsy values are as follows:

- If the parameter is "true", "yes", "y", "on", "1", "enable", these are considered true.
- If the parameter is "false", "no", "n", "off", "0", "disable", these are considered false.
- Any other value will cause the program to crash with an error.

If the type is defined as a numeric type, the program will attempt to parse the parameter into that type. If the parameter cannot be parsed into the numeric type or the parsed value exceeds the range of the type, the program will crash during execution.

Any parameter can be parsed into a string type without issues.

#### Composite Types

Composite types are list types such as QList, std::list, QVector, std::vector. The element type of the list is a simple type.

Additionally, the QStringList type is particularly noteworthy. It is essentially a specialization of QList<QString>. Users can use the QStringList type to receive any data.

### $CmdArgsDeclare and $CmdArgsNullable

#### $CmdArgsNullable

In the `$CmdArgs` above, the command line must have one or more parameters. However, in real-world scenarios, parameters can be optional, with default values or no input from the user.

For example, in IMakeCore's `ipc init` command, a script management file (either a .pro file or a CMakeLists.txt) is required. However, in a project, these two types of files may not coexist. In this case, we can default to initializing the existing file in the current directory, simplifying the command for the user. But if both files exist, the user must specify the file, such as `-- abc.pro` or `-- CMakeLists.txt`.

To support this scenario, we can add an optional parameter `$CmdArgsNullable` to the `$CmdArgs` macro annotation. The `$CmdArgsNullable` has one parameter, which is the name of the parameter defined in `$CmdArgs`.

For example, the following declaration:

=== "PrintCmd.h"

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"

    class PrintCmd : public ICmdInterface<PrintCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        PrintCmd();

    public:
        $CmdArgsNullable(args)
        $CmdArgsMemo(args, "argumets to be printed")
        $CmdArgs(QStringList, args)

    public:
        $CmdMappingMemo(print, "print arguments")
        $CmdMapping(print)
        void print();
    };
    ```

means that users can now execute the command without specifying parameters without encountering an error:

=== "No Arguments"

    ```bash
    PS D:\test\cmd> .\testCmd.exe print

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \_ __|

    ()

    ```

#### $CmdArgsDeclare

The `$CmdArgsDeclare` was seen in the `$CmdArgs` definition above. This macro is used to perform tasks beyond variable declaration.

The reason this macro is listed separately is that it can be used in conjunction with `$CmdArgsNullable`. The `$CmdArgsNullable` requires the parameter to have a default value, constructed by the default constructor. However, `$CmdArgsDeclare` allows users to define their own default values.

For example, the following declaration:

=== "PrintCmd.h"

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"

    class PrintCmd : public ICmdInterface<PrintCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        PrintCmd();

    public:
        $CmdArgsNullable(args)
        $CmdArgsMemo(args, "argumets to be printed")
        $CmdArgsDeclare(QStringList, args)
        QStringList args{"hello", "world"};

    public:
        $CmdMappingMemo(print, "print arguments")
        $CmdMapping(print)
        void print();
    };
    ```

If no arguments are input, the parameter will use the custom default value defined by the user. If arguments are provided, the parameter will take the input values.

=== "No Arguments"

    ```bash
    PS D:\test\cmd> .\testCmd.exe print

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \_ __|

    ("hello", "world")

    ```

=== "With Arguments"

    ```bash
    PS D:\test\cmd> .\testCmd.exe print -- abc def

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \_ __|

    ("abc", "def")


    ```

## $CmdArgsMemo

The `$CmdArgsMemo` is used to add comments to an argument set. It helps users better understand the meaning of the parameters.

Its first parameter is the name of the argument set, and the second parameter is the comment content. The comment content must be enclosed in double quotes, as shown in the code:

=== "PrintCmd.h $CmdArgsMemo"

    ```cpp
    $CmdArgsMemo(args, "argumets to be printed")
    ```

In the help output, it appears as follows:

=== "Help Output"

    ```bash
        [Args]:
            Name  TypeName     Nullable  Memo
            args  QStringList  false     argumets to be printed
    ```

## $CmdArgsPreHandle

The `$CmdArgsPreHandle` is used to execute a function before parameter parsing. Its usage is as follows:

=== "PrintCmd.h"

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"

    class PrintCmd : public ICmdInterface<PrintCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        PrintCmd();

    public:
        $CmdArgsNullable(args)
        $CmdArgsMemo(args, "argumets to be printed")
        $CmdArgsDeclare(QStringList, args)
        QStringList args{"hello", "world"};

        $CmdArgsPreHandle(args, argsPreHandle)
        void argsPreHandle();

    public:
        $CmdMappingMemo(print, "print arguments")
        $CmdMapping(print)
        void print();
    };
    ```

On lines 22 and 23, we define the `argsPostHandle` function, which is used to perform post-processing on the argument set values.

The `$CmdArgsPostHandle` can take one or two parameters.

- If two parameters are provided, the first is the name of the argument set, and the second is the function name.
- If one parameter is provided, it is the name of the argument set, and the function name defaults to the argument set name followed by "PostHandle".

The function must immediately follow the `$CmdArgsPostHandle` macro. The return type must be `void`, and the function can take one parameter of type `ICmdRequest&` or `const ICmdRequest&`. The parameter can be omitted.

The purpose of the PostHandle function is to validate and process the parameters. For example, we can verify the number of parameters or convert the parameter values.