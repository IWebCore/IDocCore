# IMakeCore Discussion

## A New Package Management System

In the realm of emerging programming languages, **package management** services have become commonplace. Java has Maven, Node.js has npm, Python uses pip install to install third-party libraries, Go has its own package management, Rust has Cargo, and so on.

Among C++ build tools, CMake stands out as a de facto standard. QMake holds significant importance in the GUI domain, though it remains confined to GUI programming. XMake, developed by a Chinese programmer, has garnered positive feedback and is gaining wider acceptance. Other tools include Bazel and Meson.

C++ is an ancient yet vibrant language. Due to its early origins and the characteristic of ABI incompatibility among compilers, it has lagged behind other languages in package management. Various solutions have emerged, such as vcpkg, conda, and XMake. These solutions have their strengths and are developing rapidly. Among them, vcpkg is widely used in software development.

The working principles of these C++ package management tools vary. Some package binary code for direct user use, others download source code, compile it into binary library files, and integrate it into the subsequent build process. Some even package libraries as header-only types, compiling them inline into the program.

To address the above issues, I developed a new library management system that seamlessly integrates with the qmake and CMake build systems. Unlike previous library management systems, which relied on precompiled binaries, this system distributes source code directly, eliminating the need for prior compilation.

This approach offers multiple advantages. Regardless of whether users are managing code with qmake or CMake, the library management system can be seamlessly integrated. Future plans include supporting more build systems, such as XMake. Users simply need to add a few lines of code in the build file to utilize this package management system. By adding a package's information in the configuration file, the system automatically incorporates it into the user's build.

## IMakeCore

While developing IWebCore, as requirements grew and modules expanded, external dependencies also increased. Packaging IWebCore became a challenge. Due to its reliance on static initialization objects, IWebCore cannot use header-only libraries or dynamically or statically linked libraries. Source code distribution became the only viable option.

However, distributing all packages via source code was inefficient. For instance, if I provided separate packages for HTTP, command-line, WebSocket services, etc., this approach was clearly impractical and made dependency management difficult.

After examining CMake's and XMake's package distribution methods, I found no solution to my specific problem. I then decided to create a simple, yet effective, source-based package management system. This led to the development of IMakeCore, a package management system.

Gradually, IMakeCore evolved beyond simple package integration. I also developed IPubCore and IPubCmd to support the package management system.

IPubCore functions similarly to npm or Maven's repository, offering package upload and search capabilities. Users can find available packages, learn how to use them, and integrate them into IMakeCore projects.

IPubCmd provides a command-line tool for users to manage their packages, including installation, uninstallation, updates, and listing their packages. Users can manage their packages with simple `ipc` commands.

## Summary

IMakeCore aims to complement, not replace, CMake or qmake. It offers a simpler and more convenient package management system, providing users with an additional option. It is a package management system designed to integrate into CMake and qmake build systems.

IMakeCore is not intended to solve all C++ package management issues. Its primary goal is to address the packaging needs of IWebCore. During IWebCore's development, users seeking packages for cache-based session management, HTTP compression, ranges, cross-region functionality, or other features can find them on IPubCore and integrate them into their projects using IMakeCore.

Additionally, IMakeCore supports lightweight, cross-platform libraries. These libraries are generally uncomplicated to package, have minimal dependencies, and straightforward build requirements. Their small codebase ensures they do not significantly impact build times when compiled alongside the main project.

Another advantage is that compiling source code directly allows compilers more flexibility for optimization, reducing reliance on precompiled binaries and enabling cross-platform compatibility. However, IMakeCore cannot directly handle large libraries like OpenCV, VTK, or OpenSSL. Users must still use CMake's `find_package` or qmake's `.pri` files for these dependencies.

## Conclusion

During my job interviews, some interviewers posed insightful questions that I’d like to share here.

### Why is a new package management system necessary?

- IMakeCore is not a comprehensive tool like CMake or qmake, which manage entire projects and builds. Instead, it is a package management tool that integrates seamlessly with CMake and qmake, and can support other build systems like XMake in the future. This enables `cross-project package management` by integrating IMakeCore into any qmake or CMake project to include relevant packages.

- IMakeCore is a source-based package management system. Most C++ package management tools today compile code into binaries before integration. IMakeCore, however, manages source code directly, compiling packages alongside the project. This eliminates the need for precompilation, supports cross-platform builds, and aligns with the practices of languages like Go, Rust, and Python. While source-based distribution increases build times during full recompilation, it ensures better cross-platform compatibility. This approach achieves `cross-project and cross-platform package management`.

Combining these two factors, IMakeCore is a package management system designed for cross-project and cross-platform use.

### How are package dependencies resolved?

- Due to the long-standing absence of a robust package management system in C++, each package or library tends to be relatively independent. Unlike Node.js libraries, C++ packages rarely depend on other external libraries. Most packages primarily rely on the standard library, avoiding complex dependencies. This is a notable characteristic of C++ packages.

- Users can specify dependencies in a package's definition using the `dependencies` field. IMakeCore will automatically detect if these dependencies exist and report errors if they don't.

- For special dependencies, users can manually package and manage them. We encourage users to upload these to IPubCore for community sharing.

### How are package conflicts resolved?

This is indeed a challenging issue. Package conflicts can be categorized into two types.

- The first type occurs when two packages contain identical content, leading to conflicts. This could mean their header file paths overlap, making it unclear which to reference. Or, they define the same data or functions, causing build errors during linking.

  - Such conflicts might also involve macros.

  - For existing packages, users must resolve conflicts by compiling them into dynamic or static libraries and selectively exporting headers.

  - For newly created packages, we strongly recommend using namespaces to avoid conflicts. Java’s practice of using package names as namespaces is an excellent example.

- The second type involves header file conflicts, where definitions in different packages overlap.

  - For existing packages, users must handle conflicts by repackaging into libraries, modifying source code, or replacing the library. Alternatives include refactoring into a single `.h` or `.cpp` file.

  - For new packages, we recommend using a namespace as a nested folder structure to limit header file exposure.

In summary, for future packages, we can implement stricter naming conventions to prevent conflicts. For existing packages, users must take proactive steps to mitigate these issues.

Everything is that straightforward!