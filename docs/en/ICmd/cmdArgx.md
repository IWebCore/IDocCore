<译文内容>  
# Single Command Line Argument  

In the `$CmdArgs` documentation, all command line arguments are parsed into a single member variable. If there are multiple arguments, the user must manually retrieve them into containers like `QList` or `QStringList`, which can be cumbersome.  

Therefore, the `$CmdArgX` mechanism introduces a method to precisely map arguments to specific positions. For example, the first argument can be mapped to `src`, and the second argument to `dest`.  

## Example  

To help users quickly understand `$CmdArgX`, let's create a `CopyCmd` class. This class is designed to copy files, mapping the first argument to a source file and the second argument to the destination path. For simplicity, I'll write a minimal example without complex processing or actual file copying, just to demonstrate the usage of `$CmdArgX`:  

=== "CopyCmd.h"  

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"
    
    class CopyCmd : public ICmdInterface<CopyCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        CopyCmd();
    
    public:
        $CmdArg1Memo("file to be copied")
        $CmdArg1(QString, src)
    
        $CmdArg2Memo("destination path for the copied file")
        $CmdArg2(QString, dest)
    
    public:
        $CmdMappingMemo(copy, "copy file command")
        $CmdMapping(copy)
        void copy();
    };
    
    ```  

=== "CopyCmd.cpp"  

    ```cpp
    #include "CopyCmd.h"

    CopyCmd::CopyCmd()
    {
    
    }
    
    void CopyCmd::copy()
    {
        qDebug() << "Source path:" << src;
        qDebug() << "Destination path:" << dest;
        quick_exit(0);
    }
    ```  

Users might wonder why there are no `$CmdArgX` annotations but rather `$CmdArg1` and `$CmdArg2`. This is because `$CmdArgX` uses an uppercase X to denote the position of the parameter, such as `$CmdArg1` for the first argument and `$CmdArg2` for the second. This uppercase X makes it easier for users to identify.  

In the following explanations, I'll use X to represent a specific number.  

X can range from 1 to 9, allowing users to handle up to 9 parameters with `$CmdArgX`. I believe this is sufficient for most programs, as it's rare for any program to need named handling for more than 9 parameters.  

Back to the example, we map the first argument to a `QString src` and the second argument to a `QString dest`. The `ICmd` system will automatically parse and assign values to these parameters. If fewer than two arguments are provided, the program will throw an error at runtime. If more than two arguments are provided, the extra ones will be ignored since they are not defined in the class. If the user wants to enforce exactly two parameters, they can use `$CmdArgs` to receive the data and handle any excess in the `$CmdArgsPostHandle` function.  

Here are some example outputs from running the program:  

=== "help -?"  

    ```bash
    PS D:\test\cmd> .\testCmd.exe copy -?

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        testCmd.exe copy
    [Memo]:
        copy file command
    [Argx]:
        Index  Name  Type      Nullable  Memo
        1      src   QString   false     file to be copied
        2      dest  QString   false     destination path for the copied file
    ```  

=== "copy file"  

    ```bash
    PS D:\test\cmd> .\testCmd.exe copy -- hello world
    
    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    Source path: "hello"
    Destination path: "world"
    ```  

## `$CmdArgX`  

The purpose of the `$CmdArgX` annotation is to map the X-th argument to a specific variable.  

`$CmdArgX` is a macro annotation used to define parameters. It has variants such as `$CmdArg1`, `$CmdArg2`, ..., `$CmdArg9`.  

This macro annotation takes two parameters: the first is the type parameter, and the second is the name parameter.  

The parameter types fall into three categories:  

- **Boolean type**: The corresponding string must be a truthy or falsy value. Truthy values include "true", "yes", "y", "on", "1", "enable", which are interpreted as `true`. Falsy values include "false", "no", "n", "off", "0", "disable", which are interpreted as `false`. Any other value will cause an error.  

- **Numeric type**: Such as `short`, `int`, `long`, `long long`, and their unsigned counterparts, as well as `double` and `float`. During parsing, the argument is attempted to be converted to the specified numeric type. If the conversion fails or the value is out of range, the program will throw an error at runtime.  

- **String type**: Such as `QString` or `std::string`. Any parameter type can be parsed as a string.  

Note: `$CmdArgX` differs from `$CmdArgs` in that it does not support composite types, such as `QStringList` or `QList<int>`.  

## `$CmdArgXMemo`  

The `$CmdArgXMemo` annotation has one parameter, which is the memo content, enclosed in double quotes.  

Unlike `$CmdArgsMemo`, there is no need to specify the parameter name here because X already indicates the specific position.  

In the output above, you can also see the memo content for each parameter.  

## `$CmdArgXNullable`  

The `$CmdArgXNullable` annotation indicates that the parameter can be null. If this annotation is omitted, the parameter cannot be null, and the program will throw an error if the X-th argument is missing.  

Note: Unlike `$CmdArgsNullable`, which is a macro function, `$CmdArgXNullable` is a macro without any parameters.  

=== "CopyCmd.h"  

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"
    
    class CopyCmd : public ICmdInterface<CopyCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        CopyCmd();
    
    public:
        $CmdArg1Memo("file to be copied")
        $CmdArg1(QString, src)
    
        $CmdArg2Nullable
        $CmdArg2Memo("destination path for the copied file")
        $CmdArg2(QString, dest)
    
    public:
        $CmdMappingMemo(copy, "copy file command")
        $CmdMapping(copy)
        void copy();
    };
    ```  

