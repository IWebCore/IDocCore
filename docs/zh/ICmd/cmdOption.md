# 命令行选项

> 本文档描述命令行选项

在 windows 命令行中，可以查看 dir 的命令如下：

=== "dir"

    ```bash
    C:\Users\Yue>dir /?
    显示目录中的文件和子目录列表。
    
    DIR [drive:][path][filename] [/A[[:]attributes]] [/B] [/C] [/D] [/L] [/N]
    [/O[[:]sortorder]] [/P] [/Q] [/R] [/S] [/T[[:]timefield]] [/W] [/X] [/4]
    
    [drive:][path][filename]
                指定要列出的驱动器、目录和/或文件。
    
    /A          显示具有指定属性的文件。
    属性         D  目录                R  只读文件
                H  隐藏文件            A  准备存档的文件
                S  系统文件            I  无内容索引文件
                L  重新分析点          O  脱机文件
                -  表示“否”的前缀
    /B          使用空格式(没有标题信息或摘要)。
    /C          在文件大小中显示千位数分隔符。这是默认值。用 /-C 来
                禁用分隔符显示。
    /D          跟宽式相同，但文件是按栏分类列出的。
    /L          用小写。
    /N          新的长列表格式，其中文件名在最右边。
    /O          用分类顺序列出文件。
    排列顺序     N  按名称(字母顺序)     S  按大小(从小到大)
                E  按扩展名(字母顺序)   D  按日期/时间(从先到后)
                G  组目录优先           -  反转顺序的前缀
    /P          在每个信息屏幕后暂停。
    /Q          显示文件所有者。
    /R          显示文件的备用数据流。
    /S          显示指定目录和所有子目录中的文件。
    /T          控制显示或用来分类的时间字符域
    时间段      C  创建时间
                A  上次访问时间
                W  上次写入的时间
    /W          用宽列表格式。
    /X          显示为非 8dot3 文件名产生的短名称。格式是 /N 的格式，
                短名称插在长名称前面。如果没有短名称，在其位置则
                显示空白。
    /4          以四位数字显示年份
    ```

他是有如此之多的选项。下面的内容，我们讲述 ICmd 中如何定义命令行选项。

ICore 中命令行选项为命令行参数的一种，它以`-`或`--`开头，后面跟着一个选项名，然后可以跟着一个参数值。

它为命令的执行提供指导，使得命令的执行更加灵活、可控。

## 示例

这里我们也定义一个 dir 的命令作为示例，讲述如何定义命令行选项。注意这里我不会去实现具体的功能，只作为讲清楚命令行选项的工具。

=== "MyDirCmd.h"

    ```cpp
    #pragma once
    
    #include "cmd/ICmdInterface.h"
    
    class MyDirCmd : public ICmdInterface<MyDirCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        MyDirCmd();
    
        $CmdOptionMemo(recurse, "recurse list subdirectory")
        $CmdOption(recurse)
    
        $CmdOptionMemo(time, "print create time")
        $CmdOption(time)
    
    public:
        $CmdMapping(mydir)
        void mydir();
    };
    
    ```

=== "MyDirCmd.cpp"

    ```cpp
    #include "MyDirCmd.h"
    
    MyDirCmd::MyDirCmd()
    {
    
    }
    
    void MyDirCmd::mydir()
    {
        qDebug() << "recurse:" << recurse;
        qDebug() << "time:" << time;
    }
    
    ```

我们直接列出他们的输出

=== "-?"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -?
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        testCmd.exe mydir
    [Options]:
        Option     ShortName  Required    NoValue    Memo
        --recurse  -          false       false      recurse list subdirectory
        --time     -          false       false      print create time
    ```

=== "没有选项"

    ```bash
    
    PS D:\test\cmd> .\testCmd.exe mydir
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: false
    time: false
    ```

=== "--recurse"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir --recurse
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: true
    time: false
    ```

=== "--time"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir --time
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: false
    time: true
    ```

=== "--recurse --time"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir --recurse --time
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: true
    time: true
    ```

=== "--recurse --time --abc"

    ```bash
    
    PS D:\test\cmd> .\testCmd.exe mydir --recurse --time --abc
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    ERROR OCCURED: your input options are not defined in this cmd. [Option]: --abc [Cmd Path]: mydir
    [CMD]:
        testCmd.exe mydir
    [Options]:
        Option     ShortName  Required    NoValue    Memo
        --recurse  -          false       false      recurse list subdirectory
        --time     -          false       false      print create time
    
    ```

