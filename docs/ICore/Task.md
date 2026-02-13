# Task 机制

## Task 机制

在c++中，有一个神奇的机制，odr 机制和全局静态对象机制，通过这个机制，我么可以模拟就 java 语言中的 反转控制和依赖注入机制， 从而使 IWebCore 可以变得像 Spring 一样强大。在这个机制中，我们极大的解耦了 c++ 文件之间的关联，将一个个的类定义为独立的功能，而通过这些功能的自组织，来完成一系列的功能，实现增量开发。

### 全局类的静态初始化

#### 单文件中的全局静态变量

在c++中，如果一个对象被定义为全局静态对象，那么这个对象就会在 main函数执行之前被初始化。这个是一个有趣的内容。如下 `main.cpp` 文件：

```cpp
#include <iostream>

class Abc {
public:
	Abc() {
		std::cout << __FUNCTION__ << " " << __LINE__ << std::endl;
	}
};

static Abc abc;

int main()
{
	std::cout << __FUNCTION__ << " " << __LINE__ << std::endl;
}
```

它的输出是：

```
Abc::Abc 6
main 14
```

在上面的代码中，我们可以看到 Abc 的构造函数优先于 main 函数执行。这个机制就是我们 ICore中Task执行的基本原理.

#### 不同文件中的全局静态变量

在上面的示例中，我们再变换一次，将Abc 和 main 拆分成两个不同的文件。Abc.cpp 和 main.cpp

`Abc.cpp` 文件如下：

```cpp
#include <iostream>

class Abc {
public:
	Abc() {
		std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;
	}
};

static Abc abc;
```

`main.cpp` 文件如下：

```cpp
#include <iostream>

int main()
{
	std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;
}
```

这个程序执行输出如下：

```CPP
c:\users\yue\source\repos\project3\project3\abc.cpp     Abc::Abc        6
c:\users\yue\source\repos\project3\project3\main.cpp    main    5
```

在这个输出中，Abc 的构造依然优先于 main 函数执行，这个没有改变。当然，这里我想说的是我们在这一步实现了一件事情，就是我们把这个程序拆分成了两个部分执行。不要小看这一点，我们在这一步实现了代码的`高内聚`，也就是说我们可以独立编辑 Abc 类而不影响main 函数。

#### 将对象 耦合起来

在上面一步中，我们实现了内聚，下面我们将对象耦合起来，耦合的本质依然是 `static` 的，不过这里我们使用函数返回静态局部变量，我们新添加一个 头文件， Container.h

```c++
#pragma once

#include <vector>
#include <string>

inline std::vector<std::string>& getContainer() 
{
	static std::vector<std::string> container;
	return container;
}
```

这里注意两点，一个是我们使用了inline 修饰函数。使用inline 的目的是我不想再定义一个 Container.cpp 文件。另一个是我们返回的对象是一个引用对象，这个引用对象在函数内被定义为局部静态变量。

为什么我们使用函数来返回局部静态变量，而不是直接定义一个 全局静态变量呢？这个是因为全局静态变量的初始化时间是没有办法控制的，它和其他的全局静态变量的初始化顺序是不固定的，而我们通过函数来包裹一层，那么这个静态变量的初始化时间则是确定的。局部静态变量在它首次调用的时候初始化。通过这种方式，我们就保证了我们所引用的内容一定是存在且被初始化掉的，不会导致程序崩溃。

Abc.cpp 修改如下：

```c++
#include <iostream>
#include "Container.h"

class Abc {
public:
	Abc() {
		std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;
		
		getContainer().push_back("hello world");
	}
};

static Abc abc;

```

在第9行中，我们获取到 container的引用，并在 container 中添加了一个字符串 ”hello world“。

main.cpp 文件修改如下：

```cpp
#include <iostream>
#include "Container.h"

int main()
{
	std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;
	
	for (const auto value : getContainer()) {
		std::cout << value << std::endl;
	}
}
```

修改后的成效运行如下：

```
c:\users\yue\source\repos\project3\project3\abc.cpp     Abc::Abc        7
c:\users\yue\source\repos\project3\project3\main.cpp    main    6
hello world
```

在这里，我们将 Abc类和 main 函数通过 getContainer 连接在了一起，实现了 Abc 类和 main 函数的耦合。由此我们实现了程序中的内聚和耦合。

