# Package Open Issues

This document summarizes some open issues related to the Package system. We need to clarify these issues.

## Naming Issue
1. For package groups, the name remains unchanged. We will append `@version` to the package name to resolve version identification.
2. The names of specific package `.pri` and `.cmake` files remain unchanged and should not include version numbers.
3. This approach will not cause conflicts.
4. For the asio and json libraries, we need to repackage them, including the version number, to avoid the current situation.

## Package Version Issue

1. The `*` in the installed version represents the latest version, but we currently do not have the latest version available, not even on the server. Therefore, we should stick to using specific versions.
2. Future version settings will follow the Node.js approach.

## Auto-generation of `.pri` and `.cmake` Files for Packages

> On the current foundation, we need some scripts to automatically generate `.pri` and `.cmake` files, and later other types of files as well.

1. Location
    1. The configuration for these contents can be placed in the `lib.json` file.
    2. These contents can be parsed in subsequent files.
2. Types
    1. `sources`
        1. This can be a list of files or the name of a folder. We need to distinguish between the two.
        2. If the content is a string, it represents a file; if it's an object, we need to distinguish based on the object's type.
    2. `headers`
        1. Same as above.
    3. `resources`
        1. Same as above.
    4. `includes`
        1. This refers to the relative path from the current top-level directory, to be determined during specific conversion.
    5. `libs`
        1. The specific libraries involved. These can be considered later.
    6. `definition`
        1. Key-value pairs.
        2. If the value is a string, it requires escaping.
        3. If the value is `null`, it is defined directly without a specific value.
        4. Other types include `bool`, `number`, and strings, as well as raw string types.
3. Additional Content
    1. Users can choose whether to generate certain types of files, meaning they can customize which files are generated and not rely on the program to do so automatically.
    2. Users can also choose to add additional content to the generated files.
        1. The content can be defined as a string in the JSON file or in an additional file.

### Auto-generation Content

This will be addressed after the ICmdCore is completed.

## Display of Package Content

In the future search page, some details of the package will be displayed. These contents need to be stored in the `package.json` file, so we need to precisely define the content of `package.json` down to each field.

Additionally, regarding the issue of hardware constraints, we will consider it in the future.