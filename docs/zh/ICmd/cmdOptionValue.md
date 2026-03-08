# 命令行选项参数

> 本文档描述命令行选项参数

## 简介

一个命令行选项可以有一系列的参数来进一步描述这个选项。我们以 copy 命令为例，如果用户定义了 --src 选项，那么这个选项就应该有一个参数来告知 src 的内容是什么。

## 示例

我们假设一个场景，用户打印输出内容，而在命令行中可以通过选项来配置哪些内容可以被输出。

如下是一段代码：



=== "OutputCmd.h"

    ```cpp
    #pragma once
    
    #include "cmd/ICmdInterface.h"
    
    class OutputCmd : public ICmdInterface<OutputCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        OutputCmd();
    
        $CmdOption(type)
    
        $CmdOptionValue(type, QStringList, printType)
    
    public:
        $CmdMapping(output)
        void output();
    };
    ```

=== "OutputCmd.cpp"

    ```cpp
    #include "OutputCmd.h"
    
    OutputCmd::OutputCmd()
    {
    
    }
    
    void OutputCmd::output()
    {
        qDebug() << type;
        qDebug() << printType;
        quick_exit(0);
    }
    ```

上述的示例很简单，我们定义了一个 type 的选项，并定义了一个基于 type 选项的 选项参数 printType, printType 是一个 QStringList 类型，用来指定输出内容的类型，也就是 --type 选项后面可以跟多个参数, 这些参数都会被放置在 printType 变量中。

下面是一些调用示例：

=== "-?"

    ```bash
    
    PS D:\test\cmd> .\testCmd.exe output -?
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        testCmd.exe output
    [Options]:
        Option  ShortName  Required    NoValue    Memo
        --type  -          false       false
    [OptionValues]:
        Option  Name       TypeName     Nullable  Memo
        type    printType  QStringList  false
    
    ```

=== "不带选项参数"

    ```bash
    PS D:\test\cmd> .\testCmd.exe output --type
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    cmd defined option value and option value should not be null, but you do not provide option value. [OptionValue]:type
    [CMD]:
        testCmd.exe output
    [Options]:
        Option  ShortName  Required    NoValue    Memo
        --type  -          false       false
    [OptionValues]:
        Option  Name       TypeName     Nullable  Memo
        type    printType  QStringList  false
    
    ```

=== "带选项参数"

    ```BASH
    PS D:\test\cmd> .\testCmd.exe output --type name "create time" detail
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    true
    ("name", "create time", "detail")
    
    ```

在上述的调用中，第一个示例看见选项参数已经被注册进去，第二个示例看见没有提供选项参数，此时程序会报错，第三个示例看见提供了选项参数，程序正常运行。

下面我们逐一来讲解选项参数的内容。

## $CmdOptionValue

该注解用于定义选项参数，如上面的示例中的 printType 选项参数。

```cpp
$CmdOptionValue(type, QStringList, printType)
```

$CmdOptionValue 注解有三个参数，分别是：

- 选项名：type。

选项名声是我们定义的选项名，这个是必须存在的选项。如果该选项不存在，程序在解析的时候会报错。

- 选项参数类型：QStringList

这个参数的类型和我们定义 命令行参数的类型的格式一致，用法一致。

它的类型可以是 bool 类型，数值类型， 字符串类型 和复合类型，相关的内容可以参考 参数类型的文档。

- 选项参数变量名：printType

这个是用于存放选项参数的成员变量名称。



## $CmdOptionValueMemo

这个是对 选项参数的一个注释。$CmdOptionValueMemo 的第一个参数是选项参数名称，第二个参数是注释。注释需要使用双引号括起来。



## $CmdOptionValueNullable

该注解用于定义选项参数是否可以为空。在上面的示例中，当我们定义选项参数，而没有输入选项参数的时候，程序会在执行中会报错。而当 `$CmdOptionValueNullable` 注解被使用的时候，此时就不会报错，该选项参数会使用默认值来进行操作。

该宏注解可以单独使用，但如果我们希望有用户定义的默认值的时候，可以考虑和 `$CmdOptionDeclare` 一起使用。



## $CmdOptionValueDeclare

该类用于定义选项参数的默认值。 当该选项参数被`$CmdOptionValueNullable`注解， 并且在实际的请求中，也没有输入参数，那么这个注解所带来的默认值就会被使用。

举例：

=== "OutputCmd.h"

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"

    class OutputCmd : public ICmdInterface<OutputCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        OutputCmd();

        $CmdOption(type)

        $CmdOptionValueNullable(printType)
        $CmdOptionValueDeclare(type, QStringList, printType)
        QStringList printType{"name", "time"};
        
    public:
        $CmdMapping(output)
        void output();
    };

    ```

在这这程序中，如果用户的命令是 `some-exe output --type`， 那么程序会使用默认值 "name" 和 "time" 作为选项参数。

而如果用户指定了选项参数，如 `some -exe output --type name "create time" detail`， 此时选项参数就是 "name" 和 "create time" 和 "detail" 而不是默认值。


## $CmdOptionPreHandle

这个定义在选项参数之前的处理函数。ICmd 在给选项设置值的时候，会提前运行该函数(如果函数定义的话)。

其他的内容参考 $CmdArgsPreHandle 等注解。

## $CmdOptionPostHandle

这个定义在选项参数之后的处理函数。ICmd 在给选项设置值的时候，会在设置值之后运行该函数(如果函数定义的话)。

其他的内容参考 $CmdArgsPostHandle 等注解。

这里比如用户想确保选项参数是在一组名称里面选择，而不是随便怎么输入参数都可以，那么可以为该选项参数设置一个PostHandle 函数，在函数内部对参数进行校验。