上面的代码内容很简单，原理也很简单，但却是有大的用处。比如我们要实现一个 Config 模块，那么用户可以定义很多如 Abc 类一样的 Config 类，Config 类中将自己想要的配置写入一个通过函数返回的局部静态对象中。那么用户可以在不修改原有代码的基础之上添加任意多的Config 类，来实现配置的注入。这个就是我们实现 IOC 和 DI 的基础。

### 静态类任务化

#### 全局静态初始化的问题

在上面的代码中，实现了一个简单的类注入的内容，但是这里存在一个初始化顺序的问题，我们举例说明。

我们新建一个Def 类，如下：

Def.cpp

```c++
#include <iostream>
#include "Container.h"

class Def {
public:
	Def() {
		std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;

		getContainer().push_back("Def hello world");
	}
};

static Def def;

```

此时程序执行结果输出如下：

```
c:\users\yue\source\repos\project3\project3\def.cpp     Def::Def        7
c:\users\yue\source\repos\project3\project3\abc.cpp     Abc::Abc        7
c:\users\yue\source\repos\project3\project3\main.cpp    main    6
Def hello world
hello world
```

在上面我们看见 Def 类优先于 Abc 类执行, Def 注册的内容优先于 Abc 的内容输出。

那么问题就在这里，就是所有的编译器都是 Def 优先于 Abc 执行吗？不是的，这个没有规定，没有依据，换一个编译器可能 Abc 就优先于 Def 执行了。

还有一个问题，如果Abc 类和 Def 类必须有优先级，Abc 类一定要优先于 Def 类执行，这个怎么办？

#### 添加一个任务模块

针对于上面提出的第二个问题，Abc 一定要优先于 Def 执行，这个真的没有办法保证。但是我们可以做一点变化，就是在Abc和Def 执行的时候，不是直接向 Container 中注入内容，而是注入一个任务，任务在执行的时候排下顺序，那么这个时候我们就一定能够保证 Abc 注入的内容一定是优先于 Def 注入的内容执行的。

我们定义一个 Task 模块：

`Task.h`

```cpp
#pragma once

#include <vector>

class Task
{
public:
	virtual int order() const = 0;
	virtual void task() = 0;
};

inline std::vector<Task*>& getTask()
{
	static std::vector<Task*> task;
	return task;
}
```

在这个类中，定义了两个纯虚函数，一个是 `order()` 另外一个是 `task()`。`order()` 的目的是用于排序， `task()` 的目的是用于将 对象注入到 Container 中去。

之后，我们修改Abc 类和 Def 类，如下：

`Abc.cpp`

```cpp
#include <iostream>
#include "Task.h"
#include "Container.h"

class Abc : public Task{
public:
	Abc() {
		std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;
		
		getTask().push_back(this);
	}

	// 通过 Task 继承
	virtual int order() const override
	{
		return 0;
	}
	virtual void task() override
	{
		getContainer().push_back("hello world");
	}
};

static Abc abc;

```

`Def.cpp`

```cpp
#include <iostream>
#include "Task.h"
#include "Container.h"

class Def : public Task {
public:
	Def() {
		std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;

		getTask().push_back(this);
	}

    // 通过 Task 继承
	virtual int order() const override
	{
		return 1;
	}
	virtual void task() override
	{
		getContainer().push_back("Def hello world");
	}
};

static Def def;

```

我们对类进行了相同的改造，以 Def 类为例，在第10行，我们将该类注入到了Task容器中去，删除了在这里直接将字符串注入到 Container 中的做法，而在18-21 行，将字符串注入到 Container 中。14-17行，我们重载了 order 函数。

在这个类初始化的时候，第20行的注入并不执行，而是执行第10行的注入，将类本身注入到一个Task 容器中。task() 函数可以在后来通过类指针调用。

此外，  main.cpp 也做相应的修改如下：

```cpp
#include <iostream>
#include <algorithm>
#include "Task.h"
#include "Container.h"

int main()
{
	std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;
	
	std::vector<Task*>& tasks = getTask();
	std::sort(tasks.begin(), tasks.end(), [](Task* t1, Task* t2) {
		return t1->order() < t2->order();
	});

	for (auto& task : tasks) {
		task->task();
	}

	for (const auto value : getContainer()) {
		std::cout << value << std::endl;
	}
}

```

在 main 函数中，我们在11-13行对 Task 容器进行了一次排序，在这里我们在Task 中定义的`order()` 函数派上了用场，它对注入的 Task 对象进行了一次重排序。在15-17行，我们执行了 Task 对象中的 task 函数， 将字符串添加到 Container中去。

