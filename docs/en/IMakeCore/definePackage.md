# Creating Packages (1)

In the previous documentation, we have used a series of built-in packages, such as the nlohmann/json package, the asio package, the ICore package, the ITcp package, the IHttp package, and so on. Today, we will explain how these packages are created, how users can create their own packages as needed, and how to divide a product into different packages.

> This document describes how to encapsulate source code into a package.

## Overview

Defining a package in package management can be very simple—only a `package.json` file is needed to define a package.

Let's take a very simple example: the Version package in a project.

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

The reason the author is `deepseek` is because this package was generated using `deepseek`, and I made some modifications on top of it. I sincerely apologize for using my name as the `author` field.

With this, the package is configured.

Of course, if users want to enrich this package, they can add many fields to the `package.json` file. They can also add other files to the directory, such as `README.md`, `CHANGELOG.md`, or other documentation, etc.

Below, we will describe the meaning of each field in the `package.json` file in detail. For required fields, a `*` will be marked at the end of the field.

## Package Information

### name`*`

The `name` represents the package name. Users can define their preferred name.

The name must be composed of `English uppercase and lowercase letters`, `digits`, `hyphens (-)`, `underscores (_)`, and `dots (.)`. The first character must be an English letter.

Here, it is recommended to users to use a package name in the format of `your name`.`function name`.

### version`*`

The package version number.

The format of the version number must be `major`.`minor`.`patch`. It cannot be `*`, `x`, or any other format.

`major`, `minor`, and `patch` represent the major version, minor version, and patch version, respectively, and they must be numbers.

Currently, the version does not support additional information such as `beta`, `alpha`, `pre`, etc.

### author`*`

The author's name.

This must be the actual author of the code. Users can upload others' open-source packages for everyone to use, but when uploading, they must correctly attribute the author and not claim it as their own. If the original author wishes to reclaim copyright, the uploader must transfer the rights.

(I am not sure about the specific legal content here. Will this violate the law? If someone knows, please inform me, but please don’t sue me over this matter. I can change it immediately.)

### summary`*`

A brief and concise one-sentence description of the software. This is used to inform users about what the package does.

### keywords`*`

Keywords. This is a string list and can be empty but cannot be omitted.

This is used for search optimization. If the keywords users select are good, it can help users quickly locate your library.

### isGlobal*

This field indicates whether it is a public library. The value `true` means it is a public library. It can be omitted, and when omitted, it defaults to `true`.

If users want to upload the package to IPubCore for everyone to use, the `isGlobal` field is a required field. If this field is missing, users cannot upload the package to the server. However, if users do not need to upload the package to the server for private use, they can omit this field, which will be discussed later.

#### Meaning of the `isGlobal` Field Value

If `isGlobal` is `true`, or if omitted, it indicates that the package is public. When users reference the package, they can omit the `publisher` prefix. If the value of the `isGlobal` field is `false`, then the package is not public, and users must use the `publisher` prefix to reference it.

#### Management of `isGlobal` Field in Package Upload

When uploading a package, the `isGlobal` field must exist. If it is missing, the upload is rejected.

Currently, when users first upload a package, the `isGlobal` field must be `false` and cannot be a public package. Users can apply to make the package public. If the application is approved, then when uploading the package next time, the `isGlobal` field must be `true`. If it is `false`, the upload will be rejected.

The criteria for determining whether a package is public include whether it is the original author, download volume, star count on GitHub, star count on IPubCore, etc. Generally, only one package with a given name can be public.

#### Case of Missing `isGlobal` Field

If the `isGlobal` field is missing, the package is considered public. A public package is one that can be referenced without the `publisher` prefix. For more details, see [Public Package](globalPackage.md).

Packages defined by users for their own use do not require the `publisher` prefix, making it convenient for users. However, such packages cannot be uploaded.

Note that if the package name conflicts with a cached public package name locally, the IMake program will directly report an error.

### publisher*

The `publisher` field represents the uploader's name. This field is the user's registered name on IPubCore.

If users omit this field, the default value is the name configured in IMake. Users can view their username with the command `ipc user` and set it with `ipc user set`.

