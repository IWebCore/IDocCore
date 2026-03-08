# IPubCore Package Server

> This document describes the usage of IPubCore.

## Aside

The design goal of the entire IWebCore framework is to be comparable to the Spring platform. IMakeCore is designed to be comparable to package management tools like Maven/Gradle. Therefore, besides the built-in packages of MakeCore, users should also be able to automatically download packages from remote locations to their local machine for compilation and execution together with the project.

During the development of IWebCore, a package management server was also developed to work alongside the local service of IMakeCore. Users can configure packages from the package management server, and IMakeCore will automatically download these packages and integrate them into the project.

The previous address was `https://pub.iwebcore.org`, which had a proper domain name, and the HTTPS was already set up. Initially, due to too many personal matters, I did not manage this content well. First, the HTTPS expired, then I could not afford to renew the server. I switched to a domestic server costing 99 yuan per year. However, domestic servers cannot bind `.org` / `.io` type domains. The previous `.com` domain was also hijacked, so now the website is operating without a domain name. Users can access the IPubCore website directly using the IP address (115.191.52.106).

Moreover, operating a content-based website is not just about putting the website online; it also requires consideration of the legality of user-uploaded content. This involves a significant amount of effort, and I do not have the resources to manage this. Therefore, users can register but cannot upload their own packages. If you wish to upload a package, please contact me.

Here is the main content:

---

## IPubCore Website

The IPubCore website is a platform for IMakeCore to search for and download packages. The address is [IPubCore](http://115.191.52.106/). The IPubCore website is built using the IHttpCore framework backend and a React frontend. Here, I recommend users to use the IHttpCore framework to write their own HTTP servers.

Users can search for various packages on this website and add the package name and version to the `packages.json` file. IMakeCore will automatically download the package and integrate the specified version.

The interface of the IPubCore website is shown below:

![image-20250713162242016](assets/image-20250713162242016.png)

### Finding and Using Packages

Users can input keywords on the [search page](http://115.191.52.106/search.html) to search for packages. Clicking on a found package allows users to view its detailed information.

### Registration and Login

Users can register and log in via the [Login](http://115.191.52.106/login.html) / [Register](http://115.191.52.106/register.html) buttons in the top-right corner of the website.

### How to Publish Packages

#### Email Verification

Publishing a package requires email verification.

Due to website management reasons, users cannot upload packages by default and must apply to the administrator for permission. The administrator will review the application and grant the corresponding permissions. To contact the administrator, users should send an email to the [Administrator Email](mailto:yuekeyuan001@gmail.com) using the registered email address for confirmation.

When sending an email, users must include the following content:

```
I want to publish a package, so I send this email.
我发送这封邮件，我想发布一些包。
``
```

I sincerely apologize, but due to my busy schedule (I am currently working on the entire system and also job searching, so I am very busy), I have not had the time to fix this issue. (The missing functionality is minimal, but I simply don't have the time.)

#### Packaging

Currently, users need to manually package their packages. In the future, the packaging and upload functionality will be completed by the ipc tool.

Users should create a standalone package that can be loaded into the project. Simply use the zip tool to package it into a `.zip` file. Note that during packaging, the `package.json` file must be placed in the root directory of the zip file and cannot be nested within a subdirectory.

For guidance on defining a package, please refer to the [Define Package](./definePackage.md) documentation.

#### Publishing a Package

After logging in, users can click their username in the top-right corner, then click the `My Package` button in the pop-up menu, which will redirect to the [Package Management](http://115.191.52.106/packagemanage.html) page. On this page, clicking the upload package button will lead to the [Package Upload](http://115.191.52.106/packageupload.html) page, where users can drag and drop the packaged package to upload it.

Users must verify their email before publishing a package.

During the upload process, the package information will be validated. If the validation fails, please modify according to the feedback.

---

## ipc and IPubCore

Users can operate IPubCore content using the ipc tool.

### Search

The `ipc search` command can search for packages on the network. The following content shows the search results for JSON-related packages:

```
C:\Users\Yue>ipc search -- json

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

Name                       LatestVersion   Summary
yuekeyuan/json_struct      1.0.1           json_struct is a single header only C++ library for parsing JSON directly to C++ structs and vice versa
yuekeyuan/jsoncpp          1.9.6           A C++ library for interacting with JSON data
(yuekeyuan)/nlohmann.json  3.12.0          json library for C++
yuekeyuan/rapidjson        1.0.4           A fast JSON parser/generator for C++ with both SAX/DOM style API
yuekeyuan/simdjson         3.13.1          Parsing gigabytes of JSON per second : used by Facebook/Meta Velox, the Node.js runtime, ClickHouse, WatermelonDB, Apache Doris, Milvus, StarRocks
yuekeyuan/yyjson           0.11.1          The fastest JSON library in C

``
```

### Installing Packages

If users wish to install a remote package, they generally only need to add the desired package to the project's `packages.json` file. Alternatively, they can use the `ipc package install` command to install a package. The usage method for `ipc package install` is as follows:

```
C:\Users\Yue>ipc package install

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

ERROR OCCURED: args list too short for argx to retrive data. arg count less than 1 [Cmd Path]: package install [Cmd Arg Type]: ArgX [ArgX Name]: packageName [ArgX Index]: 1

[CMD]:
    ipc package install
[Memo]:
    install package from remote to system
[Argx]:
    Index  Name         TypeName  Nullable  Memo
    1      packageName  QString   false     to be installed package name
    2      version      QString   true      to be installed package version
``
```

This command accepts two parameters: one is the package name, and the other is the version. The version can be omitted, in which case the latest version will be requested. Therefore, if a user wants to install the package `yuekeyuan/yyjson` found in the search results above, they can use the following command:

```
C:\Users\Yue>ipc package install -- yuekeyuan/yyjson

 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

download from server:  http://115.191.52.106
package installed. Name: yuekeyuan/yyjson Version: 0.11.1
``
```

At this point, the package `yuekeyuan@yyjson` is installed.