此时，不管编译器决定那个类优先初始化类，由于我们从新排序了一次 Task 类，那么这个对Container 对象的修改顺序是一定的，按照我们 order 的顺序执行的。我们实现了之前所说的可以决定那个内容可以被优先执行。

此次程序的输出如下：

```
c:\users\yue\source\repos\project3\project3\def.cpp     Def::Def        8
c:\users\yue\source\repos\project3\project3\abc.cpp     Abc::Abc        8
c:\users\yue\source\repos\project3\project3\main.cpp    main    8
hello world
Def hello world

```

可以看到 Def 仍然优先于Abc 被构造，但是 Abc 注入的内容却是优先于 Def 执行。我们达到了我们的目的。

### TaskManage

在实际的应用中，我们对于 Task 容器的代码如下：

```cpp
inline std::vector<Task*>& getTask()
{
	static std::vector<Task*> task;
	return task;
}
```

像这样的代码工作起来非常好，但是在实际的工程中，我们会将更多的功能赋予 Task，所以会用单例模式封装该代码

```cpp
#pragma once

#include <algorithm>
#include <vector>

class Task
{
public:
	virtual int order() const = 0;
	virtual void task() = 0;
};

class TaskManage
{
private:
	TaskManage() = default;
public:
	static TaskManage& instance() {
		static TaskManage inst;
		return inst;
	}
	void registTask(Task* t) {
		m_tasks.push_back(t);
	}
	void sortTask() {
		std::sort(m_tasks.begin(), m_tasks.end(), [](Task* t1, Task* t2) {
			return t1->order() < t2->order();
		});

	}
	void executeTask() {
		for (auto task : m_tasks) {
			task->task();
		}
	}

private:
	std::vector<Task*> m_tasks;
};
```

在上面的代码中，我们不再是使用 返回静态变量引用的函数的形式来定义一个 Container, 而是使用单例的形式来注册对象。在TaskManage 中，可以看到`registTask(Task* t)` 函数来注册对象。`sortTask()` 函数来排序对象，而`executeTask()` 来执行对象。一切都被封装起来了，一切都井然有序，实现了代码的内聚。

那对于此，其他的代码修改如下：

`Abc.cpp`

```cpp
#include <iostream>
#include "Task.h"
#include "Container.h"

class Abc : public Task{
public:
	Abc() {
		std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;
		
		TaskManage::instance().registTask(this);
	}

	virtual int order() const override
	{
		return 0;
	}
	virtual void task() override
	{
		getContainer().push_back("hello world");
	}
};

static Abc abc;

```

在第10行，更换了注册的方式。

`Def.cpp`

```cpp
#include <iostream>
#include "Task.h"
#include "Container.h"

class Def : public Task {
public:
	Def() {
		std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;

		TaskManage::instance().registTask(this);
	}

	virtual int order() const override
	{
		return 1;
	}
	virtual void task() override
	{
		getContainer().push_back("Def hello world");
	}
};

static Def def;
```

`main.cpp`

 ```c++
#include <iostream>
#include <algorithm>
#include "Task.h"
#include "Container.h"

int main()
{
	std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;
	
	TaskManage::instance().sortTask();
	TaskManage::instance().executeTask();

	for (const auto value : getContainer()) {
		std::cout << value << std::endl;
	}
}
 ```

这里可以看到 关于 Task 的代码完美的封装起来了。



### 构造函数的问题

在上面的代码中，我们必须在构造函数中将 类本身注册到 TaskManage 中，也必须在 cpp 文件中定义 `static Def def` 这样的代码来，这样的代码实在是没有美感，并且容易出错。那么我们是否可以在 Task 基类中来实现这两个步骤呢?

