# 安装ICmd

ICmd 是放置在 IPubCore 上的一个插件, 地址是： [ICmd](https://pub.iwebcore.org/package.html?name=ICmd&version=1.0.0) 。 


## IMakeCore

用户想使用 ICmd， 必须先安装 IMakeCore。关于IMakeCore的介绍参考 [IMakeCore 快速开始](../IMakeCore/quick_start.md)


## 配置 IMakeCore

一个最简单的 ICmd 包导入配置如下：

```json
{
    "packages":{
        "asio":"*",
        "nlohmann.json":"*",
        "ICore":"*",
        "ICmd":"1.0.0"
    }
}
```

在包的配置中，我们引入了 ICmd， ICore， nlohmann.json， asio 四个依赖。ICmd 依赖于 ICore, ICore 依赖于 nlohmann.json 和 asio 两个库。他们必须一同被导入进来。

用户如果想使用其他的库，也需要按照此方式导入进来。比如 zip 库， httplib 库等。
