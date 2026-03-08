# Controller定义

## 关于 Controller

Controller 是用于描述应用程序中处理用户输入和更新应用程序状态的组件。它通常负责接收用户界面层的请求，处理数据，并将结果返回给视图层。Controller 作为MVC（Model-View-Controller）架构中的核心部分，确保了应用程序的业务逻辑与用户界面的分离。

比如在 Spring 中，使用 `@RestController` 注解来标记一个类作为 Controller，而 Flask 使用函数装饰器 `@app.route` 来处理请求。以下是简化后的代码示例：

=== "Spring 示例"
    ```java
    import org.springframework.web.bind.annotation.GetMapping;
    import org.springframework.web.bind.annotation.RestController;

    @RestController
    public class MyController {

        @GetMapping("/hello")
        public String sayHello() {
            return "Hello, World!";
        }
    }
    ```

=== "Flask 示例"
    ```python
    from flask import Flask
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    if __name__ == '__main__':
        app.run()
    ```

 在这两个示例中，Spring 使用注解来标记 Controller，而 Flask 使用装饰器来处理请求。



在 IHttpCore 中我们使用相似的方式定义一系列的 Controller。

## IHttpCore 中的 Controller

我们根据上面的示例先写一个简单的IHttpCore 的 Controller 类。

=== "MyController.h"
    ```c++
    #pragma once

    #include "http/controller/IHttpControllerInterface.h"

    class MyController : public IHttpControllerInterface<MyController>
    {
        Q_GADGET
    public:
        MyController() = default;

        $GetMapping(hello, /hello)
        QString hello();
    };
    ```



=== "MyController.cpp"

    ```c++
    #include "MyController.h"

    QString MyController::hello()
    {
        return "hello";
    }
    ```

这样我们的一个 Controller 类就定义好了。在下面的内容中，我将逐一介绍其中的内容。



### lHttpControllerInterface

在 MyController.h 文件中，第3行代码将 `IHttpControllerInterface.h` 头文件 导入到当前类中。在第5行代码 MyController 以  CRTP 的方式继承了 IHttpControllerInterface。这样表示MyController 是我们框架中定义的一个 HttpController。



=== "IHttpControllerInteface 的声明"

```c++
template<typename T, bool enabled = true>
class IHttpControllerInterface 
: public ITaskWareUnit<T, IHttpTaskCatagory, enabled>, public ISoloUnit<T>;
```

#### 功能

IHttpControllerInterface 是一个至关重要的基类。这个基类做了一下的事情：

- 首先，它会在程序运行的初期静态初始化自身，创建一个实例对象。

- IHttpControllerInterface本身继承于 ITaskWareUnit，它是我们任务系统中的一个task。 在初次创建实例对象的时候，会将自身注册进我们的任务系统中去。

- 在程序启动的时候，任务系统会按照一定的次序逐个执行注册的任务。当执行到我们的 IHttpControllerInterface的时候，他会执行我们在基类中定义的 `$task()` 函数。

- - 关于 任务系统，参考 `core` 中的内容。

- 在执行 IHttpControllerInterface 中的 任务 的时候，他会解析整个 Controller 的内容。查找一个个的url路径和 可调用的函数，并将路由和函数绑定，成为一系列的 `IHttpControllerAction`，并将 Action 注册进系统中。

- 在用户请求到达的时候，系统会查找注册进系统的 Action， 如果Action 符合请求。则会调用该 Action。如果没有Action匹配,则会进行异常响应机制。



#### 禁用IHttpControllerInterface

在 IHttpControllerInterface 的签名中，他的第一个模版参数用于 CRTP， 必须填写上继承的基类。而第二个参数是一个 非类型模板参数（NTTP, Non-Type Template Parameter ), 它的类型是 bool 类型，默认值是 true。

这个模版参数的作用是是否允许当前的 Controller被注册到系统当中。如果值为 true，或者省略不写使用默认值的时候，Controller 会被注册到系统当中。如果值为false 的时候，则是这个 Controller不会被注册到任务系统中去，自然的Controller不会生成 Action，也不会被调用。

