# 单个命令行参数

在 $CmdArgs 文档中，我们将所有的命令行参数解析到一个成员变量中。如果有一个以上的参数，那么用户需要在 QList, 或 QStringList 等容器中手动获取参数，这种方式显得十分麻烦。

所以 $CmdArgX 机制提出了将参数精确的映射到自己的位置的方法, 比如将第一个参数映射成 src, 将第二个参数映射到 dest 这种方式。

## 示例

为了用户快速理解 $CmdArgX，我们写一个 CopyCmd 类， 这个类的作用是拷贝文件，将第一个参数指定的文件 拷贝到 第二个参数指定的路径下免去， 我简单写一个案例，不考虑复杂的处理, 也不执行具体的拷贝，就是让用户感知以下 $CmdArgX 的用法：

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
        $CmdArg1Memo("file which to be copied")
        $CmdArg1(QString, src)
    
        $CmdArg2Memo("path where accept a file copy to")
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
        qDebug() << "src path" << src;
        qDebug() << "dest path" << dest;
        quick_exit(0);
    }
    ```

或许用户会疑惑，这里并没有出现 $CmdArgX 这个宏注解，而是 $CmdArg1 和 $CmdArg2 两个宏注解。这是因为 $CmdArgX 中的 X 是一个数字，表示参数的位置，比如 $CmdArg1 表示第一个参数，$CmdArg2 表示第二个参数, 而且这里的 X 是大写的，更是方便用户识别。

在以下的各个说明中，我会会用 X 来代替具体的数值。

X 从 1-9 九个数字，用户用 $CmdArgX 最多能够处理9个参数。但我想这个对于绝大多数程序是足够的，没有什么程序会单独为9个以上的参数设置名称。

回到这个示例，这个示例中，我们用将第一个参数用 QString src 映射，第二个参数用 QString dest 映射。ICmd会自动解析并为这两个参数赋值。如果参数少于2个，程序在运行时会报错。如果多于2个，其他的参数在此类中会被忽略，因为用户也没定义如何处理多余的参数。如果用户想限定参数只能是两个，可以考虑使用 $CmdArgs 接收数据，并在相应的 $CmdArgsPostHandle 函数中进行判断处理。

下面是这个程序的一些运行结果：

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
        Index  Name  TypeName  Nullable  Memo
        1      src   QString   false     file which to be copied
        2      dest  QString   false     path where accept a file copy to
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
    
    src path "hello"
    dest path "world"
    ```

## $CmdArgX

$CmdArgX 注解的作用是将 X 位置的参数映射到自己的变量中。

$CmdArgX 是一类宏注解，用于定义参数的他的扩展形式有 $CmdArg1, $CmdArg2, $CmdArg3, $CmdArg4, $CmdArg5, $CmdArg6, $CmdArg7, $CmdArg8, $CmdArg9 九个。

该宏注解有两个参数。第一个参数是类型参数，第二个参数是名称参数。

其中参数类型有以下三类

- bool 类型。

- 数值类型，比如 short, int, long,long long 等和他们的 unsigned 形式，以及 double, float, 浮点类型。

- 字符串类型，比如 QString, std::string。

如果一个参数被解析为 bool 类型，那么他对应的字符串必须是 truthy 和 falsy 的。如下是对 truthy 和 falsy 的定义：

- 如果参数是  "true", "yes", "y", "on", "1", "enable"， 这些会被判断为 true
- 如果参数是  "false", "no", "n", "off", "0", "disable",这些会被判断为 false
- 如果除了这些值以外，其他的值 程序会报错。    

如果类型被定义成数值类型， 在参数解析的时候，会尝试将参数解析为该类型。如果参数不能够被解析为数值类型，或者解析的数值类型超过当前类型的范围。那么程序会在执行的时候报错。

任何参数类型都可以解析为字符串类型。

注意 $CmdArgX 不同于 $CmdArgs, 不能使用复合类型， 比如 QStringList, QList\<int\> 等这种类型。



## $CmdArgXMemo

$CmdArgXMemo 中只有一个参数，这个参数就是 注释的内容。注释内容需要使用双引号括起来。

不同于  $CmdArgsMemo, 这里不需要参数的名称，原因就是 X 已经指定了具体的位置，所以这个参数就省略了。

在上面的输出中，我们也看到了参数的具体的内容。

## $CmdArgXNullable

$CmdArgXNullable 指明该参数可以为空。如果没有这个修饰，那么这个参数则不能为空，如果缺失了 X 位置的参数，程序将会报错。

注意： 不同于 $CmdArgsNullable 是一个宏函数， $CmdArgXNullable 直接是一个 宏，不带任何参数。

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
        $CmdArg1Memo("file which to be copied")
        $CmdArg1(QString, src)
    
        $CmdArg2Nullable
        $CmdArg2Memo("path where accept a file copy to")
        $CmdArg2(QString, dest)
    
    public:
        $CmdMappingMemo(copy, "copy file command")
        $CmdMapping(copy)
        void copy();
    };
    ```

所以在这里 dest 参数可以为空。但是用户在这里需要在 copy 函数中进行判断，如可以使用当前目录作为 dest的值。

## $CmdArgXDeclare

这个的目的和 $CmdArgsDeclare 一致， 如果 $CmdArgXNullable 被声明于一个类中，$CmdArgXDeclare 则可以用来声明该参数的默认值。

如上面的代码，我们可以再次进行优化。

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
        $CmdArg1Memo("file which to be copied")
        $CmdArg1(QString, src)

        $CmdArg2Nullable
        $CmdArg2Memo("path where accept a file copy to")
        $CmdArg2Declare(QString, dest)
        QString dest{QDir::currentPath()};

    public:
        $CmdMappingMemo(copy, "copy file command")
        $CmdMapping(copy)
        void copy();
    };

    ```
    此时，如果我们再省略第二个参数， 那么 dest 的值就会是当前程序运行目录了。


## $CmdArgXPreHandle

$CmdArgXPreHandle 是定义在设置参数之前运行的一个函数。

他只有一个参数，这个参数就是他对应的函数名称。

函数的要求是返回值必须是 void 类型，可以有一个参数，参数类型是 ICmdRequest& 或  const ICmdRequest&。

函数必须紧跟在 $CmdArgXPreHandle 后面。

## $CmdArgXPostHandle

和 $CmdArgXPreHandle 类似， $CmdArgXPostHandle 定义在设置参数之后运行的一个函数。

他的要求和 $CmdArgXPreHandle 一样。

这里举一个例子，我们来验证以下 src 是否是一个文件。

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
        $CmdArg1Memo("file which to be copied")
        $CmdArg1(QString, src)

        $CmdArg1PostHandle(srcValidate)
        void srcValidate();

        $CmdArg2Nullable
        $CmdArg2Memo("path where accept a file copy to")
        $CmdArg2Declare(QString, dest)
        QString dest{QDir::dirName()};

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
            qDebug() << "src is not a file. src:" << src;
            quick_exit(1);
        }
    }

    void CopyCmd::copy()
    {
        qDebug() << "src path" << src;
        qDebug() << "dest path" << dest;
        quick_exit(0);
    }

    ```

在这个请求中，设置完 src 的值后，就会执行 srcValidate 函数，这个函数会检查 src 是否是一个文件。如果不是，程序会打印错误信息并退出， 程序不会再向下执行。
