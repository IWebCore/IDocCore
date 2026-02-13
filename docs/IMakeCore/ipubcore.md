# IPubCore 包分发网站

> 本文档描述 IPubCore 的使用方法。

IPubCore 网站是 IMakeCore 用于查找和下载包的网站，地址是 [https://pub.iwebcore.org](https://pub.iwebcore.org)。

IPubCore 是由 IWebCore 中 IHttpCore 框架编写的后端，react 编写的前端，这里推荐用户使用 IHttpCore 来编写自己的 http 服务器。

用户可以在这个网站上搜索各类的包，搜索到的包可以将包名和版本写到 packages.json 文件中去。IMakeCore 会自动下载该包，并集成该版本的包。

IPubCore 网站界面如下所示：

![image-20250713162242016](assets/image-20250713162242016.png)

## 如何查找和使用包

用户在 [搜索页面](https://pub.iwebcore.org/search.html) 输入关键字进行搜索。搜索到的包点击进去就可查看相关的详细信息。


## 如何注册和登录

用户通过网站顶部右上角的 [登录](https://pub.iwebcore.org/login.html) / [注册](https://pub.iwebcore.org/register.html) 按钮进行用户的注册和登录。

## 如何发布包

### 邮箱验证

发布一个包需要进行邮箱验证。

由于网站建设的原因，用户默认不能上传包，需要联系管理员进行申请。管理员会审核用户的申请，并给予相应的权限。
联系管理员 请使用注册的 email 地址 发送邮件到 [管理员邮箱](mailto:yuekeyuan001@gmail.com) 进行确认。

用户发送邮件的时候，需要注明如下内容：

```
I want to publish a package, so I send this email.
我发送这封邮件，我想发布一些包。
```

这里实在抱歉，等我挤出时间了，我一定吧这个给搞好（这个功能缺失很小，但是我现在一方面搞整个系统，一方面也在找工作，时间很紧张）。



### 打包

目前用户需要手动打包，在之后打包和上传的功能可以由 ipc 工具完成。

用户将能够加载到项目的独立包，直接使用 zip 工具打包成为 .zip 包即可。注意在打包的时候， package.json 文件必须在 zip 文件的根目录中，不能嵌套目录。

关于如何定义一个包，请参考[定义包](./definePackage.md) 的文档。



### 发布包

用户在登录之后，可以在右上角点击用户名，在弹出菜单中点击 `My Package` 按钮，跳转到 [包管理]([Package Management](https://pub.iwebcore.org/packagemanage.html)) 页面。在页面中，点击上传包，跳转到 [包上传]([上传包 - IPubCore](https://pub.iwebcore.org/packageupload.html)) 页面，将打包好的包 拖拽进去，上传即可。

用户在发布包之前必须验证邮箱。

在上传的过程中，会对包的信息进行验证，如果验证不通过，请按照反馈信息进行修改。

## 