In this example, the `dest` parameter can be null. However, the user needs to handle this case in the `copy` function, such as using the current directory as the default destination.  

## `$CmdArgXDeclare`  

This serves the same purpose as `$CmdArgsDeclare`. If `$CmdArgXNullable` is declared in a class, `$CmdArgXDeclare` can be used to specify a default value for the parameter.  

For example, in the code above, we can further optimize:  

=== "CopyCmd.h"  

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"

    class CopyCmd : public ICmdInterface<CopyCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        CopyCmd();

    public:
        $CmdArg1Memo("file to be copied")
        $CmdArg1(QString, src)

        $CmdArg2Nullable
        $CmdArg2Memo("destination path for the copied file")
        $CmdArg2Declare(QString, dest)
        QString dest{QDir::currentPath()};

    public:
        $CmdMappingMemo(copy, "copy file command")
        $CmdMapping(copy)
        void copy();
    };

    ```  
    Now, if the second argument is omitted, the `dest` parameter will default to the current directory.  

## `$CmdArgXPreHandle`  

The `$CmdArgXPreHandle` is a function that runs before setting the parameter value. It takes one parameter, which is the function name.  

The function must return `void` and can have one parameter of type `ICmdRequest&` or `const ICmdRequest&`.  

The function must be placed immediately after `$CmdArgXPreHandle`.  

## `$CmdArgXPostHandle`  

Similar to `$CmdArgXPreHandle`, `$CmdArgXPostHandle` is a function that runs after setting the parameter value. It has the same requirements as `$CmdArgXPreHandle`.  

Here's an example to verify if `src` is a valid file:  

=== "CopyCmd.h"  

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"

    class CopyCmd : public ICmdInterface<CopyCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        CopyCmd();

    public:
        $CmdArg1Memo("file to be copied")
        $CmdArg1(QString, src)

        $CmdArg1PostHandle(srcValidate)
        void srcValidate();

        $CmdArg2Nullable
        $CmdArg2Memo("destination path for the copied file")
        $CmdArg2Declare(QString, dest)
        QString dest{QDir::currentPath()};

    public:
        $CmdMappingMemo(copy, "copy file command")
        $CmdMapping(copy)
        void copy();
    };

    ```  

=== "CopyCmd.cpp"  

    ```cpp
    #include "CopyCmd.h"

    CopyCmd::CopyCmd()
    {
    
    }

    void CopyCmd::srcValidate()
    {
        if(!QFileInfo(src).exists()){
            qDebug() << "Source is not a file. Source:" << src;
            quick_exit(1);
        }
    }

    void CopyCmd::copy()
    {
        qDebug() << "Source path:" << src;
        qDebug() << "Destination path:" << dest;
        quick_exit(0);
    }

    ```  

In this example, after setting the value of `src`, the `srcValidate` function is executed to check if `src` is a valid file. If not, an error message is printed, and the program exits without further execution.