答案是可以的。祁宇在 [**通过 odr use 与类型推导逼迫编译器生成代码**](http://purecpp.cn/detail?id=2458) 这篇文章中提出了一个方法。不过我最喜欢的方法，也是在ICore中使用的方法则是 drogon 的方法，这里展示一下大佬[an-tao (An Tao)](https://github.com/an-tao)的代码：

```cpp
template <typename T, bool AutoCreation = true>
class HttpController : public DrObject<T>, public HttpControllerBase
{
  public:
    static constexpr bool isAutoCreation = AutoCreation;

  protected:
    template <typename FUNCTION>
    static void registerMethod(
        FUNCTION &&function,
        const std::string &pattern,
        const std::vector<internal::HttpConstraint> &constraints = {},
        bool classNameInPath = true,
        const std::string &handlerName = "")
    {
        if (classNameInPath)
        {
            std::string path = "/";
            path.append(HttpController<T, AutoCreation>::classTypeName());
            LOG_TRACE << "classname:"
                      << HttpController<T, AutoCreation>::classTypeName();

            // transform(path.begin(), path.end(), path.begin(), [](unsigned
            // char c){ return tolower(c); });
            std::string::size_type pos;
            while ((pos = path.find("::")) != std::string::npos)
            {
                path.replace(pos, 2, "/");
            }
            if (pattern.empty() || pattern[0] == '/')
                app().registerHandler(path + pattern,
                                      std::forward<FUNCTION>(function),
                                      constraints,
                                      handlerName);
            else
                app().registerHandler(path + "/" + pattern,
                                      std::forward<FUNCTION>(function),
                                      constraints,
                                      handlerName);
        }
        else
        {
            std::string path = pattern;
            if (path.empty() || path[0] != '/')
            {
                path = "/" + path;
            }
            app().registerHandler(path,
                                  std::forward<FUNCTION>(function),
                                  constraints,
                                  handlerName);
        }
    }

    template <typename FUNCTION>
    static void registerMethodViaRegex(
        FUNCTION &&function,
        const std::string &regExp,
        const std::vector<internal::HttpConstraint> &constraints =
            std::vector<internal::HttpConstraint>{},
        const std::string &handlerName = "")
    {
        app().registerHandlerViaRegex(regExp,
                                      std::forward<FUNCTION>(function),
                                      constraints,
                                      handlerName);
    }

  private:
    class methodRegistrator
    {
      public:
        methodRegistrator()
        {
            if (AutoCreation)
                T::initPathRouting();
        }
    };

    // use static value to register controller method in framework before
    // main();
    static methodRegistrator registrator_;

    virtual void *touch()
    {
        return &registrator_;
    }
};

template <typename T, bool AutoCreation>
typename HttpController<T, AutoCreation>::methodRegistrator
    HttpController<T, AutoCreation>::registrator_;
}  // namespace drogon
```

这里代码不做详细的解释，我基于这个代码做了进一步的封装，可以使代码更加清晰，但是原理还是这样：

```cpp
template<typename T, typename Catagory, bool enabled=true>
class ITaskWareUnit : public ITaskWare
{
    $AsTaskUnit(ITaskWareUnit)
    Q_DISABLE_COPY_MOVE(ITaskWareUnit)
protected:
    ITaskWareUnit() = default;
    virtual ~ITaskWareUnit() = default;

protected:
    virtual const std::string& $name() const final;
    virtual const std::string& $catagory() const final;
};

template<typename T, typename Catagory, bool enabled>
const std::string& ITaskWareUnit<T, Catagory, enabled>::$name() const
{
    static const std::string name = IMetaUtil::getBareTypeName<T>();
    return name;
}

template<typename T, typename Catagory, bool enabled>
const std::string& ITaskWareUnit<T, Catagory, enabled>::$catagory() const
{
    static const std::string name = IMetaUtil::getBareTypeName<Catagory>();
    return name;
}

$UseTaskUnit2(ITaskWareUnit)
{
    if constexpr (enabled){
        static std::once_flag flag;
        std::call_once(flag, [](){
            ITaskManage::instance().addTaskWare(&ISolo<T>());
        });
    }
}

```

这里代码也不做解释，用户可以很简单的使用该代码，举例如下：

```cpp
template<typename T, bool enabled=true>
class IStartupTaskInterface : public ITaskWareUnit<T, IStartupTaskCatagory, enabled>, public ISoloUnit<T>
{
public:
    IStartupTaskInterface() = default;

public:
    virtual double $order() const override;
    virtual void $task() = 0;
};

template<typename T, bool enabled>
double IStartupTaskInterface<T, enabled>::$order() const
{
    return 50;
}
```

这个类是在ICore程序启动的时候开始执行类的基类，用户可以继承这个类，示例如下：

```cpp
class IBannerTask : public IStartupTaskInterface<IBannerTask>
{
private:
    virtual void $task() final;
    virtual double $order() const final;
};
```

用户使用的时候，只需要在意最后一个 IBannerTask 的写法即可。



## ICore 中的Task机制

在上面的文档中描述了 Task 机制的实现原理，在ICore中的Task 的原理是一致的，不过 ICore中的Task 更加的复杂一些，也有一些变化。

## 如何使用 Task
