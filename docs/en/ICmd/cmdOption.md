<译文内容>
# Command Line Options

> This document describes command-line options.

In the Windows command line, you can view the `dir` command as follows:

=== "dir"

    ```bash
    C:\Users\Yue>dir /?
    Displays a list of files and subdirectories in the directory.
    
    DIR [drive:][path][filename] [/A[[:]attributes]] [/B] [/C] [/D] [/L] [/N]
    [/O[[:]sortorder]] [/P] [/Q] [/R] [/S] [/T[[:]timefield]] [/W] [/X] [/4]
    
    [drive:][path][filename]
                Specifies the drive, directory, and/or file to list.
    
    /A          Displays files with the specified attributes.
    Attributes   D  Directory                R  Read-only file
                H  Hidden file             A  Archived file (ready for backup)
                S  System file             I  Informational file (no content indexed)
                L  Reparse point           O  Offline file
    /B          Uses an empty format (no header or summary).
    /C          Displays thousand separators in file sizes. This is the default. Use /-C to disable.
    /D          Same as wide format, but files are listed in columns.
    /L          Displays file and directory names in lowercase.
    /N          New long list format, with filenames right-aligned.
    /O          Lists files in sorted order.
    Sort order   N  By name (alphabetical)     S  By size (smallest first)
                E  By extension (alphabetical) D  By date/time (earliest first)
                G  Group directories first     -  Prefix meaning "Reverse" (i.e., reverse order)
    /P          Pauses after each screen of information.
    /Q          Displays the file owner.
    /R          Displays alternate data streams.
    /S          Lists all files in the specified directory and its subdirectories.
    /T          Controls the display or sorting by time.
    Time field   C  Creation time
                A  Last access time
                W  Last write time
    /W          Uses wide list format.
    /X          Displays the short 8dot3 name for files that don't have one. The short name is inserted before the long name in the /N format.
                If no short name exists, blank spaces are displayed.
    /4          Displays the year in four digits.
    ```

There are so many options. In the following, we will explain how to define command-line options in ICmd.

Command-line options in ICore are a type of command-line parameter, starting with `-` or `--`, followed by an option name, and optionally a parameter value.

They provide guidance for command execution, making it more flexible and controllable.

## Example

Here, we define a `dir` command as an example to illustrate how to define command-line options. Note that I will not implement specific functionality here; this is only to explain the tool for defining command-line options.

=== "MyDirCmd.h"

    ```cpp
    #pragma once
    
    #include "cmd/ICmdInterface.h"
    
    class MyDirCmd : public ICmdInterface<MyDirCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        MyDirCmd();
    
        $CmdOptionMemo(recurse, "recurse list subdirectory")
        $CmdOption(recurse)
    
        $CmdOptionMemo(time, "print create time")
        $CmdOption(time)
    
    public:
        $CmdMapping(mydir)
        void mydir();
    };
    
    ```

=== "MyDirCmd.cpp"

    ```cpp
    #include "MyDirCmd.h"
    
    MyDirCmd::MyDirCmd()
    {
    
    }
    
    void MyDirCmd::mydir()
    {
        qDebug() << "recurse:" << recurse;
        qDebug() << "time:" << time;
    }
    
    ```

We directly list their output

=== "-?"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -?
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        testCmd.exe mydir
    [Options]:
        Option     ShortName  Required    NoValue    Memo
        --recurse  -          false       false      recurse list subdirectory
        --time     -          false       false      print create time
    ```

=== "No options"

    ```bash
    
    PS D:\test\cmd> .\testCmd.exe mydir
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: false
    time: false
    ```

=== "--recurse"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir --recurse
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: true
    time: false
    ```

=== "--time"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir --time
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: false
    time: true
    ```

=== "--recurse --time"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir --recurse --time
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: true
    time: true
    ```

=== "--recurse --time --abc"

    ```bash
    
    PS D:\test\cmd> .\testCmd.exe mydir --recurse --time --abc
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    ERROR OCCURED: your input options are not defined in this cmd. [Option]: --abc [Cmd Path]: mydir
    [CMD]:
        testCmd.exe mydir
    [Options]:
        Option     ShortName  Required    NoValue    Memo
        --recurse  -          false       false      recurse list subdirectory
        --time     -          false       false      print create time
    
    ```

