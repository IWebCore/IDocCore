# 用户自定义包（一）

在前面的文档中，我们使用了一系列内置的包，比如 nlohmann/json 的包， asio 的包，ICore， ITcp, IHttp 的包等等。今天我们讲述这些包是如何创建的，用户如果想打包一个包，它该如何操作。

用户自定义包，可以用于第三方的库的封装，集成到自己的项目中去；也可以将自己的项目或者产品拆分出独立的包，进行代码复用。



## 示例

在包管理中定义一个包可以非常简单，只需要一个 package.json 文件就可以定义一个包。

举一个非常简单的例子项目中的 Version 包

他的目录结构如下：

```
Version
├── agpl-3.0.txt
├── package.json
├── packaging
│   ├── Version.h
│   ├── Version.cpp
│   ├── VersionSpec.h
│   └── VersionSpec.cpp      
```

这个包中有`packaging`文件夹下面的代码，`agpl-3.0.txt` 的license许可声明,还有一个 `package.json` 的包描述文件

其中 package.json 文件的内容如下：

```json
{
    "name":"packaging",
    "version":"1.0.0",
    "summary":"python-packaging-like lib for c++, used for version management",
    "license":"none",
    "author":"deepseek",
    "autoScan": true,
    "keywords": ["packaging", "lib", "version"],
    "changelog": "default",
    "publisher": "yuekeyuan",
    "isGlobal": true
}
```

里面配置了 name, version, summary, license, author, autoScan, keywords, changelog，publisher 和isGlobal 等信息。

这里作者是 deepseek,的原因是因为这个包是我用 deepseek 生成的，在此之上做了一些修改，实在不好意思用我的名字作为 author 配置项。

这样一个包就配置好了。

当然，如果用户准备丰富这个包，可以添加很多的字段在 package.json 文件中。也可以在目录中添加其他的文件，比如 README.md, CHANGELOG.md, 或者其他的文档,等等。



## 最小配置

上面的 package.json文件中有很多的字段， 对于用户想简单的创建一个IMakeCore支持的包而言，在 packages.json 中的很多配置都不是必须的。这些不必须的字段是用于上传到服务器，给服务器解析，查找使用的。

注意：这里的内容只是针对于不上传到服务器上的包而言的，如果要上传到服务器，所有的内容都是不可省略的，否则会上传失败，服务器在上传包的时候，会自动检查包中的配置是否符合要求。



在接下来的内容中，我将给出一个最小的配置集合。以上面的 packaging 这个库而言，它可以缩略为如下的内容：

```json
{
    "name":"packaging",
    "version":"1.0.0",
    "summary":"python-packaging-like lib for c++, used for version management",
    "autoScan": true,
    "publisher": "yuekeyuan",
    "isGlobal": true
}
```

是的，就只是上面的 六个配置内容即可。

如果用户还是觉得这个配置过于复杂，可以继续精简如下：

```json
{
    "name":"packaging",
    "version":"1.0.0",
    "summary":"python-packaging-like lib for c++, used for version management",
    "autoScan": true
}
```

这个时候 publisher 和 isGlobal 字段同样也被精简下来了。



下面我们就描述一下这些字段的意义。

### name

name 表示包的名称。用户可以定义自己喜欢的名称。

名称的构成必须是 `英文大小写字符`，`数字`， `中划线-`，`下划线_` 和 `点.` 组成。其中第一个字符必须是英文字母。

这里建议用户以`自己的名称` `.` `功能名` 来作为一个包名。  



### version

包的版本号。

这里版本号的格式必须是 `major` `.` `minor` . `patch` 的形式来书写。不可以为 `*` ， `x` 或者其他以外的任何格式。

major, minor和patch, 分别是主版本号，次版本号，和补丁号，它们必须是数字。

目前版本不支持 `beta`, `alpha`, `pre` 等一系列额外信息的版本。



### summary

