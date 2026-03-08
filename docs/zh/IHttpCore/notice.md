# IHttp注意事项

> 这篇文档记录IHttp在使用过程中的注意事项

## IHttpPythonTest 报错

错误描述

```
ABORT: error occured when execute command
ABORT CLASS: IPubCore::IHttpPythonTest::IHttpPythonTestAbort
DESCRIPTON: Error:Python path configuration:
  PYTHONHOME = 'C:\Qt\Qt5.14.2\Tools\mingw730_32\bin\..\opt'
  PYTHONPATH = 'C:\Program Files\Python311'
  program name = 'python'
  isolated = 0
  environment = 1
  user site = 1
  safe_path = 0
  import site = 1
  is in build tree = 0
  stdlib dir = 'C:\Qt\Qt5.14.2\Tools\mingw730_32\opt\Lib'
  sys._base_executable = 'C:\\Program Files\\Python311\\python.exe'
  sys.base_prefix = 'C:\\Qt\\Qt5.14.2\\Tools\\mingw730_32\\bin\\..\\opt'
  sys.base_exec_prefix = 'C:\\Qt\\Qt5.14.2\\Tools\\mingw730_32\\bin\\..\\opt'
  sys.platlibdir = 'DLLs'
  sys.executable = 'C:\\Program Files\\Python311\\python.exe'
  sys.prefix = 'C:\\Qt\\Qt5.14.2\\Tools\\mingw730_32\\bin\\..\\opt'
  sys.exec_prefix = 'C:\\Qt\\Qt5.14.2\\Tools\\mingw730_32\\bin\\..\\opt'
  sys.path = [
    'C:\\Program Files\\Python311',
    'C:\\Program Files\\Python311\\python311.zip',
```

这个问题发生在 mingw 编译器执行 IWebCore程序上面，原因是 QtCreator 会自动设置PYTHONHOME 环境变量，导致查找的 python 有多个。这个解决办法也很简单，在环境变量设置中，将 PYTHONHOME  和 PYTHONPATH 全部设置为空字符串就可以了。该错误会自动消失。



## mingw 下注册的对象没有自动注册到系统中去

原因和编译器有关。在msvc下，用户可以省略构造函数，或者将构造函数限定为 `= default` 并不影响Task的初始化，注册和执行。但是在 mingw 编译器环境下，用户需要手动编写构造函数，即使构造函数的内容为空，也要在 cpp 文件中写上构造函数。



## IHttp 需要安装的包有哪些？

- packaging

  这个包是用于 IMakeCore

- pytest

  测试使用

- pytest-html

  用于显示 python 测试结果

  注意这一个包由于在 wsl 上我没有安装成功,所以目前 wsl 上面只会将 pytest 的结果输出到 console里面，不会展示为网页的形式。
  





 

