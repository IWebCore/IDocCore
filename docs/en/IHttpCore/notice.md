# IHttp Considerations

> This document records the considerations for using IHttp.

## IHttpPythonTest Error

Error Description

```
ABORT: error occurred when executing the command
ABORT CLASS: IPubCore::IHttpPythonTest::IHttpPythonTestAbort
DESCRIPTON: Error: Python path configuration:
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
  sys.base_prefix = 'C:\\Qt\\Qt5.14.2\\Tools\mingw730_32\\bin\\..\\opt'
  sys.base_exec_prefix = 'C:\\Qt\\Qt5.14.2\\Tools\mingw730_32\\bin\\..\\opt'
  sys.platlibdir = 'DLLs'
  sys.executable = 'C:\\Program Files\\Python311\\python.exe'
  sys.prefix = 'C:\\Qt\\Qt5.14.2\\Tools\mingw730_32\\bin\\..\\opt'
  sys.exec_prefix = 'C:\\Qt\\Qt5.14.2\\Tools\mingw730_32\\bin\\..\\opt'
  sys.path = [
    'C:\\Program Files\\Python311',
    'C:\\Program Files\\Python311\\python311.zip',
```

This issue occurs when the mingw compiler executes the IWebCore program. The reason is that QtCreator automatically sets the PYTHONHOME environment variable, leading to multiple Python versions being detected. The solution is simple: set both PYTHONHOME and PYTHONPATH to empty strings in the environment variables, and the error will disappear automatically.

---

## Objects Registered Under mingw Are Not Automatically Registered to the System

This issue is related to the compiler. On the msvc platform, users can omit the constructor or set it to `= default` without affecting Task initialization, registration, or execution. However, in the mingw compiler environment, users must manually define the constructor. Even if the constructor has no content, it must be explicitly written in the `.cpp` file.

---

## What Packages Need to Be Installed for IHttp?

- packaging

  This package is used for IMakeCore.

- pytest

  Used for testing.

- pytest-html

  Used to display Python test results.

  Note: One of these packages did not install successfully on WSL, so on WSL, pytest results are only output to the console and not displayed as a web page.