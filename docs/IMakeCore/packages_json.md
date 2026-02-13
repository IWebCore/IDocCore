# pacakges.json

> 本文档描述 packages.json 文件的结构和用法。

## 概览

packages.json 是项目的包管理配置。与此相对应的还有一个 [configs.json](./configs_json.md) 文件，用于管理系统的IMakeCore 配置。

在[包集成](./packageIntegration.md) 中，我们介绍了 packages.json 中 packages 字段的用法。在这篇文档中，将系统的介绍 packages.json 的结构和用法。

packages.json 是 IMakeCore 自动生成的一个文件，用于管理项目的依赖包的配置。它的位置在项目的当前目录下面。


一般的packages.json 如下：
```json
{
    "libstores": [],
    "forceLocal": true,
    "packages": {
        "ICmd": "*",
        "ICore": "*",
        "IRdb": "x",
        "asio": "*",
        "cpp-httplib": "*",
        "nlohmann.json": "*",
        "packaging": "*",
        "stachenov.quazip": "*",
        "zlib": "*"
    }
}
```

在接下来的内容里，将对该配置的用法进行详细的说明。

## packages 的中的字段

### forceLocal[](#forceLocal)

全局作用域的 `forceLocal` 值类型是 `bool` 类型， 默认值是 `false` 。

`forceLocal` 如果定义在全局作用域，那么配置在 packages.json 中的包都要受到影响。如果一个 包没有在属性中配置 `"forceLocal":false` 那么这个包的 `forceLocal` 值为全局作用域中的 `forceLocal` 的值。 

如果一个包的`forceLocal` 的值为 `true`, 该包将会被拷贝到项目的包路径下面。

这里的优先级是： 具体的包的 `forceLocal` 的优先级高于 全局 `forceLocal` 的优先级。 如果一个包的 `forceLocal` 的属性没有定义，那么全局的`forceLocal`的值将会代替包的 `forceLocal` 的值。

