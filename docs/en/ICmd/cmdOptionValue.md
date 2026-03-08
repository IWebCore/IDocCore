<译文内容>  
# Command Line Option Parameters  

> This document describes command line option parameters.  

## Introduction  

A command line option can have a series of parameters to further describe the option. We use the copy command as an example. If the user defines the `--src` option, then this option should have a parameter to specify what the `src` content is.  

## Example  

Let's consider a scenario where the user wants to print output content, and through command line options, they can configure which content can be output.  

Here is a code example:  

=== "OutputCmd.h"  

```cpp  
#pragma once  

#include "cmd/ICmdInterface.h"  

class OutputCmd : public ICmdInterface<OutputCmd>  
{  
    Q_GADGET  
    $AsCmd(/)  
public:  
    OutputCmd();  

    $CmdOption(type)  

    $CmdOptionValue(type, QStringList, printType)  

public:  
    $CmdMapping(output)  
    void output();  
};  
```  

=== "OutputCmd.cpp"  

```cpp  
#include "OutputCmd.h"  

OutputCmd::OutputCmd()  
{  

}  

void OutputCmd::output()  
{  
    qDebug() << type;  
    qDebug() << printType;  
    quick_exit(0);  
}  
```  

The above example is simple. We define a `type` option and a parameter `printType` based on the `type` option. `printType` is a `QStringList` type used to specify the output content type. That is, the `--type` option can be followed by multiple parameters, and these parameters will be placed in the `printType` variable.  

Here are some call examples:  

=== "-?"  

```bash  
PS D:\test\cmd> .\testCmd.exe output -?  

     _____  _    _        _      _____  
    |_   _|| |  | |      | |    /  __ \  
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___  
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \  
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/  
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|  

    [CMD]:  
        testCmd.exe output  
    [Options]:  
        Option  ShortName  Required    NoValue    Memo  
        --type  -          false       false  
    [OptionValues]:  
        Option  Name       TypeName     Nullable  Memo  
        type    printType  QStringList  false  
```  

=== "Without Option Parameter"  

```bash  
PS D:\test\cmd> .\testCmd.exe output --type  

     _____  _    _        _      _____  
    |_   _|| |  | |      | |    /  __ \  
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___  
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \  
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/  
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|  

    cmd defined option value and option value should not be null, but you do not provide option value. [OptionValue]:type  
    [CMD]:  
        testCmd.exe output  
    [Options]:  
        Option  ShortName  Required    NoValue    Memo  
        --type  -          false       false  
    [OptionValues]:  
        Option  Name       TypeName     Nullable  Memo  
        type    printType  QStringList  false  
```  

=== "With Option Parameter"  

```bash  
PS D:\test\cmd> .\testCmd.exe output --type name "create time" detail  

     _____  _    _        _      _____  
    |_   _|| |  | |      | |    /  __ \  
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___  
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \  
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/  
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|  

    true  
    ("name", "create time", "detail")  
```  

In the above calls, the first example shows that the option parameter has been registered. The second example shows that no option parameter was provided, and the program reported an error. The third example shows that option parameters were provided, and the program ran normally.  

Now, let's explain the content of the option parameters one by one.  

## $CmdOptionValue  

This annotation is used to define an option parameter, as in the `printType` option parameter in the example above.  

```cpp  
$CmdOptionValue(type, QStringList, printType)  
```  

The `$CmdOptionValue` annotation has three parameters:  

- Option name: `type`.  

The option name is the name we defined for the option. This must exist; otherwise, the program will report an error during parsing.  

- Option parameter type: `QStringList`.  

This parameter's type and usage are consistent with the format and usage of defining command line parameters. Its type can be bool, numeric types, string types, or composite types. For related content, you can refer to the documentation on parameter types.  

- Option parameter variable name: `printType`.  

This is the name of the member variable used to store the option parameter.  

## $CmdOptionValueMemo  

This is a memo for the option parameter. The first parameter of `$CmdOptionValueMemo` is the option parameter name, and the second parameter is the memo. The memo should be enclosed in double quotes.  

## $CmdOptionValueNullable  

This annotation is used to define whether an option parameter can be null. In the example above, when we define an option parameter and do not input it, the program will report an error. However, when `$CmdOptionValueNullable` is used, the program will not report an error, and the option parameter will use a default value for operation.  

This macro annotation can be used alone. However, if you want to have a user-defined default value, consider using it together with `$CmdOptionValueDeclare`.  

## $CmdOptionValueDeclare  

This annotation is used to define the default value for an option parameter. When the option parameter is annotated with `$CmdOptionValueNullable` and no parameter is provided in the actual request, the default value defined by this annotation will be used.  

For example:  

=== "OutputCmd.h"  

```cpp  
#pragma once  

#include "cmd/ICmdInterface.h"  

class OutputCmd : public ICmdInterface<OutputCmd>  
{  
    Q_GADGET  
    $AsCmd(/)  
public:  
    OutputCmd();  

    $CmdOption(type)  

    $CmdOptionValueNullable(printType)  
    $CmdOptionValueDeclare(type, QStringList, printType)  
    QStringList printType{"name", "time"};  

public:  
    $CmdMapping(output)  
    void output();  
};  
```  

In this program, if the user's command is `some-exe output --type`, the program will use the default values "name" and "time" as the option parameters.  

If the user specifies option parameters, such as `some-exe output --type name "create time" detail`, the option parameters will be "name", "create time", and "detail", rather than the default values.  

## $CmdOptionPreHandle  

This defines a pre-processing function before the option parameter. When ICmd sets a value for the option, it will run this function (if the function is defined).  

For other content, refer to annotations like `$CmdArgsPreHandle`.  

## $CmdOptionPostHandle  

This defines a post-processing function after the option parameter. When ICmd sets a value for the option, it will run this function (if the function is defined) after setting the value.  

For other content, refer to annotations like `$CmdArgsPostHandle`.  

For example, if the user wants to ensure that the option parameter is chosen from a specific set of names and not arbitrary input, they can set a PostHandle function for the option parameter. Inside this function, they can validate the parameters.