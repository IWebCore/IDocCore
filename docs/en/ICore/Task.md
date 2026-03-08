<译文内容>
# Task Mechanism

## Task Mechanism

In C++, there is a powerful mechanism known as the ODR (One Definition Rule) mechanism and the global static object mechanism. By leveraging this mechanism, we can simulate Java's inversion of control (IoC) and dependency injection (DI) mechanisms, enabling IWebCore to become as powerful as Spring. This mechanism greatly decouples the dependencies between C++ files, defining each class as an independent functional unit. Through the self-organization of these functional units, a series of functionalities can be achieved, supporting incremental development.

### Global Static Initialization

#### Static Variables in a Single File

In C++, if an object is defined as a global static object, it is initialized before the main function executes. This is an interesting aspect. Consider the following `main.cpp` file:

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

The output is:

```
Abc::Abc 6
main 14
```

In the above code, you can see that the constructor of `Abc` executes before the main function. This mechanism is the foundation of how `Task` execution works in `ICore`.

#### Static Variables in Different Files

In the above example, we split `Abc` and `main` into two different files: `Abc.cpp` and `main.cpp`.

`Abc.cpp`:
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

`main.cpp`:
```cpp
#include <iostream>

int main()
{
	std::cout << __FILE__ << "\t" << __FUNCTION__ << "\t" << __LINE__ << std::endl;
}
```

The program's output is:

```
c:\users\yue\source\repos\project3\project3\abc.cpp     Abc::Abc        6
c:\users\yue\source\repos\project3\project3\main.cpp    main    5
```

Here, the constructor of `Abc` still executes before the main function, which remains unchanged. However, what we've achieved in this step is splitting the program into two parts. This seemingly small change enables high cohesion, meaning we can edit the `Abc` class independently without affecting the main function.

#### Coupling Objects Together

In the previous step, we achieved cohesion. Now, let's couple the objects together. The essence of coupling is still tied to `static`, but this time we use a function to return a static local variable. We introduce a new header file, `Container.h`:

```cpp
#pragma once

#include <vector>
#include <string>

inline std::vector<std::string>& getContainer() 
{
	static std::vector<std::string> container;
	return container;
}
```

Note two points: First, we use the `inline` keyword for the function to avoid defining a separate `Container.cpp` file. Second, the returned object is a reference to a static local variable within the function.

Why use a function to return a static local variable instead of defining a global static variable directly? Because the initialization time of a global static variable cannot be controlled, and its initialization order relative to other global static variables is undefined. By wrapping it in a function, we ensure that the static variable's initialization time is determined, specifically when it is first called. This guarantees that any content referenced is both present and initialized, preventing program crashes.

Modify `Abc.cpp` as follows:

```cpp
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

On line 9, we retrieve the container reference and add the string "hello world" to it.

Modify `main.cpp` as follows:

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

The modified program's output is:

```
c:\users\yue\source\repos\project3\project3\abc.cpp     Abc::Abc        7
c:\users\yue\source\repos\project3\project3\main.cpp    main    6
hello world
```

Here, we connected the `Abc` class and the main function through `getContainer`, achieving coupling between the `Abc` class and the main function. This demonstrates cohesion and coupling within the program.

Although the above code is simple in content and straightforward in principle, it has significant utility. For example, to implement a `Config` module, users can define multiple classes like `Abc`, where each class writes its desired configurations into a container returned by a function. Users can then add any number of `Config` classes without modifying existing code, enabling configuration injection. This forms the basis for implementing IoC and DI.

### Static Class Taskization

#### Issues with Global Static Initialization

In the previous code, we demonstrated a simple class injection. However, there is an initialization order issue. Let's illustrate this.

Create a new `Def` class as follows:

`Def.cpp`:
```cpp
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

The program's output is:

```
c:\users\yue\source\repos\project3\project3\def.cpp     Def::Def        7
c:\users\yue\source\repos\project3\project3\abc.cpp     Abc::Abc        7
c:\users\yue\source\repos\project3\project3\main.cpp    main    6
Def hello world
hello world
```

In the above output, the `Def` class executes before the `Abc` class, and the content registered by `Def` is output before that of `Abc`.

The question here is: Do all compilers guarantee that `Def` executes before `Abc`? No, there is no defined order. Depending on the compiler, `Abc` might execute before `Def`.