Here, note the last request where we input an undefined option. ICmd will display an error message. This means that users can only use options that have been defined.

## $CmdOption

The `$CmdOption` macro is used to define command-line options. This macro annotation has only one parameter, which is the option name. Note that the option name here is the full name, and an abbreviation can be defined separately.

The reason for not defining the option data type is simple: an option has only two states, existence or non-existence, no Schrödinger's cat issue. Therefore, we do not need to define a data type, and the data type is directly a boolean. This parameter defaults to non-existence, with a value of `false`. If the user uses this parameter in the command line, its value will change to `true`.

Options can be followed by option parameters, which will be explained in the next document.

## $CmdOptionShortName

An option's name can be long to fully describe its meaning, so users don't need to guess or rely on the Memo. However, a long option name can make user input difficult. Therefore, we use `$CmdOptionShortName` to define a short name for the option.

The `$CmdOptionShortName` macro has two parameters: the first is the full option name, and the second is the short name for the option.

For example, let's modify the previous example:

=== "MyDirCmd.h"

    ```cpp
    #pragma once
    
    #include "cmd/ICmdInterface.h"
    
    class MyDirCmd : public ICmdInterface<MyDirCmd>
    {
        Q_GADGET
        $AsCmd(/)
    public:
        MyDirCmd();
    
        $CmdOptionShortName(recurse, r)
        $CmdOptionMemo(recurse, "recurse list subdirectory")
        $CmdOption(recurse)
    
        $CmdOptionShortName(time, t)
        $CmdOptionMemo(time, "print create time")
        $CmdOption(time)
    
    public:
        $CmdMapping(mydir)
        void mydir();
    };
    
    ```

=== "MyDirCmd.cpp"

    ```cpp
    #include "MyDirCmd.h"
    
    MyDirCmd::MyDirCmd()
    {
    
    }
    
    void MyDirCmd::mydir()
    {
        qDebug() << "recurse:" << recurse;
        qDebug() << "time:" << time;
    }
    
    ```

In the above example, we defined abbreviations `r` and `t` for the `recurse` and `time` options, respectively.

Now, users can input the options using the short names.

=== "-r"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -r
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: true
    time: false
    ```

=== "-t"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -t
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: false
    time: true
    ```

=== "-r -t"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -r -t
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    recurse: true
    time: true
    ```

The help information also changes at this point.

=== "Changed help"

    ```bash
    PS D:\test\cmd> .\testCmd.exe mydir -?
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        testCmd.exe mydir
    [Options]:
        Option     ShortName  Required    NoValue    Memo
        --recurse  -r         false       false      recurse list subdirectory
        --time     -t         false       false      print create time
    
    ```

=== "Help before change"

    ```bash
    
    PS D:\test\cmd> .\testCmd.exe mydir -?
    
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    [CMD]:
        testCmd.exe mydir
    [Options]:
        Option     ShortName  Required    NoValue    Memo
        --recurse  -          false       false      recurse list subdirectory
        --time     -          false       false      print create time
    ```

Comparing the two, the ShortName field is now filled.

## $CmdOptionMemo

The `$CmdOptionMemo` macro is used to define the description of an option. This macro annotation has two parameters: the first is the option name, and the second is the option's description. The option's description must be enclosed in double quotes.

## $CmdOptionRequired

The `$CmdOptionRequired` macro has one parameter, which is the option name.

It is used to define an option as a required parameter. If the user does not input this option, the command line will display an error.

This option is usually followed by corresponding parameters. If an option is required and no parameter is provided, the value is fixed, so why define the parameter? For example, if we are doing authentication work, options like `--name` and `--password` must be required to ensure the user provides a username and password.

For option parameters, refer to the next document.

## $CmdOptionNoValue

This annotation has one parameter, which is the option name.

The purpose of this annotation is to inform ICmd that this option does not take any parameters. If parameters are provided, the program should display an error message to the user.

For example, in the `mydir` command, we define an option `--recurse` that should not take any parameters. If the user inputs a parameter after `--recurse`, the program should display an error message.