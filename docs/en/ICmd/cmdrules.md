# Command Line Rules

For ICmd, we have standardized the command line rules. As follows:

## Command Line Path

The command line path is the path that matches exactly one `CmdAction`.

Here, the command line path starts from the second string and continues until a non-`-` string. The `-` is used to define parameters and options, etc.

If the command line path is empty, it will output all the registered command line paths in the system.

---

## Command Line Parameters

Command line parameters start with the `--` double-hyphen string, and the subsequent strings are their parameters until another `-` appears.

Note: There must be a space between `--` and the parameter.

A command can have multiple parameters, and parameters can be defined by multiple `--`.

---

## Command Line Options

Command line options are strings starting with `--` or `-`. The part after the hyphen must be a specific string without any space; otherwise, it is considered as part of the command definition.

Options starting with `--` are full-named command line options, while those starting with `-` are abbreviated options.

Command line options can be followed by command line parameters.

---

## Help `-?`

The purpose of `-?` is to output the help documentation. This can be appended after a specific command line path to display the corresponding information for that path.