被标记为 forceLocal 的包会在包加载的时候拷贝到项目的包路径下面， 关于项目的包路径 请参考 [localLibStore](#locallibstore)。


举例如下：
```json
{
    "forceLocal": true,
    "packages": {
        "lib1": "*",
        "lib2": "x",
        "lib3": {
            "version": "*",
            "forceLocal": false
        },
        "lib4": {
            "version": "x",
            "forceLocal": true
    }
}
```

在上面的例子中，lib1 的 forceLocal 为 true, 会被拷贝到项目包路径下进行加载。lib2的version 信息是 `x`, 这个包会被直接忽略，不加载。lib3 的 forceLocal 为 false, 他会按IMakeCore默认的加载规则来加载。lib4 的 forceLocal 为 true, 它也会被拷贝到项目包路径下进行加载。

注意上面的 lib3 的包，如果在项目包路径下面有这个包匹配它的 name 和 version, 那么 lib3 实际加载的包也是由项目包位置而来的。

全局 forceLocal 为 true 的情况通常但不限于以下情况使用：
- 用户想将某个包的版本固定在本地，不从远程仓库下载，以便于调试和修改。
- 用户想把项目连同项目依赖一同打包，在不同的机器上进行编译，这样依赖包就不用再从网络上下载。 

### servers

servers 字段的值类型是一个 array 列表类型，里面可以存放字符串，默认为空列表，该字段可以省略不写，默认为空列表。servers字段内部的字符串必须是一个服务器路径。用户可以提供多个服务器地址用于下载包。

比如以下是合法的路径：

```txt
http://127.0.0.1:8000
https://abc.com
http://abc.com:81
```

注意这里的路径必须是一个 `scheme + host` 的路径， 不能带有 path信息，如下的路径是非法路径：

```
http://127.0.0.1/
http://abc.com/hello
```

servers 的目的是提供网络包服务。IMakeCore 可以在相应的服务器上查询，下载包。

servers 字段中靠前定义的服务器优先于靠后的服务器， packages.json 中定义的 servers 的优先级高于 IMakeCore系统配置中的 servers 的优先级。IMakeCore 在实际的包查询和下载中，将会按照优先级来调用服务器地址，如果前一个服务器不能满足服务，比如连接不上或者没有当前需要的包，这回按顺序尝试使用下一个服务器地址来提供服务。



### localLibStore [](locallibstore)

packages.json 中定义的 localLibStore 字段是表示当前的项目包位置。 该字段对应的是表示一个文件夹路径的字符串。字段可以省略，如果字段省略，那么默认的路径是项目路径下面的 `.lib` 文件夹。用户可以自己定义 localLibStore 的路径。

这个字段和 forceLocal 字段配合使用。如果一个包的属性是 forceLocal, 那么这个包就会被存放在 localLobStore 中去。


### libStores

libstores 字段对应的值类型是一个 array 列表，表示一系列存放包的文件夹。libstores 字段可缺省，默认为空列表。

注意 localLibStore 的优先级高于 libStores， libStores 的优先级高于 IMakeCore 系统中定义的 libstore 的优先级。

packages.json 中定义的 libStores 只适用于当前项目，不适用于其他的项目。如果用户需要将一个 libStore 适用于所有的项目，可以在 IMakeCore 系统中配置 libStore。

用户如果有一些额外的包存放在不同的文件夹中，则可以将相应的文件夹的路径放置在 libStores 字段中。这样包就会被 IMakeCore识别并处理。

### packages

> package 中的内容在 [包集成](./packageIntegration.md) 中有详细的描述。这里将其中的内容复制过来，以形成完整的 packages.json 的结果描述。已经了解的用户可以忽略此内容。

#### 简单的包配置

所有的包都需要在 packages.json 文件中的 packages 域中定义。他们的定义方式如下：

##### name : version

最基本的包集成方法就是 name : version 这种形式。 这里指定了包的版本。如果本地没有这个版本的包，IMakeCore 将尝试从服务器拉取该版本的包。如果服务器拉取失败，则该版本的包配置失败。用户需要检查该包该版本是否存在。

version 的形式是  `xxx.xxx.xxx` 。例如 `1.0.0` 这种形式，其他的形式，如 `beta` 之类的目前不支持。 

它的使用方式如下：

```json
{
    packages:{
        "ICore" : "1.0.0",
        "asio" : "1.30.2"
    }
}
```

##### name : *

这种形式不指定包的具体版本。

IMakeCore 在加载该包的时候，会扫描本地所有的包，如果找到该包，会使用扫描到的包的最高版本进行加载。如果没有找到该包，会在服务器上下载该包的最新版本，并进行加载。

所有这里有一点要注意：如果用户使用 `*` 来导入包，如果用户对于版本有要求，用户并不能确定的导入到自己想要的版本。如果用户想使用最新版本，而本地存在的并非是最新版本，在包加载的时候，加载的也不会是最新的版本。用户需要指定版本号加载最新版本，或者通过 `ipc update` 来更新本地包到最新版本来进行加载。



##### name : x

这里的 `x` 是字符 `x` ['eks]， 用户也可以使用大写的 `X` 来书写。

如果一个包标记为  `x`，那么在加载 packages 中所定义的包的时候，这个包会被过滤掉，不会加载这个包。

IMakeCore 定义这个 `x` 的目的是由于 json 文件不能有注释注掉要导入的包。用户如果只是想临时去掉这个包，则可以使用 `x` 作为包的配置项。



####  更复杂的包配置

上面讲述的是简单的，键值对，并且值是字符串的，一行写的下的包配置。

IMakeCore 支持更复杂的配置，用户可以配置一个包更多的信息。此时的键值对的 值不再是一个字符串，而是一个对象集合，如下所示：

```json
{
    "packages":{
        "MyLib" : {
            "version" : "*",
            "path" : "c:/mylib_path/MyLib",
            "url" : "https://github.com/MyName/MyLib/MyLib.zip"
            "forceLocal" : true
        }
    }
}

```

在上面的配置中，用户可以指定复杂的内容，以满足用户对于个性化配置的需要。

下面我们一以来讲解对象中的这些属性都是什么意思。

##### version

这里的 version 和我们一行能写的包配置的 version一般无二。用户可以设置`具体的版本`，可以使用 `*` 来表示所有版本都可以接受， 也可以使用 `x` 来表示这个包不能够被解析和加载到项目中去。

version 是一个必须项。用户必须申明该包的版本，即使他是 `*` 任意版本。

##### path

path 的值是一个字符串。

这里的 path 是包的本地路径，如果用户配置了本地路径，IMakeCore 会从本地加载包。相应的，如果在这个路径下面找不到这个包，那么就会包加载错误，用户需要手动检查该包还在不在，包的版本和我们定义的版本是否一致。

path 可以省略不写。不写的话，IMakeCore 会使用其他的路径加载。

如果用户写了 path 路径，那么 path 的优先级是最高的，IMakeCore 只能从这个路径中去查询包。

##### url

url 可以是一个字符串，表示一个 url路径， 也可以是一个字符串序列，表示一系列路径。

这里的 url 是包的下载地址，如果用户没有配置本地路径，或者在本地没有查找到相关的包，那么IMakeCore 就会使用用户定义的url路径顺序下载包，尝试解析加载包。

如果url 指定多个，并且前一个 url 下载到包了，但是该报并不匹配配置中的包，那么此时IMakeCore不会尝试下载解析后面的包，而是直接报错。此时用户需要手动检查包的配置。

url 可以省略不写。

##### forceLocal [](#forceLocal)

`forceLocal` 的值为 `bool` 类型，默认为 `false`。

forceLocal 如果为 true。那么表示这个包必须从`项目路径下的包文件夹`中加载包。如果`项目路径下的包文件夹`中没有该包，IMakeCore 会复制一个包到该路径下，并进行加载。

`项目路径下的包文件夹` 默认是项目路径下的.`lib 文件夹`，用户也可以在package.json 中配置其他路径。

forceLocal 存在的意义有以下两点。

- 用户对一个包想进行一些更改，以满足自己的要求。此时如果直接在包上进行更改，则会污染这个包。导致其他项目出现问题。如果拷贝到项目路径下，则没有这个问题。
- 用户想将这个项目拷贝分享，而将要拷贝的位置没有安装 IMakeCore, 或者是断网状态，或者是想直接拷贝过去编译，那么将依赖的包拷贝到项目文件夹下无疑是一个很好的方法。

forceLocal 字段除了可以配置在包属性内，可以配置在 packages.json 的公共域中，具体用法参考 [forceLocal](./packages_json.md#forceLocal)