Another issue: If the `Abc` and `Def` classes must have a specific order (e.g., `Abc` must execute before `Def`), how can this be ensured?

#### Adding a Task Module

To address the second issue—where `Abc` must execute before `Def`—there is no guaranteed way to enforce this order. However, we can change the approach. Instead of directly injecting content into the container during initialization, we can inject a task. The task's execution order can be controlled, ensuring that the content injected by `Abc` executes before that of `Def`.

Define a `Task` module:

`Task.h`:
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

This class defines two pure virtual functions: `order()` for sorting and `task()` for executing the task.

Modify `Abc` and `Def` classes as follows:

`Abc.cpp`:
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

	// Override the Task virtual functions
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

`Def.cpp`:
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

	// Override the Task virtual functions
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

In the above code, we modify the classes to inherit from `Task`. For the `Def` class (lines 10-11), we inject the class into the `Task` container instead of directly injecting the string into the container. Lines 18-21 handle the string injection. Lines 14-17 override the `order()` function.

During initialization, line 10 injects the class instance into the `Task` container without executing the task. The `task()` function is called later using the class pointer.

Modify `main.cpp` accordingly:
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

In this `main` function, lines 11-13 sort the `Task` container using the `order()` function defined in `Task`, ensuring the tasks are ordered correctly. Lines 15-17 execute the `task()` function for each task, adding the strings to the container in the specified order.

The output now is:

```
c:\users\yue\source\repos\project3\project3\def.cpp     Def::Def        8
c:\users\yue\source\repos\project3\project3\abc.cpp     Abc::Abc        8
c:\users\yue\source\repos\project3\project3\main.cpp    main    8
hello world
Def hello world
```

Although `Def` still initializes before `Abc`, the content injected by `Abc` executes first. This achieves our goal.

### TaskManage

In practical applications, the `Task` container code might look like this:

```cpp
inline std::vector<Task*>& getTask()
{
	static std::vector<Task*> task;
	return task;
}
```

This works well, but in real-world projects, we might want to encapsulate more functionality into the `Task` class, so we use the Singleton pattern to wrap the code:

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

In this code, we no longer use a function returning a static variable reference to define the container. Instead, we use a Singleton pattern to register objects. The `registTask()` function registers objects, `sortTask()` sorts them, and `executeTask()` executes them. This encapsulates everything neatly, achieving code cohesion.

Other code modifications are as follows:

`Abc.cpp`:
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

	// Override the Task virtual functions
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

`Def.cpp`:
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

	// Override the Task virtual functions
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

`main.cpp`:
```cpp
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

Here, the Task-related code is perfectly encapsulated.

### Issues with Constructors

In the above code, we must register the class instance with `TaskManage` in the constructor, and also define static variables like `static Def def` in the .cpp file. This is not very elegant and can be error-prone. Can we achieve both steps in the base `Task` class?

Yes, this is possible. Qi Yu proposed a method in the article [Forcing the Compiler to Generate Code Using ODR and Type Deduction](http://purecpp.cn/detail?id=2458). However, the method I prefer and the one used in `ICore` is inspired by drogon's approach. Here's a code snippet from the great contributor [an-tao](https://github.com/an-tao):

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
        // ... (code omitted for brevity)
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

    static methodRegistrator registrator_;
};

template <typename T, bool AutoCreation>
typename HttpController<T, AutoCreation>::methodRegistrator
    HttpController<T, AutoCreation>::registrator_;
```

This code is not explained in detail here, but I have further encapsulated it to make the code clearer. The principle remains the same:

```cpp
template<typename T, typename Catagory, bool enabled=true>
class ITaskWareUnit : public ITaskWare
{
    // ... (code omitted for brevity)
};
```

Users can easily use this code, as shown in the example:

```cpp
template<typename T, bool enabled=true>
class IStartupTaskInterface : public ITaskWareUnit<T, IStartupTaskCatagory, enabled>, public ISoloUnit<T>
{
public:
    // ... (code omitted for brevity)
};
```

Users can simply inherit from this class, as shown in the example:

```cpp
class IBannerTask : public IStartupTaskInterface<IBannerTask>
{
private:
    // ... (code omitted for brevity)
};
```

Users only need to pay attention to the final parameter in the inheritance declaration.

## Task Mechanism in ICore

The implementation principles of the Task mechanism described in the above documentation are consistent with those in `ICore`, although the `ICore` implementation is more complex and includes some variations.

## How to Use Task