软件简单简短的一句话描述。这个用于告知用户这个包是干什么的。需要这个配置的原因是在 `ipc packages` 这个命令中，会列举这个库的简要说明。而这个简要说明的内容就是 summary 的内容。



### autoScan

autoScan 字段表示IMakeCore自动扫描整个包，将包中的文件添加到项目和编译中去。

autoScan 字段是bool 类型的字段。该字段和如何处理包中的文件，如何将 cpp, h, ui, res 宏定义的内容和项目关联起来有关。在后面的内容会详细介绍文件处理模块。在这篇文档中，用户需要将autoScan字段配置为 true, 表示启用自动扫描模式来加载包中的内容。在之后的文档中会描述如果 autoScan 为 false 的情况该如何处置。



### publisher

publisher 字段表示上传者的字段。这个字段是上传用户自己的名称，也就是在 IPubCore 中注册的名称。

如果用户省略该字段，则该字段的默认值是用户在 IMake 中配置的名称，用户可以在命令行中使用 `ipc user` 来查看自己的用户名称，使用 `ipc user set` 命令来设置用户名称。`ipc user` 默认的内容是  `default`。所以如果省略了这个字段，那么这个发布者就是 default.



### isGlobal

这个字段表示这个包是否是一个公共包。公共包就是在引用这个包的时候可以省略 publisher 字段的包。

举一个例子，我们在引用 `ICore` 这个包，可以直接使用如下的形式导入包。

```json
"ICore" : "1.0.0"
```

 其实还有一种形式，就是把包名称写完全。一个包名称包含 `publisher` 和 `name` 这两个字段, 他们中间以 斜线 `/` 进行分割，如下所示：

```json
"yuekeyuan/ICore" : "1.0.0"
```

因为 ICore 这个包的 `isGlobal` 为 `true` 所以我们可以省略 `yuekeyuan` 这个publisher 字段和斜线，直接使用 `ICore` 这个名称。

这么做有什么好处呢？这个是因为一个包名称， 比如 abc, 这个名称， zhangsan 能够写这个包，lisi 也能写这个包，那么就需要通过 publisher 来区分引用的是谁的包，`zhangsan/abc` 和 `lisi/abc`就是两个不同的包。如果zhangsan的包 声明了 `isGlobal` 为 `true`, 那么 `abc` 引用的就是zhangsan的包，此时在同一个 环境下就不能有lisi 的包isGlobal 也为 true 的情形，如果存在，则会报错。

在包名称添加前缀的目的就是大家都可以创建和上传 同名的包，而不担心包名冲突的问题。如果在之后的事件里面，有的包做的比较好，那么这个包就可以成为 公共包，给大家使用，这个时候包 publisher 的名称就可以直接省略。



### 同时省略 isGlobal 和 publisher

在上述的精简配置中，我们同时省略了 isGlobal 和 publisher 这两个字段。此时我们默认这个包是 isGlobal 为 true 的公共包，并且可以省略 publisher 的名称直接引用这个包。

这个对于一个不会上传到服务器的本地包而言，是再适合不过了。用户可以直接使用 名称来导入这个包。在这篇文档中，我们只说明如何简单自定义一个包，不会涉及到上传服务器的内容，所以用户可以放心的省略这两个字段。

如果上传到服务器，还是需要认真写好每一个字段。



## 包的位置

用户自定义的包可以放到任何一个 libstore的文件夹下面, 如下调用 `ipc libstores` 命令，就会输出所有的可用的libstores.

```text
C:\Users\Yue>ipc libstores

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

C:/Users/Yue/IMakeCore/.lib
```

上述的 libstore 是全局 libstore, 用户也可以配置自己的libstore 文件夹位置，来放置所需要的包的位置，可以通过 `ipc libstores add ` 命令来添加额外的包。

注意放置在 libstore 文件夹下面的内容必须是一个包含 package.json 的文件夹，不能将 package.json 直接放置在 libstore 文件夹下面。



## 说明

在上面的教程中，我们描述了一个最简单的包是什么样子的。此外还有很多的内容没有做说明。