# 定义包

> 本篇文档描述如何将源代码封装为一个包

## overview

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

下面具体描述以下 package.json 文件的各个字段的含义。其中如果是必须字段，将在字段的后面标注一个 `*` 。

## 包的信息

### name`*`

name 表示包的名称。用户可以定义自己喜欢的名称。

名称的构成必须是 `英文大小写字符`，`数字`， `中划线-`，`下划线_` 和 `点.` 组成。其中第一个字符必须是英文字母。

这里建议用户以`自己的名称` `.` `功能名` 来作为一个包名。  

### version`*`

包的版本号。

这里版本号的格式必须是 `major` `.` `minor` . `patch` 的形式来书写。不可以为 `*` ， `x` 或者其他以外的任何格式。

major, minor和patch, 分别是主版本号，次版本号，和补丁号，它们必须是数字。

目前版本不支持 `beta`, `alpha`, `pre` 等一系列额外信息的版本。

### author`*`

作者名称。

这个必须是代码的实际作者，用户可以上传别人的开源包给大家使用，但是上传的时候一定要把作者给写上，不能写自己。如果原作者想要回代码所属权，上传者需要将所属权转让。

(这里我不知道具体的法律内容是啥，会不会触犯法律。如果有懂的，可以告知我，但不要因为这件事情告我，我可以改，立马改。)

### summary`*`

软件简单简短的一句话描述。这个用于告知用户这个包是干什么的。

### keywords`*`

关键字。该内容是一个 字符串列表，可以为空，不可省略。

这个是用于优化搜索使用的，如果用户选的关键字好，可以帮助使用者快速定位到你的库。

### isGlobal*

这个字段代表是否是公共库，它的值为 true 时表示这个是一个公共库。可以省略，省略时为true。

如果用户想上传包到 IPubCore 给所有人使用，isGlobal 则是必须字段。如果没有该字段，用户无法将该包上传到服务器，但是用户如果不需要上传服务器，而自己在私下使用该包，那么可以将该字段省略，在后面有专门说到该字段省略的情况。

#### isGlobal 字段值的意义

如果 isGlobal 为 `true`, 或者省略时， 则表示这个包是一个公共包。那么用户在引用该包的时候可以省略publisher前缀，如果isGlobal 字段的值为`false`, 那么这个包是一个非公共包，用户在引用该包的时候必须使用 publisher 前缀加以限定。

#### 用户上传包中 isGlobal 的管理

用户上传包时，isGlobal 字段必须存在，如果不存在，用户不可上传包。

目前在用户第一次上传包的时候，isGlobal 字段必须是 false, 不能够为公共包，用户可以申请该包为公共包。如果通过申请，那么在下一次上传包的的时候， isGlobal 字段的值必须是 true, 如果为 false 则无法上传包。

一个包为公共包的判断依据有是否是原作者，下载量，github 上的 star数量，IPubCore 中的star数量等指标要求。一般一个名字下面只能有一个包是公共包。

#### isGlobal 字段缺失的情况

如果isGlobal 字段缺失，则这个包是公共包。公共包就是在引用包的时候可以省略 publisher 前缀的包。具体的内容可以查看 [公共包](globalPackage.md)。

用户自己定义的包，在自己使用的时候不需要添加前缀，这样能够方便用户自己使用，但是这个包不能够上传上去。

需要注意一点，如果这个包的名称和本地缓存下来的公共包的名称冲突，IMake程序会直接报错。

### publisher*

publisher 字段表示上传者的字段。这个字段是上传用户自己的名称，也就是在 IPubCore 中注册的名称。

如果用户省略该字段，则该字段的默认值是用户在 IMake 中配置的名称，用户可以在命令行中使用 `ipc user` 来查看自己的用户名称，使用 `ipc user set` 命令来设置用户名称。

用户在上传包时不可以省略该字段，如果省略该字段，则上传会被拒绝。 如果用户登入的名称和包中的 publisher 字段不一致，用户上传也会失败。



### autoScan*

autoScan 字段是bool 类型的字段。该字段和如何处理包中的文件，如何将 cpp, h, ui, res 宏定义的内容和项目关联起来有关。在后面的内容会详细介绍文件处理模块。



### 其他字段

#### license

软件使用的版权。

#### changelog

本次更新的内容

#### dependencies

本软件的依赖库。

这个字段在加载该包的时候会检查依赖中定义的包。如果依赖包不存在，则IMakeCore 会在包加载的时候报错。

依赖库的定义如下：

```
{
	...
    "dependencies": {
        "ITcp": "*",
        "ICore": "*"
    },
    ....
}
```

