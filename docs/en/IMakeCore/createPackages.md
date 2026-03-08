# User-Defined Packages (Part 1)

In the previous documentation, we used a series of built-in packages, such as the `nlohmann/json` package, the `asio` package, and others like `ICore`, `ITcp`, and `IHttp`. Today, we will explain how these packages are created and how users can package their own modules.

User-defined packages can be used to encapsulate third-party libraries for integration into their own projects; they can also be used to split their own projects or products into independent packages for code reuse.

---

## Example

Defining a package in the package management system can be very simple—only a `package.json` file is needed to define a package.

Here is a very simple example: the `Version` package in a project.

Its directory structure is as follows:

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

The code under the `packaging` folder, the `agpl-3.0.txt` license declaration file, and the `package.json` package description file are included in this package.

The content of the `package.json` file is as follows:

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

This configuration includes information such as `name`, `version`, `summary`, `license`, `author`, `autoScan`, `keywords`, `changelog`, `publisher`, and `isGlobal`.

The reason the author is listed as `deepseek` is because this package was generated using `deepseek`, and some modifications were made to it. I sincerely apologize for using my name as the `author` configuration.

Once configured, the package is ready.

Of course, if users wish to enhance the package, they can add additional fields to the `package.json` file or include other files in the directory, such as `README.md`, `CHANGELOG.md`, or other documentation.

---

## Minimum Configuration

The `package.json` file above contains many fields, but for users who simply want to create a package supported by IMakeCore, many of these configurations are not required. These non-required fields are used for uploading to a server and are parsed and indexed by the server.

Note: The following content is specific to packages that are not uploaded to a server. If uploading to a server is desired, all fields must be included; otherwise, the upload will fail. During the upload process, the server automatically checks whether the package configuration meets the requirements.

In the following content, I will provide the minimal configuration set. Taking the `packaging` library as an example, it can be reduced to the following content:

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

Yes, only the above six configuration items are needed.

If users still find this configuration too complex, it can be further simplified as follows:

```json
{
    "name":"packaging",
    "version":"1.0.0",
    "summary":"python-packaging-like lib for c++, used for version management",
    "autoScan": true
}
```

At this point, the `publisher` and `isGlobal` fields are also removed.

---

Now, let's describe the meaning of these fields.

### name

The `name` represents the package name. Users can define any name they like.

The name must consist of `English uppercase and lowercase letters`, `numbers`, `hyphens (-)`, `underscores (_)`, and `dots (.)`. The first character must be an English letter.

Here, it is recommended that users use the format `YourName.FunctionName` for the package name.

---

### version

The `version` represents the package version number.

The version format must be written as `major`.`minor`.`patch`. It cannot be in any other format, such as `*` or `x`.

`major`, `minor`, and `patch` represent the major version, minor version, and patch version, respectively, and they must be numbers.

Currently, the version does not support additional information such as `beta`, `alpha`, or `pre`.

---

### summary

The `summary` is a brief and concise description of the software. It is used to inform users about the purpose of the package. The reason for requiring this configuration is that the `ipc packages` command lists a brief description of the library, and this brief description is the content of the `summary`.

---

### autoScan

The `autoScan` field indicates whether IMakeCore automatically scans the entire package and adds the files in the package to the project and compilation process.

The `autoScan` field is a boolean field. It determines how the package files are processed and how the contents of `.cpp`, `.h`, `.ui`, `.res` macros are associated with the project. This will be detailed in the following content on file handling. In this documentation, users need to configure `autoScan` to `true` to enable automatic scanning mode to load the package content. Later documentation will describe how to handle the case when `autoScan` is `false`.

---

### publisher

The `publisher` field represents the uploader's name. This field is the user's registered name in IPubCore.

If the user omits this field, the default value is the name configured by the user in IMake. Users can view their user name using the `ipc user` command and set it using `ipc user set`. The default content of `ipc user` is `default`. Therefore, if this field is omitted, the publisher defaults to `default`.

---

### isGlobal

This field indicates whether the package is a public package. A public package allows the publisher field to be omitted when referencing the package.

For example, when referencing the `ICore` package, you can directly import it as follows:

```json
"ICore" : "1.0.0"
```

Alternatively, you can write the full package name, which includes the `publisher` and `name` fields separated by a forward slash (`/`), as shown below:

```json
"yuekeyuan/ICore" : "1.0.0"
```

Because the `ICore` package has `isGlobal` set to `true`, we can omit the `yuekeyuan` publisher field and the forward slash, and directly use `ICore`.

What is the benefit of this approach? It allows multiple users to create and upload packages with the same name without worrying about name conflicts. For example, if a package is well-maintained and becomes popular, it can be made a public package for others to use, and the publisher's name can then be omitted.

---

### Omitting `isGlobal` and `publisher` Simultaneously

In the simplified configuration above, we omitted both the `isGlobal` and `publisher` fields. By default, the package is considered a public package (`isGlobal` is `true`), and the publisher name can be omitted when referencing the package.

This is particularly suitable for local packages that are not uploaded to a server. Users can directly reference the package by name. In this documentation, we will only explain how to simply customize a package and will not involve content related to server uploads, so users can safely omit these two fields.

If uploading to a server is desired, all fields must be properly configured.

---

## Package Location

User-defined packages can be placed in any subfolder of a `libstore`. For example, by calling the `ipc libstores` command, all available `libstore` folders will be displayed:

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

The above `libstore` is a global `libstore`. Users can also configure their own `libstore` folder locations to store required packages using the `ipc libstores add` command.

Note: The contents placed in the `libstore` folder must be a folder containing `package.json`. Do not place the `package.json` file directly in the `libstore` folder.

---

## Summary

In the tutorial above, we described what a minimal package looks like. Additionally, there is much more content that has not been explained.