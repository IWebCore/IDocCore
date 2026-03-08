# Controller Definition

## About Controller

A Controller is a component used to describe parts of an application that handle user input and update the application's state. It typically receives requests from the user interface layer, processes the data, and returns the result to the view layer. As a core part of the MVC (Model-View-Controller) architecture, the Controller ensures the separation of business logic from the user interface.

For example, in Spring, the `@RestController` annotation is used to mark a class as a Controller, while Flask uses function decorators like `@app.route` to handle requests. Below are simplified code examples:

=== "Spring Example"
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

=== "Flask Example"
    ```python
    from flask import Flask
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    if __name__ == '__main__':
        app.run()
    ```

In these examples, Spring uses annotations to mark Controllers, while Flask uses decorators to handle requests.

In IHttpCore, we define a series of Controllers using a similar approach.

## Controller in IHttpCore

Let's first write a simple IHttpCore Controller class based on the example above.

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

Now, our Controller class is defined. In the following content, I will introduce each part one by one.

### IHttpControllerInterface

In the MyController.h file, line 3 includes the `IHttpControllerInterface.h` header file. Line 5 shows that MyController inherits from IHttpControllerInterface using CRTP. This indicates that MyController is a HttpController defined in our framework.

=== "Declaration of IHttpControllerInterface"
```c++
template<typename T, bool enabled = true>
class IHttpControllerInterface 
: public ITaskWareUnit<T, IHttpTaskCatagory, enabled>, public ISoloUnit<T>;
```

#### Functionality

IHttpControllerInterface is a crucial base class. This class does the following:

- First, it performs static initialization of itself during the initial runtime, creating an instance object.

- IHttpControllerInterface inherits from ITaskWareUnit, which is a task in our task system. During the initial creation of the instance object, it registers itself in our task system.

- During program startup, the task system executes the registered tasks in a certain order. When it reaches IHttpControllerInterface, it executes the `$task()` function defined in the base class.

- It parses the entire Controller content. It searches for each URL path and callable function, binding the routes to the functions and creating a series of `IHttpControllerAction`. These actions are then registered in the system.

- When a user request arrives, the system looks up the registered Action. If the Action matches the request, it is called. If no matching Action is found, an exception handling mechanism is triggered.

#### Disabling IHttpControllerInterface

In the signature of IHttpControllerInterface, the first template parameter is used for CRTP and must specify the base class. The second parameter is a non-type template parameter (NTTP), which is a boolean with a default value of `true`.

This template parameter controls whether the Controller is registered in the system. If the value is `true` or omitted (using the default), the Controller is registered. If the value is `false`, the Controller is not registered, and no Actions are generated or called.

Therefore, if a developer wants to temporarily disable a class during development, they can set the second template parameter to `false`. This prevents the Controller from functioning. However, if a Controller is confirmed to be unused, it should be deleted from the code rather than marked as disabled.

### Q_GADGET

In line 7 of the code, the `Q_GADGET` macro is defined. This is a macro declared in Qt for reflection functionality.

The word "GADGET" means small components or widgets in English. Qt programmers more commonly use the `Q_OBJECT` macro. Both `Q_GADGET` and `Q_OBJECT` are macros in the Qt framework related to the meta-object system. They are connected to Qt's reflection system but serve different purposes and have different implementations. `Q_OBJECT` provides comprehensive reflection capabilities, while `Q_GADGET` offers a more basic reflection feature. However, `Q_GADGET` is lighter and does not require the class to inherit from `QObject`. The reflection features we use are as follows:

- `Q_INVOKABLE` provides reflection for class methods.
- `Q_PROPERTY` provides reflection for class fields.
- `Q_CLASS_INFO` provides additional information about the class.

For more details on `Q_GADGET`, refer to the `QtDoc` or the documentation in our `core`.

In the definition of a Controller, `Q_GADGET` is essential. Without this macro, the program will fail to compile. It provides reflection for URL and function information.

### $AsController

In Spring, there is an `@RequestMapping` annotation. This annotation can be defined at the class level to specify a routing prefix. Similarly, in IHttpCore, there is a `$AsController` macro annotation. This annotation is used to define a routing prefix, which is appended to the routes of all methods in the class during generation.

Example:

=== "Example"
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

In this Controller, the route for the `hello()` function is no longer `/hello` but `/MyController/hello`. This is because, in line 8, we define the `$AsController(MyController)` macro. This causes all routes in the class to start with `/MyController`.

If we comment out line 8 and uncomment line 9, the route for `hello()` will become `/admin/about/hello`. For details on routing rules, refer to the documentation on routing rules. The routing rules for functions also apply to the `$AsController` macro.

### Function Definition

In lines 11-12 of MyController.h, we define a function mapping:

=== "Mapping"
    ```c++
    11   $GetMapping(hello, /hello)
    12   QString hello();
    ```

Line 11 is a macro annotation indicating that this is a GET request, and the response function is `hello`, which is the first parameter of the macro. The corresponding route is `/hello`, the second parameter. Additionally, we have other mappings like `$PostMapping`, `$DeleteMapping`, etc.

This document does not delve deeply into these macro annotations. For specific details, refer to the content related to HTTP routing.

Line 12 is the response function. This function must follow immediately after the `$GetMapping` macro annotation, without any other content in between or before it.

This document does not explain the response function in detail. For more information, refer to the content related to HTTP functions.