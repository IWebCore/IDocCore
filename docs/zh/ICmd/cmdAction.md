# 定义命令

> 本文档描述如何定义命令。

## 示例

我们将 [指南](./overview.md) 中的 VersionCmd 示例照搬下来，之后对于 Cmd 如何定义命令行，我们以此为基础进行讲解。

为防止用户忘记该代码是什么样子，誊抄如下：

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
定义一个Cmd类必须继承于 `ICmdInterface`。

`ICmdInterface` 的类位于 `ICmd 包`中的 `cmd/ICmdInterface.h` 路径下面。用户必须在类中引用该头文件

=== "头文件引用"
    ```cpp
    #include "cmd/ICmdInterface.h"
    ```

<br>
`ICmdInteface` 是一个 `CRTP` 模板基类，他的定义如下：

=== "ICmdInteface 类的定义"

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

`ICmdInteface` 基类中的父类不需要关心，这里要关心的是 `ICmdInteface` 的两个模板参数 `T` 和 `enabled`。

<br>

模板的第一个参数 `typename T`是我我们要实现的子类的名称。比如 VersionCmd 中的 ICmdInterface 的参数就是 VersionCmd

=== "VersionCmd 类的定义"
    ```cpp
    class VersionCmd : public ICmdInterface<VersionCmd>
    ```

<br>

模板参数的第二个参数 bool enabled 默认值为 true，表示该 Cmd 是否启用。如果设置为 false，则该 Cmd 将不会使用。

用户一般不需要设定该值，但是如果用户想禁用该类，比删除该类更好的办法就是在类定义中将 enabled 设置为 false。

比如我们如果不想使用 VersionCmd，可以这样定义：

=== "禁用 VersionCmd"
    ```cpp
    class VersionCmd : public ICmdInterface<VersionCmd, false>
    ```

这样用户就不能在使用该 Cmd 了。


## Q_GADGET

`Q_GADGET` 是一个宏，用于声明一个类为 `Qt 元类型`。经过 `Q_GADGET` 声明的类可以通过 Qt 的元系统进行反射，而获取到类的额外信息，这些信息将会被使用于我们对命令和参数以及选项的解析过程中。

更多关于 `Q_GADGET` 的信息，请参考 Qt 官方文档。

## $AsCmd

`$AsCmd` 是一个宏注解。这个宏注解的作用一个是用于帮助程序更好的进行反射。另外一个作用是定义一个前置命令路径。

一个完整的命令行是有 程序名称， $AsCmd 定义的前置命令路径，和 $CmdMapping 定义的命令路径组合而成的。

在`$AsCmd` 中，用户如果不想使用前置命令，则可以 将宏的参数输入为 `/`。 

如上我们的 VersionCmd 因为将 `$AsCmd` 中的参数设置为 `/`， 此时 他解析出来的路径就是 `some-exe version`，`some-exe` 是程序的名称

如果设置的内容不为  `/`， 比如，`abc`

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

那么此时该命令行的路径就是 `some-exe abc version`

<br>
用户可以设置多个命令前缀。各个命令前置使用 `,` 分隔。比如我们设置 `abc def, ghi` 这种参数

=== "$AsCmd(abc def, ghi)"
    ```
    #pragma once

    #include "cmd/ICmdInterface.h"
    
    class VersionCmd : public ICmdInterface<VersionCmd>
    {
        Q_GADGET
        $AsCmd(abc， def, ghi)
    public:
        VersionCmd();
    
    public:
        $CmdMappingMemo(version, "print imakecore version info")
        $CmdMapping(version)
        void version();
    };
    ```
此时该命令行的路径就是 `some-exe abc def version`。

## $CmdMapping

`$CmdMapping` 是用于定义具体的命令函数的。 比如在 CmdVersion 中，我们定义了一个 version 的 $CmdMapping 和函数：

=== "$CmdMapping(version)"

    ``` 
        //...
        $CmdMapping(version)
        void version();
        //...
    ```

### 映射函数

这里 $CmdMapping 宏注解有一个参数，参数的内容必须是响应函数的名称， 宏注解后面必须跟随响应的函数。

如果 $CmdMapping 后面没有跟随函数，则程序在运行前会报错，如果函数的名称和宏注解中的第一个参数不一致，则程序在运行的时候页会报错。

对于响应函数，ICmd 也有要求：

- 该响应函数的返回值必须是 void 类型，不能够是其他任何类型的返回值。

- 该响应函数可以没有参数，如果有参数，则参数类型必须是  ICmdRequest& 或 const ICmdRequest& 类型。

### 映射路径

$CmdMapping 的映射路径有以下的情况

#### 默认映射路径

如果$CmdMapping 只有一个参数，就像例子中的 `version`  一样，那么这个参数既是 函数名称，也是映射路径。

也就是说在这个例子中 `$CmdMapping(version)` 定义了一个 `version` 的映射函数，这个映射函数的映射路径是 `version`。

 一个完整的命令行是有 `程序名称`， `$AsCmd` 定义的前置命令路径，和 `$CmdMapping` 定义的命令路径组合而成的。所以这些组合起来，就是 `some-exe version` 这个命令的由来。



#### 自定义映射路径

用户也可以自定义命令。

`$CmdMapping` 一共可以有9个参数。如果参数超过一个。那么从第二个参数开始的参数列表就是 `$CmdMapping` 所定义的映射路径。

所以 `$CmdMapping(version)` 和 `$CmdMapping(version, version)` 这两种定义方式是等价的。

如果 这个定义是 `$CmdMapping(version, abc, def, ghi)` ，那么 $CmdMapping 定义的路径就是 `abc def ghi` ，这个路径再结合 `$AsCmd` 所定义的路径，就是整个映射函数的完整路径。

#### `/` 映射路径

`$CmdMapping` 的参数可以是 `/`， 这个表示 `$CmdMapping` 没有定义路径，那么此时映射函数的路径就是  `$AsCmd` 所定义的路径。

所以 `VersionCmd.h` 可以书写为如下格式，他和一开始定义的 `VersionCmd.h` 是等价的

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

`$CmdMappingMemo` 用于定义命令的描述信息，这个信息会在程序帮助中进行输出。

$CmdMappingMemo 的第一个参数必须是我们的映射函数的名称。第二个参数是一个用 双引号括起来的字符串，就如在示例中所描述的。

=== "$CmdMappingMemo"

    ```cpp
        $CmdMappingMemo(version, "print imakecore version info")	
    ```



此时，如果我们 使用命令  `some-exe version  -?` 命令查看该内容，就可以看到相关的输出

=== "some-exe version -? 输出"

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

## 一个类中定义多个命令

一个 Cmd 类可以定义多个命令。每一个命令都必须由 $CmdMapping 定义。

比如我们可以定义一个 `add` 和 `sub` 命令。

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

在上面的示例中，我们在一个类中定义了两个命令。`some-exe addsub add` 和 `some-exe addsub sub` 这两个命令分别调用了 `AddSubCmd` 类中的 `add` 和 `sub` 函数。

但是在实际的应用中，非常不建议这么定义。因为在一个类中，不仅有命令的定义，还有参数和选项的内容。一个类中定义的命令会同时共享选项和参数。

所以，我们推荐一个命令一个类。

但是还有一些例外的事情，比如我 定义了一个  `some-exe package list` 的名命令，那么我想以 `some-exe list` 作为其简写方式。 这样的情况就可以定义两个映射函数，而在其中一个映射函数中调用另外一个映射函数。