Users cannot omit this field when uploading. If it is omitted, the upload will be rejected. If the logged-in username does not match the `publisher` field in the package, the upload will also fail.

### autoScan*

The `autoScan` field is a boolean field. It is related to how the package's files are handled and how the C++ and header content, along with macros, are linked to the project. This will be introduced in detail later.

### Other Fields

#### license

The copyright license used by the software.

#### changelog

The content of this update.

#### dependencies

The dependencies of the software.

This field checks for the existence of the defined packages in the dependencies during package loading. If the dependency package does not exist, IMakeCore will report an error during package loading.

The definition of dependencies is as follows:

```json
{
	...
    "dependencies": {
        "ITcp": "*",
        "ICore": "*"
    },
    ....
}
```

Here, the package depends on ITcp and ICore. If these packages do not exist, an error will be reported.

The version definition for dependencies can be `*`, a specific version, or a version range. Version ranges follow the [Semantic Versioning 2.0.0 | Semantic Versioning](https://semver.org/) specification.

#### urls

This is an array of URLs related to the library. Users can add as many as needed.

#### Other Content

No further enumeration will be done here. Users can define any fields they wish, with no uniform specifications.

## Package Code Integration

The `package.json` file provides basic information about the package, and the `autoScan` field determines how the package's compilation-related information and files are handled. Below, this content will be elaborated on.

### User-Provided Package Information

When the `autoScan` field in `package.json` is `false`, it indicates that users want to manage the package code themselves. In the package, users must provide `.pri` and `.cmake` files to support program integration and load the package into the project.

#### .pri File

Users must provide a `.pri` file in the project for the program to use. The file name can be in the following formats:

- `{packageName}.pri`
- `{publisher}@{packageName}.pri`
- `{publisher}@{packageName}@{version}.pri`
- `{packageName}@{version}.pri`

Where `publisher`, `packageName`, and `version` are the values of the `publisher`, `name`, and `version` fields in the `package.json` file. Among these, `packageName` is mandatory, while `publisher` and `version` are optional.

IMake provides the following functions for code management via qmake:

- loadToSources
- loadToHeaders
- loadToIncludes
- loadToResources
- loadToForms
- loadToLibraries
- loadToDefinitions

These functions, by their names, are used to load various resources into the project. Therefore, when defining the `.pri` configuration file, users can use the above functions to perform operations.

In addition to these functions, users can also use Qt's built-in variables such as `HEADERS`, `SOURCES`, `DEFINES`, `LIBS`, etc., to load resources. In essence, the above functions encapsulate Qt's variables for easier resource addition. Using these functions is also synchronized with CMake, which provides the same functions.

#### .cmake File

When the `autoScan` value is `false`, users must also provide a `.cmake` file in the package to enable IMake to support CMake-based project compilation. The `.cmake` file can be named as follows:

- `{packageName}.cmake`
- `{publisher}@{packageName}.cmake`
- `{publisher}@{packageName}@{version}.cmake`
- `{packageName}@{version}.cmake`

Where `publisher`, `packageName`, and `version` are the values of the `publisher`, `name`, and `version` fields in the `package.json` file. Among these, `packageName` is mandatory, while `publisher` and `version` are optional.

IMake provides the following functions for code management via CMake:

- loadToSources
- loadToHeaders
- loadToIncludes
- loadToResources
- loadToForms

- loadToLibraries
- loadToDefinitions

These functions, by their names, are used to load various resources into the project. Therefore, when defining the `.cmake` configuration file, users can use the above functions to perform operations. These functions are consistent with those provided by qmake.

Users can load files using the following methods:

```cmake
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

### Auto-Scanning Package Information

The `autoScan` field tells IMakeCore to use automatic scanning for code loading. Users no longer need to configure `.pri` and `.cmake` files. Even if they are configured, IMake will not use them but will instead scan the files. Therefore, automatic scanning of package information can be used across different project management tools.

When the package information is defined in the project's `packages.json` file,

### Source Handling

### Header Handling

### Resource Handling

### UI File Handling

### Macro Handling

## Custom Package Dependencies

### Package Dependency Definition in CMake

### Package Dependency Definition in qmake

## Package Upload

## Other Considerations