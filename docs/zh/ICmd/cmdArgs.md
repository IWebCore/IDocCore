# 命令行参数集

> 本文档描述如何处理参数集

一个命令行不仅有命令，也需要有参数。CmdArgs 是一个命令行参数集，它可以解析命令行参数，并提供方便的接口来获取参数的值。

## 命令行中参数的规则

在 ICmd 命令中，命令行参数的规则如下：

- 参数是有双横杠`-- ` 后面跟随一个个参数而来。注意 `--` 和参数之间`要有间隔`，不能连在一起，连在一起会被解析为 选项，而不再是参数。
- 参数可以有一个或者多个。 多个参数之间要有`空格`间隔
- 如果单个参数中间本身有空格，则参数需要有双引号括起来。

如下是合法的参数

```bash
-- abc
-- 123
-- true
-- false
-- abc 124 true hello
-- "c:/program files/hello/world"
```

## 示例 

为了示例程序，我们创建一个testCmd项目，定义一个 PrintCmd类，代码如下：
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

运行此程序。有如下输出结果：

=== "-? 帮助"
    
    ```bash
    D:\test\cmd>testCmd.exe print -?
    
    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        testCmd.exe print
    [Memo]:
        print arguments
    [Args]:
        Name  TypeName     Nullable  Memo
        args  QStringList  false     argumets to be printed
    ```
    此时输出的是帮助信息

=== "一个参数"
    ```bash
    D:\test\cmd>testCmd.exe print -- hello

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    ("hello")
    ```

=== "多个参数"
    ```bash
    D:\test\cmd>testCmd.exe print -- hello world

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    ("hello", "world")
    
    ```


=== "带空格的参数"

    ```bash
    D:\test\cmd>testCmd.exe print -- hello world "hello world"
    
    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    ("hello", "world", "hello world")
    
    ```

=== "没有参数的情况"
    ```bash

    D:\test\cmd>testCmd.exe print --
    
    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    ERROR OCCURED: Args is defined not empty, but the cmd request arguments is empty [Action Path]: print [Value Name]: args [Cmd Path]: print [Cmd Arg Type]: Args [Cmd Arg Values]:
    
    [CMD]:
        testCmd.exe print
    [Memo]:
        print arguments
    [Args]:
        Name  TypeName     Nullable  Memo
        args  QStringList  false     argumets to be printed
    
    ```

在上面的示例中，可以观察到各种情况的输出内容。

## $CmdArgs

$CmdArgs 宏注解用于声明一个参数集。宏注解一共有两个参数，第一个参数是想解析的数据类型，第二个参数是参数集的名称。在之后的程序处理过程中，用户将使用这个名称来获取参数集的值。

注意一点，这里一直在说参数集，而不是参数，这个是因为我们定义有  $CmdArg1, $CmdArgs 这样的 类似于 $CmdArgX 的单独参数处理。用户可以在后续的章节中看到。

$CmdArgs 的名称必须是一个合法的类字段名称。这个是因为 $CmdArgs 宏注解会在类中生成一个成员变量，这个成员变量的名称就是 $CmdArgs 后面跟的名称。它实的定义内容如下：

=== "$CmdArgs 的定义"
    ```cpp
    #define $CmdArgs(TYPE, NAME)                                            \
        $CmdArgsDeclare(TYPE, NAME)                                          \
        TYPE NAME {};
    ```

它会用第一个参数`类型`和第二个参数`名称`来声明一个类内成员变量。

### 参数类型

在 ICmd 中可用的成员类型可以分为如下的两类，简单类型和复合类型。

#### 简单类型

简单类型包括如下几种：

- bool 类型

- 数值类型: short/int/long/long long/float/double, 以及它们的 unsigned 版本。

- string 类型：QString, std::string。

如果用户使用的是简单类型，那么这里要求用户在命令行中的只能有一个参数。如果参数数量超过一个，那么程序会在运行时报错。

如果一个参数被解析为 bool 类型，那么他对应的字符串必须是 truthy 和 falsy 的。如下是对 truthy 和 falsy 的定义：

- 如果参数是  "true", "yes", "y", "on", "1", "enable"， 这些会被判断为 true
- 如果参数是  "false", "no", "n", "off", "0", "disable",这些会被判断为 false
- 如果除了这些值以外，其他的值 程序会报错。    

如果类型被定义成数值类型， 在参数解析的时候，会尝试将参数解析为该类型。如果参数不能够被解析为数值类型，或者解析的数值类型超过当前类型的范围。那么程序会在执行的时候报错。

任何参数都可以解析为字符串类型，这个没有问题。


#### 复合类型

复合类型是 QList/ std::list / QVector / std::vector 的列表类型。列表类型的参数类型是上述简单类型。

另外，QStringList 类型特别点出。他其实是 QList<QString> 类型的一种特化。用户可以用 QStringList 类型来接收一切的数据。


