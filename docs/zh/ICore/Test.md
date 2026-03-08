# 测试

## 测试概述

c++中有诸多优秀的测试框架。我选择 QtTest 进行了一个简单的封装来作为 ICore 基本的测试框架。封装的内容是将 QTest 封装成任务的形式，注册到 ICore 框架中，用户可以通过配置，可以通过注解的形式启动或者关闭 测试。


## 单元测试

单元测试是软件测试中最基础的测试类型，针对软件的最小可测试单元（如函数、方法或类）进行验证，目的是确保单个模块的逻辑正确性14。其主要特点包括：

1. ‌**测试对象**‌：聚焦代码逻辑的独立单元，例如函数、类方法或接口；
2. ‌**执行阶段**‌：开发过程中由开发者同步完成，通常借助自动化框架（如JUnit）编写测试用例48；
3. ‌**关注点**‌：验证模块接口、局部数据结构、独立代码路径及错误处理能力。

单元测试的接口是 `IUnitTestInterface`, 用户使用该测试需要继承此类， 如下是一个案例：

```c++
#pragma once

#include "core/test/IUnitTestInterface.h"

class TestSqlite : public IUnitTestInterface<TestSqlite>
{
    Q_OBJECT
public:
    TestSqlite();

public slots:
    void testInsert();
};
```

如上是TestSqlite 的类。用户除了继承 `IUnitTestInterface` 之外，还需要添加 `Q_OBJECT` 宏， 以及 `public slots:` 来定义这个 单元测试类。

单元测试默认是关闭状态，在程序启动的时候不会进行单元测试，如果用户想启动单元测试，可以使用 `$EnableUnitTest(true)` 宏注解。如果用户想关闭 单元测试，可以使用  `$EnableUnitTest(false)` 宏，或者不写该语句

如下是示例：

```cpp
#include "core/application/IApplication.h"

$SetAppThreadCount(4)
$EnableUnitTest(true)
int main(int argc, char* argv[]) {
    IApplication app(argc, argv);
    app.setThreadCount(4);
    return app.run();
}
```

在第四行我们开启了 单元测试的宏注解，单元测试就会在程序启动的时候进行测试。



## 集成测试

集成测试在单元测试后进行，主要验证多个模块或子系统协同工作的正确性，尤其是接口和数据交互问题26。其核心特点为：

1. ‌**测试对象**‌：模块间的接口兼容性、全局数据结构及数据传递过程27；
2. ‌**执行策略**‌：分为增量式（逐步组合模块）和非增量式（整体组合后测试）两种策略68；
3. ‌**常见问题**‌：模块间数据丢失、接口参数不匹配、副作用引发的全局数据异常等。

集成测试的父类是 `IIntegrationTestInteface`， 使用方法和 `IUnitTestInterface` 一致。

集成测试默认是关闭状态，用户可以通过 `$EnableIntegrationTest(true)` 注解打开集成测试。



## 功能测试（系统测试）

功能测试属于系统测试范畴，验证系统整体功能是否符合用户需求，通常面向真实用户场景36。其特点包括：

1. ‌**测试对象**‌：完整的业务功能链，例如用户注册、支付流程等端到端场景38；
2. ‌**执行阶段**‌：在集成测试完成后，由测试团队通过工具（如Selenium）模拟用户操作68；
3. ‌**关注点**‌：输入输出的正确性、性能瓶颈及用户体验问题。

功能测试的父类是 `IFunctionTestInterface` ,使用方法和 `IUnitTestInterface` 一致。

功能测试默认是关闭状态，用户可以通过 `$EnableFunctionTest(true)` 注解打开集成测试。



## Http 测试

在web开发中，有http 测试的需求，一般使用外部的工具进行测试记录，在IWebCore 中，实现了 IHttpPythonTest 功能，可以在整个项目启动之后，执行 pytest 对 http 请求进行逐一测试。具体的内容请参考 `IHttpCore` 相关的内容。



