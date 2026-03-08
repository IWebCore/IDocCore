# Packages

## Introduction

In the ICore program, in the code files, you can often see code like the following:

```cpp
$PackageWebCoreBegin

$PackageWebCoreEnd
```

These two lines of code are macros used to define a namespace, and the namespace is IWebCore. You can find its definition as follows:

```cpp
#define $PackageWebCoreBegin  $IPackageBegin(IWebCore)

#define $PackageWebCoreEnd    $IPackageEnd(IWebCore)
```

If the macros are expanded, the code becomes as follows:

```cpp
inline namespace IWebCore {
    
}
```

## IPackageBegin / IPackageEnd

Let's look at the definition of IPackageBegin:

```cpp
#define $IPackageBegin_1(name1) \
inline namespace name1 {

#define $IPackageBegin_2(name1, name2) \
inline namespace name1 {   \
    inline namespace name2 {

#define $IPackageBegin_3(name1, name2, name3) \
inline namespace name1 {   \
    inline namespace name2 {   \
        inline namespace name3

#define $IPackageBegin_4(name1, name2, name3, name4) \
inline namespace name1 {   \
    inline namespace name2 {   \
        inline namespace name3 \
            inline namespace name4


// .... util $IPackageBegin_9

#define $IPackageBegin_(N) $IPackageBegin_##N
#define $IPackageBegin_EVAL(N) $IPackageBegin_(N)
#define $IPackageBegin(...) PP_EXPAND( $IPackageBegin_EVAL(PP_EXPAND( PP_NARG(__VA_ARGS__) ))(__VA_ARGS__) )
```

In the above definition, we define a macro roughly like this:

```cpp
IPackageBegin(arg1, arg2, ...)
```

This macro can pass up to 9 nested namespace names, with each parameter nesting another layer of namespace in the original namespace.

IPackageEnd is similar.

Note that our development environment is based on C++17, which does not support folded namespaces. Under C++20, the above code would be simpler.

### inline namespace

Why is there an "inline" here? It's because I want the contents within this namespace to be transparent for developers to use. Developers do not need to use the namespace IWebCore to reference the object.

Because "inline" is used, if there is another class or object with the same name, it will still cause a conflict. At this point, developers can resolve naming conflicts by adding namespace qualification before the object name.

### Why Use Namespaces

Since the usage is transparent, can we do without the namespace IWebCore? It's not recommended. Because in IWebCore, the library is a source code library containing many classes. If classes have the same name and are not wrapped in a namespace, there will be issues with class compilation conflicts. One solution to this problem is to compile the library into binary and selectively export some names. However, it is still recommended that each library includes its own namespace.

### How to Use IPackage Types in Custom Packages

When users define their own custom packages, they can define their package's namespace by defining their own macros. For example, if a user creates a new package called Abc, they can define the macros as follows:

```cpp
#define $PackageAbcBegin  $IPackageBegin(Abc)

#define $PackageAbcEnd    $IPackageEnd(Abc)
```

Users can then write code like the following at the beginning of each namespace they want to wrap:

```cpp
$PackageAbcBegin

class Abc
{
	// ... 
}

$PackageAbcEnd
```

We recommend users define their package's namespace using the above method for the following reasons:

- Consistency: When all packages are written this way, the IWebCore style is consistent, reducing the cognitive load on users.
- Error Prevention: By using macro definitions, if users make a typo, the compiler will report an error, preventing incorrect code from being written.