这里该库依赖了 ITcp 和 ICore, 如果该库不存在，则会报错。

这里依赖库的版本定义可以为 `*` ， 可以为具体的版本， 也可以是一个 版本范围， 版本范围遵循 [Semantic Versioning 2.0.0 | Semantic Versioning](https://semver.org/) 的定义。

#### urls

这个是和库相关的 url 链接，为字符串数组，用户可以写尽量多的内容。

#### 其他的内容

这里不再一一列举，用户可以想用自己想用的任何字段，不做统一规定了。

## 包代码的管理集成

package.json 文件提供包的基本的信息，其中 autoScan 字段决定用户如何处理包中的参与编译的信息和文件。下面对于该项内容进行集中的说明。

### 用户提供包信息

当 package.json 中的 autoScan 字段为 false 的时候，则表示用户希望自己编写包代码管理的文件。在包中用户必须提供 .pri 和 .cmake 文件以用于支持程序集成，能够将包加载到项目当中去。

#### .pri 文件



在项目中用户必须提供 .pri 作为后缀名的文件，以供程序使用。文件的名称可以是以下形式：

- `{packageName}.pri` 
- `{publisher}@{packageName}.pri`
- `{publisher}@{packageName}@{version}.pri` 
- `{packageName}@{version}.pri` 

其中 publisher, packageName 和 version 分别是 package.json 文件中提供的 publisher, name 和 version 这三个字段的值。上述的名称必须项是 `packageName`， `publisher` 和 `version` 是可选项。

在IMake中qmake提供了以下的函数用于管理代码。

- loadToSources

- loadToHeaders

- loadToIncludes

- loadToResources

- loadToForms

- loadToLibraries

- lloadToDefinitions

上面的函数顾名思义，就是将各种资源加载到项目中去，所以用户在定义 pri 配置文件的时候，可以使用上面的各个函数来进行操作。

用户除了这些函数之外，也可以使用 Qt 自带的 HEADERS , SOURCES, DEFINES, LIBS 等qt 变量来加载资源。实际上上述的函数就是封装了Qt 本身的变量以方便添加资源。同时使用这些函数也和 cmake 同步，cmake同样提供了上述的函数。


#### .cmake 文件

当包 autoScan 的值为false 的时候，用户同样需要在包中提供一个 .cmake 文件以使 IMake 支持 cmake 的编译项目。该 .cmake 文件的名称可以为以下的内容：

- `{packageName}.cmake` 
- `{publisher}@{packageName}.cmake`
- `{publisher}@{packageName}@{version}.cmake` 
- `{packageName}@{version}.cmake` 

其中 publisher, packageName 和 version 分别是 package.json 文件中提供的 publisher, name 和 version 这三个字段的值。上述的名称必须项是 `packageName`， `publisher` 和 `version` 是可选项。

在IMake中cmake提供了以下的函数用于管理代码。

- loadToSources

- loadToHeaders

- loadToIncludes

- loadToResources

- loadToForms

- loadToLibraries

- lloadToDefinitions

上面的函数顾名思义，就是将各种资源加载到项目中去，所以用户在定义 pri 配置文件的时候，可以使用上面的各个函数来进行操作。这些函数与 qmake 中提供的函数是一致的。

用户可以使用以下的方式加载文件：

``` cmake
loadToIncludes(${CMAKE_CURRENT_LIST_DIR})

loadToHeaders(
    ${CMAKE_CURRENT_LIST_DIR}/http/IHttpAbort.h
	# and so on
	${CMAKE_CURRENT_LIST_DIR}/http/session/IHttpSessionWare.h
)

loadToSources(
    ${CMAKE_CURRENT_LIST_DIR}/http/IHttpCookieJar.cpp 
	# .... and so on
    ${CMAKE_CURRENT_LIST_DIR}/http/session/IHttpSessionWare.cpp
)

loadToResources(
    ${CMAKE_CURRENT_LIST_DIR}/http/webresource.qrc
)

```



### 自动扫描包信息

autoScan 告知IMakeCore代码加载待方式是自动扫描代码。用户不再需要配置 .pri 和 .cmake 文件，即使配置了，IMake 也不会采用该配置文件，而是通过扫描的方式来进行文件的扫描。所以自动扫描包信息是可以跨项目管理工具使用的。

在该包的信息被定义在项目中的`packages.json` 文件中时，项目管

### source 的处理

### header 的处理

### resouce 的处理

### ui 文件的处理

### 宏的处理


## 自定义包依赖

### cmake中的包依赖定义

### qmake中的包依赖定义

## 包上传


## 其他的设想

