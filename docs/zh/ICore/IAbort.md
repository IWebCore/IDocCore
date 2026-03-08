# IAbort 模块文档

## 模块概述

IWebCore的开发过程中，用户的代码时被任务化，模块化的。开发者所编写的代码是整个代码中的一个个功能点，这些功能点会被封装成一个个的任务（Task），在项目运行的初期，是初始化这一系列的任务。在所有的任务完成初始化的时候，程序开始提供服务。所以对于IWebCore而言，用户可以在任务执行的时候对代码的逻辑进行先期的判断，如果代码符合一定的逻辑，则可以继续执行，如果不符合逻辑，则直接让任务失败。

在 IWebCore 中，通过IAbort 来定义和调用qFatal 来告知开发者程序出现异常。用户通过继承 IAbortInterface 来定义 一个 Abort， 在Abort 中定义错误的名称和信息，通过宏生成相应的静态成员函数，给开发者调用。

### Abort 的异常机制

Abort 模块是一种**轻量级致命错误处理方案**，有以下优点：

- **立即终止**：触发错误后直接终止程序，避免不确定状态扩散。
- **信息聚合**：自动收集错误代码、描述、触发位置等关键信息。
- **可扩展性**：通过模板和宏快速定义新错误类型，支持自定义错误类型和描述。
- **错误标准化**： 通过宏来标准化错误信息，防止用户的错误输入。
- **提前运行时开销**：在程序提供服务之前做检查，不占用程序服务时间和成本。
- **错误信息收集**：自动记录错误代码、描述、触发位置等。
- **代码位置追踪**：自动捕获触发错误的文件名、函数名和行号。

## IAbortInterface

### 如何定义一个 Abort

#### 继承于 IAbortInterface

用户定义自己的 Abort 需要继承 IAbortInterface 宏

```cpp
template<typename T>
class IAbortInterface : public ISoloUnit<T>
{
public:
    IAbortInterface() = default;

public:
    void abort(int code, const char* data, const QString& description, ISourceLocation location);
    void abort(int code, const char* data, ISourceLocation location);
    virtual QMap<int, QString> abortDescription() const = 0;
    virtual QString abortComment() { return {}; }

private:
    void checkAbortInfoLength();
};
```

IAbortInterface 提供一个纯虚函数，abortDescription, 用于对abort 类型的描述，此外，还需要再子类中添加 `$AsAbort` 宏来定义aabort 的字段和函数。

#### `$AsAbort` 宏

- **作用**：声明错误枚举并自动生成对应的 `abortXXX()` 方法。

- **语法**：

  ```c++
  class CustomAbort : public IAbortInterface<CustomAbort> {
    $AsAbort(Error1, Error2, ...)  // 定义错误枚举
  public:
    // 必须实现 abortDescription()
    QMap<int, QString> abortDescription() const override {
      return {
        {Error1, "描述1"},
        {Error2, "描述2"}
      };
    }
  };
  ```

- **原理**：宏展开后生成静态成员方法 `abortError1()`, `abortError2()` 等方法，可直接调用。

- **注意**：这里`$AsAbort` 后面跟随的是圆括号，不是大括号，他本质上是一个宏和宏的参数。

#### `description` 实现

- **职责**：通过 `abortDescription()` 方法返回错误码与描述的映射。这里可以告知开发者为什么会出现这个异常，如何处理这个异常信息等。

- **示例**：

  ```c++
  QMap<int, QString> CustomAbort::abortDescription() const {
    return {
      {NetworkError, "网络连接失败"},
      {InvalidInput, "输入格式错误"}
    };
  }
  ```

- **注意**： 这里的返回的 map 的键值字段必须和 `$AsAbort` 中定义的字段一一对应。Abort 会在初始化的时候检查字段是否缺失，或有多余字段出现。如果有不匹配，则会报错。

### 如何使用 Abort

#### 触发预定义错误（以 `IGlobalAbort` 为例）

