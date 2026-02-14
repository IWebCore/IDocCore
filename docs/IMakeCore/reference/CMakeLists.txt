cmake_minimum_required(VERSION 3.16)

project(dynamicMapping_demo LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core)

add_executable(dynamicMapping_demo
  main.cpp
  IndexController.h IndexController.cpp
)
target_compile_definitions(dynamicMapping_demo PRIVATE _WIN32_WINNT=0x0601)
target_link_libraries(dynamicMapping_demo Qt${QT_VERSION_MAJOR}::Core)
target_link_libraries(dynamicMapping_demo ws2_32 mswsock)

include($ENV{ICMakeCore})
ICMakeCoreInit(dynamicMapping_demo)