所以如果用户在开发过程中，想临时屏蔽该类，可以将第二个模版参数设置成 false。 这样这个 Controller就不会起作用。如果将代码中第5行改为:

=== "禁用IHttpControllerInterface"
    ```c++
    class MyController : public IHttpControllerInterface<MyController, false>
    ```

那么，这个Controller类不会被启用，`/hello` 路由连同函数也不会被注册，用户就无法访问 `/hello` 路径。

当然，如果用户确定这个 Controller 不会再被使用，需要删掉该类，而不是将该类标记为不启用。



### Q_GADGET

在 代码的第7行，我们写了一个宏 `Q_GADGET` 在这里。这个事 Qt 中声明的一个宏，用于反射功能。

`GADGET` 英文的意思是小部件，小零件的意思。如果用户是写 Qt 程序， 更常用的是 `Q_OBJECT` 这个宏。

`Q_GADGET` 和 `Q_OBJECT` 是 Qt 框架中用于元对象系统的宏。它们都与 Qt 的反射系统有关，但它们的用途和实现方式有所不同。`Q_OBJECT` 提供了完整的反射功能，`Q_GADGET` 提供一个更基本的反射功能。但是Q_GADGET 更轻量级,他不需要类继承于 `QObject`， 并且他提供的反射功能刚好够用，我们用到的反射功能如下。

- `Q_INVOKABLE` 提供了类方法的反射。
- `Q_PROPERTY` 提供了类字段的反射
- `Q_CLASS_INFO` 提供了一类一些额外的信息。

关于 `Q_GADGET` 的内容，可以参考 `QtDoc` 或者我们的 `core` 中间的文档。

在 Controller的定义中，`Q_GADGET` 是必不可少的。如果缺少该宏定义，则程序会编译失败。他提供了url 信息，函数信息的反射。



### $AsController

在 Spring 中，有 `@RequestMapping` 这个注解。这个注解可以定义在 类的级别上面，表示这个类的路由前缀。同样的，在 IHttpCore 中我们也有一个 `$AsController` 宏注解，这个注解的作用是定义一个路由前缀，类中所有的方法的路由会在生成的时候添加上该前缀。

示例如下：

=== "示例"

    ```c++
    #pragma once

    #include "http/controller/IHttpControllerInterface.h"

    class MyController : public IHttpControllerInterface<MyController>
    {
        Q_GADGET
        $AsController(MyController)
    //  $AsController(/admin/about)    
    public:
        MyController() = default;

        $GetMapping(hello, /hello)
        QString hello();
    };
    ```

在上述Controller中，hello() 函数的路由不再是  `/hello` ,而会变成 `/MyController/hello`, 这个是因为在程序第8行我们定义了`$AsController(MyController)` 这个宏注解。通过该宏注解，该类的所以路由都会以  `/MyController` 开头。

如果我们注销掉第8行，开启第 9 行，则， `hello()` 函数的路由会变成 `/admin/about/hello`。具体的路由规则可以参考 `路由规则`的文档，函数的路由规则对应 `$AsController` 宏注解同样适用。



### 函数的定义

在 `MyController.h` 的第11-12行我们定义了一个函数mapping

=== "mapping"
    ```c++
    11   $GetMapping(hello, /hello)
    12   QString hello();
    ```

第11 行是一个宏注解，表示这个是一个 GET 请求， 响应函数是 `hello`， 也就是宏注解的第一个参数。响应的路由是 `/hello` 这个url，是宏注解的第二个参数。 此外我们还有 `$PostMapping`, `$DeleteMapping` 等一系列的 Mapping。

这篇文档不详细展开这类宏注解，具体内容请参考 `http路由` 相关的内容。



第12行是响应的函数。这个函数必须跟在 `$GetMapping` 宏注解的后面。防止宏注解的前面或者宏注解和函数之间有其他内容均不可。

这篇文档也不会详细解释响应函数，具体的内容参考 `http函数` 相关的内容。