# configs.json
> 本文档描述 configs.json 文件的配置项。

## 概览

configs.json文件存储 IMakeCore 的系统配置信息。

用户不要轻易修改该内容。




## 配置项

### globalLibStore

packages.json 中定义的 localLibStore 字段是表示当前的`系统包`位置。 该字段对应的是表示一个文件夹路径的字符串。字段可以省略，如果字段省略，那么默认的路径是IMakeCore系统路径下面的 `.lib` 文件夹。用户可以自己定义 globalLibStore 的路径。

用户在网络上请求到的包，都会安装到此位置。


### libStores

libstores 字段对应的值类型是一个 array 列表，表示一系列存放包的文件夹。libstores 字段可缺省，默认为空列表。

注意 在项目 packages.json 中定义的 libStores 和 localLibStore 的优先级高于 在 IMakeCore configs.json 中定义的libStores。IMakeCore 在加载包时，如果待选包的 name 和 version 相同的情况下，则会优先从项目中的 libStore中加载包。

configs.json 中定义的 libStores 只适用于所有项目。

用户如果有一些额外的包存放在不同的文件夹中，则可以将相应的文件夹的路径放置在 libStores 字段中。这样包就会被 IMakeCore识别并处理。

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


### user

user 是用户在注册 IPubCore 网站时填写的 用户名信息。

该字段仅用于通过 ipc 工具进行包上传使用，不会用于其他目的，收集用户信息。 (目前由于 `ipc` 包上传功能没有完善，此字段不会被使用)

用户可以通过  `ipc user` 命令来查看 用户名称， 可以通过 `ipc user set` 命令来设置用户名。

### email
email 是用户在注册 IPubCore 网站时填写的邮箱信息。

该字段仅用于通过 ipc 工具进行包上传使用，不会用于其他目的，收集用户信息。 (目前由于 `ipc` 包上传功能没有完善，此字段不会被使用)

用户可以通过  `ipc email` 命令来查看邮箱， 可以通过 `ipc email set` 命令来设置邮箱。