### $CmdArgsDeclare 和 $CmdArgsNullable

#### $CmdArgsNullable
在上面的 $CmdArgs 中，命令行必须有一个和一个以上的参数。在实际的情况中，参数可以是默认的，可以没有参数，而参数的值是被提前指定的，或者被用户默认的。

比如在 IMakeCore 中 的 `ipc init` 命令中需要有管理脚本，不管是 pro 文件或者 CMakeLists.txt 文件等。但在一个项目中这两种类型文件不一定会同时存在。那么我们就可以默认为，ipc init 是是初始化 当前文件夹中存在的那个文件，这样用户就可以少些很多内容，简化命令。但是如果同时存在，那么此时用户就需要指定文档，比如 `-- abc.pro` 或者 `-- CMakeLists.txt`。

为了支持这种情况，我们需要在 $CmdArgs 宏注解中增加一个可选参数 $CmdArgsNullable。$CmdArgsNullable 只有一个参数，就是在 $CmdArgs中定义的第二个参数，参数名称。

比如我们有如下的声明：

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

那么此时用户就可以不指定参数，此时用户就可以执行如下命令而不报错了：

=== "没有参数的情况"
    ```bash
    PS D:\test\cmd> .\testCmd.exe print

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    ()
    
    ```

#### $CmdArgsDeclare

$CmdArgsDeclare 在上面的 $CmdArgs 的定义中见过。这个内容是用于完成除了声明变量之外的工作。

这个宏注解在这里单独列出的原因是它可以配合 $CmdArgsNullable 一起使用。$CmdArgsNullable 要求参数必须有默认值，而且必须是默认构造而来。而 $CmdArgsDeclare 则可以用来声明用户自己想要的默认值。

比如我们有如下的声明：

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

此时，如果我们没有输入参数，那么参数就会使用我们自定义的默认值，而我们输入参数了，那么参数则是我们输入的值。

=== "没有参数"
    ```bash
    PS D:\test\cmd> .\testCmd.exe print

    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    ("hello", "world")
    
    ```

=== "有参数"

    ```bash
    PS D:\test\cmd> .\testCmd.exe print -- abc def
    
    _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
    | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
    | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    ("abc", "def")


    ```

## $CmdArgsMemo
$CmdArgsMemo 用于给参数集添加注释。它可以帮助用户更好的理解参数的含义。

她的第一个参数是参数集的名称，第二个参数是注释内容。其中注释内容必须使用双引号括起来。就如我们代码中所描述的：

=== "PrintCmd.h $CmdArgsMemo"
```cpp
$CmdArgsMemo(args, "argumets to be printed")
```

在帮助输出中他的输出内容会如下：

=== "帮助输出"
    ```bash
        [Args]:
            Name  TypeName     Nullable  Memo
            args  QStringList  false     argumets to be printed
    ```

## $CmdArgsPreHandle

$CmdArgsPreHandle 用于在参数解析之前执行的函数。他的使用方式如下：

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

在第18，19 行，我们定义了 CmdPreHandle 函数。这个函数的作用是将参数集的值进行预处理。

$CmdArgsPreHandle 的参数可以是一个或者两个。

如果参数是两个的话，第一个参数是 参数集的名称，第二个参数是函数名称。

如果只有一个的话，参数是 参数集的名称，而函数默认是 参数集的名称 + "PreHandle" 这个名称。

函数必须紧跟  $CmdArgsPreHandle 后面。函数的返回值必须是 void, 函数可以有一个参数, 参数类型必须是 `ICmdRequest&` 或 `const ICmdRequest&` 类型，参数也可以省略。

## $CmdArgsPostHandle

$CmdArgsPostHandle 用于在参数解析之后执行的函数。他的使用方式如下：

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
    
        $CmdArgsPostHandle(args, argsPostHandle)
        void argsPostHandle();
    
    public:
        $CmdMappingMemo(print, "print arguments")
        $CmdMapping(print)
        void print();
    };
    
    ```

在第22，23 行，我们定义了 CmdPostHandle 函数。这个函数的作用是将参数集的值进行后处理。

$CmdArgsPostHandle 的参数可以是一个或者两个。

如果参数是两个的话，第一个参数是 参数集的名称，第二个参数是函数名称。

如果只有一个的话，参数是 参数集的名称，而函数默认是 参数集的名称 + "PostHandle" 这个名称。

函数必须紧跟  $CmdArgsPostHandle 后面。函数的返回值必须是 void, 函数可以有一个参数, 参数类型必须是 `ICmdRequest&` 或 `const ICmdRequest&` 类型，参数也可以省略。

PostHandle 函数的作用是对参数的验证和后处理。比如，我们可以对参数的数量进行验证，或者对参数的值进行转换等。




