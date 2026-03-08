# IMakeCore 包

> 本文档描述插件的编辑与生成


## 插件

在 IMakeCore 中，开发者可以引入一系列的插件。在产生一定量的代码积累之后，也会将代码封装成 IMakeCore 的包，来实现代码复用。这篇文档讲述如何将开发出来的代码封装起来，成为一个 IMakeCore的包，并如何发布该包。

IMakeCore 目前支持 qmake 集成和 cmake 集成。所以对于插件的封装，开发者需要关注于三个文件。

- package.json

  这个文件是用于定义一个插件的。它包括插件的一系列信息，如 group， name， version， dependencies 等信息。

- .pri 文件

  这个是用于qmake 集成的文件。当 qmake 包含该文件的时候，该包就会被引入项目当中。

- .cmake 文件

  这个是 cmake 的 module 文件，用于cmake 的集成。当cmake项目包含该文件的时候，该包就会被引入到项目当中去。

下面就这个三个文件展开讲述

### package.json

### 基本属性详解

#### name

定义插件的唯一标识名称，建议采用小写字母和连字符组合的命名方式1。例如："my-plugin"

#### group

指定插件所属的组织或分组，通常采用反向域名表示法1。例如："com.example.plugins"

#### version

遵循语义化版本规范(MAJOR.MINOR.PATCH)，表示插件的版本号7。例如："1.0.0"

#### author

插件作者信息，可包含姓名、邮箱等联系方式1。格式示例："John Doe [john@example.com](mailto:john@example.com)"

#### summary

插件的简短描述（50字以内），用于快速了解插件功能1

#### description

详细说明插件的功能、特性和使用场景1

#### link

插件相关资源的链接，如文档、源码仓库等1

#### license

插件的许可证类型，如"MIT"、"Apache-2.0"等1

### 高级属性配置

#### dependencies

声明插件依赖的其他IMakeCore包1。格式示例：

```json
"dependencies": {
  "core-utils": "^1.2.0",
  "network-lib": "~2.1.3"
}
```

#### requires

指定插件运行所需的最低IMakeCore版本1。示例：

```json
"requires": ">=2.0.0"
```

#### cmake

配置CMake集成相关参数13。可包含：

- module_path: .cmake文件路径
- variables: 导出的CMake变量
- targets: 提供的CMake目标

#### qmake

配置qmake集成相关参数1。可包含：

- include_path: .pri文件路径
- config: 额外的qmake配置项

### .pri文件编写指南

qmake集成文件应包含以下内容1：

1. 定义插件提供的头文件路径
2. 设置必要的编译选项
3. 链接所需的库文件
4. 导出插件版本信息

示例结构：

```
qmakeCopy Code# 插件头文件路径
INCLUDEPATH += $$PWD/include

# 链接库配置
LIBS += -L$$PWD/lib -lmyplugin

# 版本定义
DEFINES += MYPLUGIN_VERSION=1.0.0
```

### .cmake文件编写指南

CMake模块文件应实现以下功能36：

1. 定义插件的导入目标
2. 设置头文件搜索路径
3. 处理依赖关系
4. 提供版本兼容性检查

示例结构：

```
cmakeCopy Code# 创建导入目标
add_library(myplugin INTERFACE IMPORTED)

# 设置头文件路径
target_include_directories(myplugin INTERFACE
  ${CMAKE_CURRENT_LIST_DIR}/include
)

# 链接依赖库
target_link_libraries(myplugin INTERFACE
  other::dependency
)

# 版本检查
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  MyPluginConfigVersion.cmake
  VERSION 1.0.0
  COMPATIBILITY SameMajorVersion
)
```

### 查找插件

IMakeCore提供以下方式查找已发布的插件4：

1. 命令行工具：`imake search <keyword>`
2. 在线仓库：https://plugins.imakecore.com
3. IDE集成：通过开发环境的插件市场浏览
4. 本地缓存：`~/.imake/plugins`目录下的已安装插件

插件发布流程：

1. 验证package.json配置
2. 运行`imake package`生成发布包
3. 使用`imake publish`上传到仓库
4. 通过`imake update`更新版本