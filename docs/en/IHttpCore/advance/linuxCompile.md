# Compilation under Linux

> This document describes the compilation of the IHttp project under Linux and the issues encountered.

> TODO: I'm not very familiar with this either, but I have compiled it and run it online. Users are resourceful and stronger than me, so it should be fine.

I encountered an issue where if users have installed the offline Qt 5.14.2, the compilation does not work if done via the command line; it must be compiled from the command line. This is a problem of Qt version conflict. I did not delve deeply into it. If someone encounters this issue, they can write a detailed document describing it.

Here is my compilation method:

```
sudo apt install qtbase5-dev
qmake
make -j20
```

Note the issue with Qt versions.