这里请注意最后一个请求，我们输入了不存在的选项，ICmd 会提示错误信息。也就是说用户所能使用的选项必须是已经定义的选项。


## $CmdOption

$CmdOption 用于定义命令行选项，该宏注解只有一个参数，就是选项名称。注意这里的选项名称是全称，在后续有简称可以定义。

这里不用定义选项数据类型的原因也很简单，一个选项只有两种状态，存在或者不存在，没有薛定谔的猫问题。所以我们不需要定义数据类型，数据类型直接是 bool 类型， 并且这个参数默认是不存在的， 值为 false。如果用户在命令行中使用了该参数，则它的值将变为 true。

选项后面可以跟随选项参数，这里选项的参数内容将在下一篇文档中进行讲解。


## $CmdOptionShortName

一个选项的名称可以很长，能够完整表述出该选项的意义，用户不需要靠猜测，也可以不看 Memo。 但是很长的选项会让用户的输入变得困难。所以我们使用 $CmdOptionShortName 来定义一个选项的简称。

$CmdOptionShortName 只有两个参数，第一个参数是选项的全称，第二个参数是选项的简称。

如下，我们改造上面的示例：

=== "MyDirCmd.h"

    ```cpp
    #pragma once
    
    #include "cmd/ICmdInterface.h"
    
    class MyDirCmd : public ICmdInterface<MyDirCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        MyDirCmd();
    
        $CmdOptionShortName(recurse, r)
        $CmdOptionMemo(recurse, "recurse list subdirectory")
        $CmdOption(recurse)
    
        $CmdOptionShortName(time, t)
        $CmdOptionMemo(time, "print create time")
        $CmdOption(time)
    
    public:
        $CmdMapping(mydir)
        void mydir();
    };
    
    ```

=== "MyDirCmd.cpp"

    ```cpp
    #include "MyDirCmd.h"
    
    MyDirCmd::MyDirCmd()
    {
    
    }
    
    void MyDirCmd::mydir()
    {
        qDebug() << "recurse:" << recurse;
        qDebug() << "time:" << time;
    }
    
    ```

上面的示例中，我们为 resurse 选项和  time 选项定义了简称， r 和 t。

此时用户的请求就可以使用简称来输入选项了。



=== "-r"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -r
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: true
    time: false
    ```

=== "-t"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -t
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: false
    time: true
    ```

=== "-r -t"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -r -t
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: true
    time: true
    ```

而此时我们的帮助也有所变化

=== "变化后的帮助"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -?
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        testCmd.exe mydir
    [Options]:
        Option     ShortName  Required    NoValue    Memo
        --recurse  -r         false       false      recurse list subdirectory
        --time     -t         false       false      print create time
    
    ```


=== "变化前的帮助"

    ```bash
    
    PS D:\test\cmd> .\testCmd.exe mydir -?
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        testCmd.exe mydir
    [Options]:
        Option     ShortName  Required    NoValue    Memo
        --recurse  -          false       false      recurse list subdirectory
        --time     -          false       false      print create time
    ```

两者想对比，ShortName 的内容被填充上了。

## $CmdOptionMemo

$CmdOptionMemo 用于定义选项的说明，该宏注解有两个参数，第一个参数是选项名称，第二个参数是选项的说明。选项的说明必须是双引号括起来的内容。




## $CmdOptionRequired

$CmdOptionRequired 有一个参数，这个参数就是选项名称。

$CmdOptionRequired 用于定义选项为必填项，如果用户没有输入该选项，则命令行会报错。

这个选项后面一般会跟着相应的参数。如果一个选项是必填项，而没有跟随参数，这个参数也没多大意思，它的值是固定的，那么为什么还需要这个参数呢？

举个例子，如果我们做认证的工作，那么 --name  和 --password  这两个选项一定是必填项，这样就能够保证用户输入了用户名和密码。

关于 选项参数，请参考下篇内容。

## $CmdOptionNoValue

这个注解有一个参数，参数内容就是选项名称。

该注解的目的是告知 ICmd 这个选项没有任何参数，如果有参数，则是用户输入错误，程序需要报错提示用户。

举个例子，在 mydir 命令中，我们定义了一个选项 --recurse，这个选项就不应该有任何参数，如果用户输入了 --recurse 而有后续参数，则程序需要报错提示用户。
