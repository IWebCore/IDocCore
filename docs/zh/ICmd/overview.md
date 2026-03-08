# ICmd 使用指南

## 描述

ICmd 是使用`宏注解`来定义命令行的工具，用于解析命令行，让用户免于复杂的命令行解析，流程流转控制，而专注于命令行的主要逻辑。

用户通过`宏注解`来定义处理函数，命令路径，参数，参数处理函数， 选项，选项处理函数等一系列内容，自动解析出这些内容。在执行具体的命令行时，ICmd自动匹配具体命令，并注入选项内容，参数内容，最后执行 处理函数。此时用户在处理函数的时候，所有的 参数，命令都已经被解析出来，用户可以使用这些参数和选项来处理具体的功能。

### 参考项目
用户可以参考 [IPubCore](https://github.com/IWebCore/IPubCmd) 来进一步了解使用方法 

## 案例

我们写一个简单的案例，来描述ICmd如何使用。

### 安装 ICmd
关于如何安装 ICmd，请参考 [安装 ICmd](install.md)。

如果想更多的了解包管理系统，请参考 [包管理系统](../IMakeCore/quick_start.md)。

### main.cpp

首先定义 main.cpp， main.cpp 的主要内容是启动一个 ICmdServer ,来接收，解析并执行 cmd.

=== "main.cpp"
    ```cpp
    #include "core/application/IApplication.h"
    #include "cmd/ICmdServer.h"

    int main(int argc, char *argv[])
    {
        IApplication a(argc, argv);

        ICmdServer server;
        server.serve();

        return a.run();
    }
    ```

ICmdServer 的具体功能是， 解析出 ICmdRequest 内容，匹配具体的某个路径的 ICmdAction，并执行 ICmdAction 的处理逻辑。

其中 ICmdRequest 是将命令行解析为 `路径`，`参数` 和`选项` 三个部分的内容。

ICmdAction是针对某个具体的 `路径` 的处理动作，而处理的包括，将参数和选项注入到定义的 `Cmd` 中去，如果`参数`和`选项`有定义预处理函数或后处理函数，则会执行预处理函数或后处理函数，最后执行 处理函数。



### 定义一个 Cmd

下面我们定义一个 VersionCmd。

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

在头文件中，我们定义了一个 Cmd 项， 

VersionCmd 通过CRTP继承 ICmdInterface。这个 ICmdInterface主要的内容就是解析Cmd,生成 CmdAction 内容，并注入到 ICmdManage 中去。这时如果 ICmdServer 匹配到这个 CmdAction, 这个类就会被执行。

`Q_GADGET` 的作用是使这个类能够被反射，知道它定义了什么 classinfo, property 和 method。这些信息会被组织起来成为 CmdAction 中的内容。

`$AsCmd(/)`注解说明两个事情，第一，这个使一个 Cmd 类。第二这个Cmd 的首个路径是 `/`。同时如果路径是 `/` 则这个路径会被忽略。

`$CmdMapping(version)` 是定义一个 Cmd 处理函数，它后面必须跟一个名称是 version 的函数。并且 CmdMapping也默认定义了一个路径 version， 所以这个cmd 会生成一个路径是 version 的 CmdAction.

`$CmdMappingMemo(version, "print imakecore version info")` 这个是给 version 作一个注解，这个注解会在用户打印这个 CmdAction 时输出。

在 `void version()` 函数中，不仅执行了具体的打印功能，还有一句值得注意 `quick_exit(0);` 这个的目的是退出整个程序。所以在 Cmd 书写过程中，用户执行完成功能后，必须手动退出程序。



### 使用该 Cmd

我们执行该命令，如下：

=== "IPubCmd verison"
    ![cmd version](assets/image-20250702212502579.png)

我们使用 -？打印一下它的介绍
=== "-? 帮助"
    ![cmd version help](assets/image-20250702212559976.png)

在上面我们看到了它的命令内容和我们写入的 Memo内容。用户可以通过这些内容快速了解这个命令如何使用。

### 更复杂的例子

下面我们将写一个更复杂的例子，在这个例子中，我们显示代码和输入输出，不多作介绍。

=== "PackageInstall.h"

    ```cpp
    #pragma once

    #include "cmd/ICmdInterface.h"

    class PackageInstall : public ICmdInterface<PackageInstall>
    {
        Q_GADGET
        $AsCmd(package)
    public:
        PackageInstall();

    public:
        $CmdArg1Memo("to be installed package name")
        $CmdArg1(QString, packageName)

        $CmdArg1PostHandle(checkPackageName)
        void checkPackageName();

        $CmdArg2Memo("to be installed package version")
        $CmdArg2Nullable
        $CmdArg2(QString, version)

        $CmdArg2PostHandle(checkVersion)
        void checkVersion();

    public:
        $CmdMappingMemo(install, "install package from remote")
        $CmdMapping(install)
        void install();

    private:
        void queryAvaliableServer();
        void checkLocalExist();
        void checkOnlineExist();
        void downloadPackage();
        void unarchieveData();

    private:
        QString queryLatestPackageVersion(const QString& version);

    private:
        QString m_makePath;
        QString m_host;
        QString m_zipPath;
    };
    ```

=== "PackageInstall.cpp"

    ```cpp
    #include "PackageInstall.h"
    #include "data/Env.h"
    #include "data/Remote.h"
    #include <httplib.h>
    #include <iostream>
    #include <QProcess>
    #include <QRegularExpression>
    #include <JlCompress.h>

    using namespace httplib;

    PackageInstall::PackageInstall()
    {

    }

    void PackageInstall::checkPackageName()
    {

    }

    void PackageInstall::checkVersion()
    {

    }

    void PackageInstall::install()
    {
        checkLocalExist();
        queryAvaliableServer();

        checkOnlineExist();
        downloadPackage();
        unarchieveData();

        qDebug().noquote() << "package installed. Name:" << packageName << "Version:" << version;
        quick_exit(1);
    }

    void PackageInstall::checkLocalExist()
    {
        if(!version.isEmpty()){
            if(Env::instance().isLocalPackageExist(packageName, version)){
                qDebug() << "pacakge already installed. Name:" << packageName << "Version:" << version;
                quick_exit(0);
            }
        }else{
            auto version = Env::instance().getLocalLatestPackageVersion(packageName);
            if(!version.isEmpty()){
                qDebug() << "pacakge already installed. Name:" << packageName << "Version:" << version;
                quick_exit(0);
            }
        }
    }

    void PackageInstall::queryAvaliableServer()
    {
        m_host = Remote::getRemoteServer();
        if(m_host.isEmpty()){
            qDebug() << "no server avaliable. package install quit";
            quick_exit(0);
        }
        qDebug().noquote() << "download from server: " << m_host;
    }

    void PackageInstall::checkOnlineExist()
    {    
        version = Remote::checkRemotePackage(m_host, packageName, version);
        if(version.isEmpty()){
            qDebug() << "package not exist online." << "Package" << packageName;
            quick_exit(1);
        }
    }

    void PackageInstall::downloadPackage()
    {
        m_zipPath = Env::instance().imakeRoot() + "/.cache/" + packageName + "@" + version + ".zip";
        Remote::downloadPackage(m_host, m_zipPath, packageName, version);
    }

    void PackageInstall::unarchieveData()
    {
        auto path = Env::instance().libStores().first() + "/" + packageName + "@" + version;
        JlCompress::extractDir(m_zipPath, path);
    }

    ```

相关的输出如下：


=== "help"
    ![image-20250702213049934](assets/image-20250702213049934.png)

=== "install package"
    ![image-20250702213132674](assets/image-20250702213132674.png)


## 接下来的内容

- 在上述的示例中我们展示了如何使用该工具，接下来的内容会更多的介绍相关内容，请继续阅读。