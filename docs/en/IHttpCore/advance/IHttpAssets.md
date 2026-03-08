# IHttp.assets

IHttpAssets is a plugin for IHttpCore. The purpose of this plugin is to provide support for static files.

Users can use this library by configuring it in the packages section.
=== "packages.json"
    ```json
    {
        "packages": {
            "IHttp.assets": "1.0.0"
        }
    }
    ```

## Default Assets

IHttpAssets provides a default file parsing service called IHttpDefaultAssets. When users integrate IHttpAssets into their own projects, IHttpDefaultAssets is automatically supported.

### Example

Users can use the following content to start the Assets service

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

### Macro Annotations

- `$SetHttpAssetsPath`

Through the third line, `$SetHttpAssetsPath(":/templates/")`, a directory for assets is set, allowing the HTTP service to request files from the `:/templates/` directory.

The directory set here is a Qt Resource directory. Users can also set a relative or absolute path.

- `$SetHttpAssetsEnabled`

In `IHttpAssetsAnnomacro`, there is also a macro annotation `$SetHttpAssetsEnabled`, which defaults to true. If users want to temporarily disable the file service, they can set `$SetHttpAssetsEnabled(false)`. This will stop the assets service from functioning.

## Custom Assets

In addition to the default assets provided above, users can customize their own assets, such as:

- The default assets do not support file caching, while user-defined assets can cache files.
- The default assets do not support directory responses, while user-defined assets can respond to directory content.
- The default assets do not support relative URL paths, and users can also customize this to include a custom URL path during responses.
- And so on, without further enumeration.

### How to Customize Assets?

For detailed instructions, refer to IHttpDefaultAssets.