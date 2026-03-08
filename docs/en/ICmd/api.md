```cpp
# ICmd Usage Interface

### ICmdInterface

The declaration of ICmdInterface is as follows:

```cpp
template<typename T, bool enabled=true>
class ICmdInterface : public ICmdWare, public ITaskWareUnit<T, ICmdCatagory, enabled>, public ISoloUnit<T>
{
public:
    ICmdInterface() = default;

public:
    virtual void $task() final;
};
```

ICmdInterface has two template parameters. The first template parameter is the type to inherit from. The second template parameter is a bool type that indicates whether to use this Cmd. The default value is true, meaning the Cmd is used. If the user explicitly declares this parameter as false, the Cmd will not be parsed and will not be executed.

### $AsCmd

$AsCmd is a macro annotation that performs two functions: defining functions for executing related function calls, and defining prefix paths.

$AsCmd must have parameters, and users can set up to 9 parameters. These parameters, along with the path defined in $CmdMapping, constitute the entire command path. If the path in $AsCmd is `/`, this path will be ignored. Therefore, if the user does not want to define any prefix path in $AsCmd, it should be written as `$AsCmd(/)`. Note that all paths should not be enclosed in quotes.

### $CmdMapping

$CmdMapping is used to define the specific processing function. After CmdAction processes parameters and options and exits the program if necessary, it executes the function defined by $CmdMapping.

The first parameter of $CmdMapping must be the function name. The function defined by $CmdMapping must be specified.

If $CmdMapping has only one parameter, this parameter is both the function name and the function path. The path defined by $AsCmd, plus this path, forms the entire CmdAction path.

If $CmdMapping has other parameters, these parameters define the function path. In this case, the function name is not used as the path.

$CmdMapping can have up to 9 parameters, where the first parameter is the function name, and the remaining 8 are used to define the path.

The path in $CmdMapping can be `/`. If the path is `/`, then the CmdAction path is the one defined in $AsCmd.

A class can define multiple $CmdMapping. If multiple $CmdMapping appear, the functions they define share all parameter and option configurations. In practice, it is not recommended to define multiple $CmdMapping in a class unless they genuinely share all parameters and options.

The return type of the function defined by $CmdMapping must be void. The function parameters can be empty, or of type ICmdRequest or a reference to ICmdRequest. Other types are invalid.

### $CmdMappingMemo

The purpose of $CmdMappingMemo is to provide comments for $CmdMapping, allowing users to understand what the Cmd does.

$CmdMappingMemo has two parameters: the first is the function corresponding to $CmdMapping, and the second is the comment. Note that the comment should be enclosed in double quotes `""`.

### $CmdOption Series

The purpose of $CmdOption is to define command-line options.

The declaration of $CmdOption is as follows:

```cpp
#define $CmdOption(Opt) \
    Q_CLASSINFO( PP_CMD_OPTION(Opt), #Opt)    \
    Q_PROPERTY(bool Opt MEMBER Opt )   \
    bool Opt {false};
```

It has one parameter, Opt, which is the name of the option.

$CmdOption defines a bool variable with the name specified by the first parameter. This variable indicates whether the option is included in the request. If the option is included in the request, the variable is true; otherwise, it is false.

If the user uses this option, they must prepend `--` when sending the Cmd request. For example, if the user defines `$CmdOption(value)`, the request should include `--value`.

If a request contains an option that has not been defined in the Cmd class, the request is invalid, and an error will be reported during program execution.

#### $CmdOptionShortName

This macro annotation is used to define a short name for the option in $CmdOption.

$CmdOptionShortName has two parameters: the first is the name of the corresponding option, and the second is the short name. For example, defining `$CmdOptionShortName(value, v)` will declare a short name `v` for `value`.

$CmdOptionShortName uses a hyphen `-` to declare the option. For example, the above definition uses `-v` to declare the `value` option, which is equivalent to `--value`.

The first parameter of $CmdOptionShortName must correspond to an option declared by $CmdOption.

$CmdOptionShortName can be omitted. If omitted, the option has no short name.

#### $CmdOptionMemo

This is used to provide a memo description for the option.

It has two parameters: the first is the full name of the option, and the second is the description. Note that the description should be enclosed in double quotes `""`.

#### $CmdOptionNoValue

The $CmdOptionNoValue annotation indicates that the option cannot have subsequent parameters. If there are subsequent parameters, the program will report an error.

$CmdOptionNoValue has one parameter, which is the name of the option.

#### $CmdOptionRequired

The $CmdOptionRequired annotation indicates that the option must be included in the request. If it is not included, the program will report an error.

$CmdOptionRequired has one parameter, which is the name of the option.

#### $CmdOptionPreHandle

$CmdOptionPreHandle is used to define a function that executes before the option is set.

$CmdOptionPreHandle can have two parameters: the first is the corresponding option, which is required, and the second is the function name.

If the second parameter is omitted, the function name defaults to `optionName_PreHandle`. If this function is not defined, the program will report an error.

#### $CmdOptionPostHandle

$CmdOptionPostHandle is used to define a function that executes after the option is set.

$CmdOptionPostHandle can have two parameters: the first is the corresponding option, which is required, and the second is the function name.

If the second parameter is omitted, the function name defaults to `optionName_PostHandle`. If this function is not defined, the program will report an error.

### $CmdArgs Series

$CmdArgs is used to parse and store request parameters. Its usage is similar to $CmdOptionValue.

In ICmd, request parameters are set by those following `--`. Note that there must be a space after `--`. A request can have multiple command-line parameters. A command line can have multiple command-line parameter settings starting with `--`. The order of command-line parameters is their order in the command line.

The definition of $CmdArgs is as follows:

```cpp
#define $CmdArgs(TYPE, NAME) 
```

It has two parameters: the first is the type to which command-line parameters should be parsed, and the second is the name for $CmdArgs.

Available types include:

- QString (string type)
- Numeric types (integer and floating-point data)
- bool type
- QList<XXX> (composite types) and QStringList

The rules for these parameter types are the same as those for $CmdOptionValue. If the user defines $CmdArgs as a non-composite type, only one parameter can be specified.

A program can theoretically define multiple $CmdArgs; they can convert data into different types for processing. However, it is not necessary to use multiple $CmdArgs unless required.

$CmdArgs can have the following additional annotations:

#### $CmdArgsDeclare

This is used to set a default value for the parameter. It should be used with $CmdArgsNullable.

#### $CmdArgsNullable

This indicates that the parameter can be null. If the request parameter is empty, no setting or execution of preHandle and postHandle is performed.

$CmdArgsNullable has one parameter, which is the name of the $CmdArgs parameter.

If a parameter is not defined with $CmdArgsNullable, it cannot be omitted, and an error will be reported if omitted.

#### $CmdArgsMemo

Usage is the same as other Memo annotations.

#### $CmdArgsPreHandle

Usage is the same as other PreHandle annotations.

#### $CmdArgsPostHandle

Usage is the same as other PostHandle annotations.

### $CmdArgX Series

$CmdArgX differs from $CmdArgs; it is used to process parameters one by one.

In practice, there is no $CmdArgX annotation. Instead, X represents numbers from 1 to 9, such as $CmdArg1, $CmdArg2, up to $CmdArg9.

The following explanation uses $CmdArg1 as an example.

The definition of $CmdArg1 is as follows:

```cpp
#define $CmdArg1Declare(TYPE, NAME) \
    PP_CMD_ARG_X_DECLARE(TYPE, NAME, 1)

#define $CmdArg1(TYPE, NAME)    \
    $CmdArg1Declare(TYPE, NAME) \
    TYPE NAME {};
```

It has two parameters: the first is the Type, and the second is the Name.

Note that the type here cannot be a composite type; it must be a simple type, such as QString, int, or bool, because it converts the first parameter to the specified Type.

#### $CmdArgXDeclare

This is used to set a default value for the parameter to be parsed. It must be used together with $CmdArgXNullable; otherwise, it is ineffective.

#### $CmdArgXNullable

This indicates that the parameter can be null.

This macro annotation does not require parameters. The X number already implies the information, indicating which parameter position it refers to. If this annotation is omitted and the parameter at position X is missing, the program will report an error.

#### $CmdArgXPreHandle

This is similar to other preHandle annotations.

Note that only one parameter is required, which is the function name.

#### $CmdArgXPostHandle

This is similar to other postHandle annotations.

Note that only one parameter is required, which is the function name.

#### $CmdArgXMemo

This is used to provide a description for the Xth parameter.

Note that only one parameter is required, which is the description.

### C++26 Attribute Feature

When the overall content of ICmd's functionality is written out, the C++26 feature is customized, and the remaining work involves fixing some bugs. After that, C++26 will be fully released. The main content of C++26 is reflection. One proposal in particular is very interesting.

![image-20250702203824306](assets/image-20250702203824306.png)

The usage of the clap library, as shown above, is as follows:

![image-20250702204130409](assets/image-20250702204130409.png)

The description in this proposal aligns with my thoughts. It turns out that everyone wants to use attributes to handle command-line operations. Therefore, in the future, ICmd will be deprecated or refactored for C++26.