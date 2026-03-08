# IMakeCore Package

> This document describes the editing and generation of plugins

## Plugins

In IMakeCore, developers can introduce a series of plugins. After accumulating a certain amount of code, they can also encapsulate the code into IMakeCore packages to achieve code reuse. This document explains how to encapsulate developed code into an IMakeCore package and how to publish the package.

IMakeCore currently supports qmake integration and cmake integration. Therefore, for plugin encapsulation, developers need to focus on three files.

-   package.json

    This file is used to define a plugin. It includes a series of plugin information, such as group, name, version, dependencies, etc.

-   .pri file

    This is a file for qmake integration. When qmake includes this file, the package will be introduced into the project.

-   .cmake file

    This is a cmake module file used for cmake integration. When a cmake project includes this file, the package will be introduced into the project.

Now, let's elaborate on these three files.

### package.json

### Detailed Explanation of Basic Attributes

#### name

Defines the unique identifier name of the plugin. It is recommended to use lowercase letters and hyphens for naming1. For example: "my-plugin"

#### group

Specifies the organization or group to which the plugin belongs. It is typically represented using reverse domain name notation1. For example: "com.example.plugins"

#### version

Adheres to the semantic versioning specification (MAJOR.MINOR.PATCH), indicating the plugin's version number7. For example: "1.0.0"

#### author

Plugin author information, which can include name, email, and other contact details1. Format example: "John Doe [john@example.com](mailto:john@example.com)"

#### summary

A brief description of the plugin (within 50 characters), used for a quick understanding of the plugin's functionality1

#### description

Detailed explanation of the plugin's functionality, features, and usage scenarios1

#### link

Links to plugin-related resources, such as documentation, source code repositories, etc.,1

#### license

The license type of the plugin, such as "MIT", "Apache-2.0", etc.,1

### Advanced Attribute Configuration

#### dependencies

Declares other IMakeCore packages that the plugin depends on1. Format example:

```json
"dependencies": {
  "core-utils": "^1.2.0",
  "network-lib": "~2.1.3"
}
```

#### requires

Specifies the minimum IMakeCore version required for the plugin to run1. Example:

```json
"requires": ">=2.0.0"
```

#### cmake

Configures parameters related to CMake integration13. Can include:

-   module_path: .cmake file path
-   variables: Exported CMake variables
-   targets: Provided CMake targets

#### qmake

Configures parameters related to qmake integration1. Can include:

-   include_path: .pri file path
-   config: Additional qmake configuration items

### .pri File Writing Guidelines

The qmake integration file should contain the following content1:

1.  Define the paths to the header files provided by the plugin
2.  Set necessary compilation options
3.  Link the required library files
4.  Export the plugin version information

Example structure:

```
# Plugin header file path
INCLUDEPATH += $$PWD/include

# Link library configuration
LIBS += -L$$PWD/lib -lmyplugin

# Version definition
DEFINES += MYPLUGIN_VERSION=1.0.0
```

### .cmake File Writing Guidelines

The CMake module file should implement the following functions36:

1.  Define the imported targets of the plugin
2.  Set the header file search paths
3.  Handle dependency relationships
4.  Provide version compatibility checks

Example structure:

```
# Create imported target
add_library(myplugin INTERFACE IMPORTED)

# Set header file path
target_include_directories(myplugin INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}/include
)

# Link dependency libraries
target_link_libraries(myplugin INTERFACE
  other::dependency
)

# Version check
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  MyPluginConfigVersion.cmake
  VERSION 1.0.0
  COMPATIBILITY SameMajorVersion
)
```

### Finding Plugins

IMakeCore provides the following ways to find published plugins4:

1.  Command-line tool: `imake search <keyword>`
2.  Online repository: https://plugins.imakecore.com
3.  IDE Integration: Browse through the plugin market in the development environment
4.  Local cache: Plugins already installed under the `~/.imake/plugins` directory

Plugin publishing process:

1.  Validate the package.json configuration
2.  Run `imake package` to generate the release package
3.  Use `imake publish` to upload to the repository
4.  Use `imake update` to update the version