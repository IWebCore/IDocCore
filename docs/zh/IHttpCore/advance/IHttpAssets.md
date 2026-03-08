# IHttp.assets

IHttpAssets 是一个 IHttpCore 的插件。这个插件的目的是提供对静态文件的支持。

用户可以通过在 packages 中配置该库来使用该库。
=== "packages.json"
    ```json
    {
        "packages": {
            "IHttp.assets": "1.0.0"
        }
    }
    ```

## Default Assets

在IHttpAssets中，默认提供了一个文件解析服务 IHttpDefaultAssets. 当用户将 IHttpAssets集成到自己的项目当中的时候，IHttpDefaultAssets 会默认支持。

### 示例

用户可以使用如下的内容开启 Assets 服务

=== "main.cpp"

    ```cpp
    #include "http/assets/IHttpAssetsAnnomacro.h"

    $SetHttpAssetsPath(":/templates/")
    int main(int argc, char *argv[])
    {
        IApplication a(argc, argv);
        IHttpServer server;
        server.listen();
        return a.run();
    }
    ```

### 宏注解

- `$SetHttpAssetsPath`

通过第三行的 `$SetHttpAssetsPath(":/templates/")`,设置一个  assets 的目录，这样我们就可以使用 http 服务去请求 `:/templates/` 目录下面的文件了。

这里设置的目录是 Qt Resource 的目录。用户也可以设置相对的或绝对的路径。

- `$SetHttpAssetsEnabled`

在 `IHttpAssetsAnnomacro` 中，还提供一个 宏注解 `$SetHttpAssetsEnabled`, 这个值默认为 true。 如果用户想临时关闭文件服务，则可以设置  `$SetHttpAssetsEnabled(false) `。这样 assets 就不会再进行工作。



## 自定义 Assets

除了上面默认提供的 assets 之外，用户可以定制自己的assets，比如，

- default assets 并不支持文件缓存，用户自定义的则可以缓存文件。
- 默认的 assets 不支持目录的响应，用户自定义的则可以响应目录的内容。
- 默认的 asserts 不支持相对的url 路径，用户也可以自定义，响应的时候加上一段自定义的url路径。
- 还有很多，不列举了。

### 如何自定义 assests?

具体内容参考 IHttpDefaultAssets. 

