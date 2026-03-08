# 安装 IMakeCore

> 本文档描述如何安装 IMakeCore.

## 安装

### 预备安装环境

#### python 环境

IMakeCore 需要 python3 的安装环境来该运行程序。请确保系统中 有 python 3 的安装环境。

另外需要确保 python3 中有 `packaging` 和 `requests` 两个库，否则 IMakeCore 在执行的时候会报错。

用户可以使用如下命令安装：

```powershell
# 安装 packaging 和 requests
pip install packaging requests
```



#### Qt 环境

如果用户只在cmake下进行开发程序，不使用 Qt 相关的包，如 ICore, IHttp, IRdb, ICmd 等等包，只使用普通的包，那么用户可以不安装Qt 环境。

开发者请自行安装 Qt，建议Qt版本不低于 Qt5.14.2。Qt5.14.2及以上的版本经过了测试，以下的版本没有测试，用户也可以自行测试。

Qt5.14.2是最后一个编译后的分发版本，之后的版本都是通过安装器进行安装的。



### 	安装 IMakeCore

IMakeCore 的下载地址是 [IMakeCore.zip](./assets/IMakeCore-v0.0.1.zip) ，也可以在 github 上进行下载，地址是：[Releases · IWebCore/IMakeCore](https://github.com/IWebCore/IMakeCore/releases)。

用户下载的是一个 zip 压缩包，解压缩后的内容如下：

![image-20260213211812635](assets/image-20260213211812635.png)

在这个文件夹中有 `linux_install.sh` 和 `windows_install.bat` 两个脚本文件，他们分别对应 linux 上的安装包和 windows 上的安装包。



#### linux 安装 IMakeCore

我是在wsl中安装的IMakeCore。

在解压后的文件夹中打开命令行工具，执行命令如下：

```bash
./linux_install.sh
```

执行bash之后会请求管理员权限，需要输入密码。在输入密码之后脚本继续执行，安装文件和设置环境变量等内容。

如下是安装时的输出截图：

![image-20260213212224166](assets/image-20260213212224166.png)

在 linux 上安装 IMakeCore之后，如果在接下来的测试中没有响应，请重启 linux.

IMakeCore使用的安装目录是 `/opt/IMakeCore`



#### windows 安装 IMakeCore

windows 安装 IMakeCore 和linux的安装方式是一致的。

在解压后的文件夹中打开命令行工具，执行命令如下：

```powershell
.\windows_install.bat
```

命令行在执行过程中会请求管理员权限的对话框。用户在同意管理员权限之后会弹出新的命令框执行安装过程。安装过程如下图所示：

![image-20260213204949382](assets/image-20260213204949382.png)

安装脚本会拷贝文件和设置一些环境变量。执行完成之后用户就可以使用 IMakeCore了。

IMakeCore 的安装目录是 `C:\Users\Yue\IMakeCore`. 也就是在用户目录下面。



## 测试安装情况

IMakeCore 安装好了之后，可以在 bash 或者cmd 中执行 `ipc version` 这个命令测试是否安装成功。`ipc` 是内置在IMakeCore 中的一个默认的程序，在安装之后也被放置在环境变量中了。



在linux中执行情况如下：

![image-20260213212910564](assets/image-20260213212910564.png)



在 windows中执行的截图如下：

![image-20260213212956744](assets/image-20260213212956744.png)



此时 IMakeCore已经安装完成了,用户可以接下来继续阅读关于IMakeCore的内容。



