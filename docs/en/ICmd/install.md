<译文内容>
# Install ICmd

ICmd is a plugin placed on IPubCore. Its address is: [ICmd](https://pub.iwebcore.org/package.html?name=ICmd&version=1.0.0).

## IMakeCore

To use ICmd, users must first install IMakeCore. For an introduction to IMakeCore, refer to [IMakeCore Quick Start](../IMakeCore/quick_start.md).

## Configure IMakeCore

The simplest configuration for importing the ICmd package is as follows:

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

In the package configuration, we introduce four dependencies: ICmd, ICore, nlohmann.json, and asio. ICmd depends on ICore, and ICore depends on the two libraries nlohmann.json and asio. They must be imported together.

If users want to use other libraries, they need to import them in the same way. For example, the zip library, httplib library, etc.