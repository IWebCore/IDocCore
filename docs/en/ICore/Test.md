<译文内容>
# Testing

## Testing Overview

C++ has several excellent testing frameworks. I chose QTest and encapsulated it as a task, registering it into the ICore framework. Users can enable or disable tests through configuration or annotations.

## Unit Testing

Unit testing is the most fundamental type of software testing, validating the smallest testable units of software (such as functions, methods, or classes) to ensure the logical correctness of individual modules. Its main characteristics include:

1. **Test Object**: Focusing on independent code logic units, such as functions, class methods, or interfaces;
2. **Execution Phase**: Performed concurrently during development by developers, typically using automated frameworks (like JUnit) to write test cases;
3. **Focus**: Validating module interfaces, local data structures, independent code paths, and error handling capabilities.

The interface for unit testing is `IUnitTestInterface`. Users must inherit from this class to use it. Here is an example:

```cpp
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

In addition to inheriting from `IUnitTestInterface`, users must add the `Q_OBJECT` macro and define the unit test class using `public slots`.

Unit testing is disabled by default and does not run during program startup. Users can enable unit testing using the `$EnableUnitTest(true)` macro annotation. To disable it, users can use `$EnableUnitTest(false)` or omit the annotation.

Here is an example:

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

On the fourth line, the `$EnableUnitTest(true)` macro is used to enable unit testing, which will then run during program startup.

## Integration Testing

Integration testing follows unit testing and primarily verifies the correctness of multiple modules or subsystems working together, especially regarding interface and data interaction issues. Its core characteristics are:

1. **Test Object**: Module interface compatibility, global data structures, and data transmission processes;
2. **Execution Strategy**: Divided into incremental (combining modules step by step) and non-incremental (combining all modules for testing) strategies;
3. **Common Issues**: Problems such as data loss between modules, mismatched interface parameters, and anomalies caused by side effects in global data.

The parent class for integration testing is `IIntegrationTestInterface`, with usage similar to `IUnitTestInterface`.

Integration testing is disabled by default. Users can enable it using the `$EnableIntegrationTest(true)` annotation.

## Functional Testing (System Testing)

Functional testing falls under system testing, verifying whether the system's overall functionality meets user requirements, typically in real-user scenarios. Its characteristics include:

1. **Test Object**: Complete business functionality chains, such as end-to-end scenarios like user registration and payment processes;
2. **Execution Phase**: Conducted after integration testing, by the testing team using tools (such as Selenium) to simulate user operations;
3. **Focus**: Correctness of input and output, performance bottlenecks, and user experience issues.

The parent class for functional testing is `IFunctionTestInterface`, with usage similar to `IUnitTestInterface`.

Functional testing is disabled by default. Users can enable it using the `$EnableFunctionTest(true)` annotation.

## HTTP Testing

In web development, there is a need for HTTP testing, typically using external tools for recording. In IWebCore, the `IHttpPythonTest` functionality is implemented, allowing pytest to test HTTP requests one by one after the entire project has started. For more details, please refer to the content related to `IHttpCore`.