```c++
// 直接抛出异常，传入的数据是 用户提供的异常信息
void ISoloUnitDetail::abortError(QString content)
{
    IGlobalAbort::abortSingletonInstanceCreateError(content);
}

// 抛出异常，提供位置信息
if(m_pathFunValidators.contains(name)){
    auto info = name + "IHttpManage::registerPathValidator, path validator already registered";
    IGlobalAbort::abortDuplicatedKey(info, $ISourceLocation);
}
```

注意这里使用了一个参数， `$ISourceLocation`, 这是一个宏，封装了当前的文件位置，函数名称和报错行信息，关于 `$ISourceLocation`, 请参阅后续说明。

#### 2.2 自定义错误类型

**步骤**：

1. 继承 `IAbortInterface` 模板类：

   ```c++
   class NetworkAbort : public IAbortInterface<NetworkAbort> 
   {
     	$AsAbort(ConnectionTimeout, DNSResolutionFailed)
   public:
     	QMap<int, QString> abortDescription() const override {
       	return {
         		{ConnectionTimeout, "连接超时（30秒未响应）"},
         		{DNSResolutionFailed, "域名解析失败"}
       	};
     	}
   };
   ```

2. 触发错误：

   ```c++
   NetworkAbort::abortConnectionTimeout("api.example.com", $ISourceLocation);
   ```

触发错误时，日志将按以下格式输出：

```
NAME: [错误名称]
ABORT: [错误描述]
ABORT CLASS: [错误类名]
ABORT COMMENT: [全局注释（可选）]
DESCRIPTION: [自定义描述（可选）]
SOURCE_LOCATION: FILE [文件名] FUNCTION [函数名] LINE [行号]
```



## IGlobalAbort

### 作用

- **预定义全局错误**：提供一组通用致命错误类型，涵盖常见场景。
- **直接使用**：无需继承即可调用，例如 `IGlobalAbort::abortDuplicatedKey()`。

### 内容

**预定义错误码与描述**：

| 错误码（枚举）                 | 触发场景示例                           | 描述                                     |
| :----------------------------- | :------------------------------------- | :--------------------------------------- |
| `UnVisibleMethod`              | 反射调用了 Qt 元系统中标记为隐藏的方法 | "该方法禁止调用，但 Qt 元系统要求其存在" |
| `UnReachableCode`              | Switch-Case 中未覆盖的分支             | "不应执行到的代码分支"                   |
| `UnImplimentedMethod`          | 未实现的虚方法被调用                   | "功能尚未实现，预计在 v2.0 完成"         |
| `SingletonInstanceCreateError` | 单例类被重复实例化                     | "单例类禁止创建多个实例"                 |
| `DuplicatedKey`                | 数据库插入重复主键                     | "键 'user_id=1001' 已存在"               |

**使用场景示例**：

```c++
// 在单例类的构造函数中检查实例
if (instanceExists) {
  IGlobalAbort::abortSingletonInstanceCreateError(
    "ConfigManager", 
    $ISourceLocation
  );
}
```



## Source Location

在c++20中，标准库支持了 std::source_location，编译器给std::source_location开了洞，这个可以很好的帮助用户定位代码位置。但是在IWebCore中，我们使用的标准是c++17, 所以这里没有办法使用 std::source_location, 于是我们自定义了 ISourceLocation

```cpp
struct ISourceLocation
{
    const char* filename{nullptr};
    const char* function{nullptr};
    int line{0};
};
```

并在此基础上定义了宏 $ISourceLocation， 用于模拟 std::source_location的初始化：

```cpp
#define $ISourceLocation ISourceLocation{__FILE__, __FUNCTION__, __LINE__}
```

所以到这里就可以看懂我们为什么要使用 `$ISourceLocation` 这个宏了。

在IWebCore持续的迭代过程中，$ISourceLocation 会被 std::source_location 所代替。 



## 最佳实践

1. **错误码命名**：使用 `PascalCase` 格式（如 `InvalidRequest`），避免魔法数字。
2. **位置追踪**：始终传递 `$ISourceLocation` 宏，确保日志可定位。
3. **错误描述**：在 `abortDescription()` 中提供明确的解决方案提示（如 "请检查网络配置"）。

通过此模块，开发者可以快速实现**高可维护性**的致命错误管理，尤其适用于框架开发和高可靠性要求的场景。



