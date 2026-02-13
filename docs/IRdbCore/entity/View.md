# View 实体

## 概述

在数据库中，数据库表类型有 Table 和 View 两种。Table是一个实实在在的数据库实体，而View则是在Table和View的基础上通过查询语句建立起来的虚拟表，目的是为了方便查询使用。而在实际的项目过程中，我们不仅需要查询数据库Table,更多的是进行表的部分查询和表的连查询。所以我们在除了Table以外，还支持View进行查询和对象模型映射，满足更广泛的需求。

### View的特点

1. ***\*视图通常是只读的\****：大多数视图在数据库中是只读的，因为它们通常是查询的结果集而不是实际的数据存储。因此，在对视图进行映射时，确保它的用途是读取数据。虽然特定情况下View也可以进行写入和删除，但是我们不考虑这些情况，在我们实现的对View的操作只包括查询操作。
2. ***\*视图和实体的映射\****：视图中的列与实体类的属性一一映射。确保在实体类中定义了视图中所有必要的列，并且在创建视图的时候，注意视图列的名称要与实体列的名称进行一一对应。
3. ***\*视图的主键\****：视图没有主键，因为它是由多个表的连接或查询结果组成的。我们在实现视图类的过程中禁止出现主键，出现了也会被自动忽略。
4. ***\*性能考虑\****：视图的查询性能可能较差，特别是如果视图我们中的查询涉及复杂的联接或聚合操作。在这种情况下，确保数据库性能足够好，避免由于频繁查询视图导致的性能问题。用户需要考虑到这些情形，使用`index` 等一系列的工具来提高性能。



## View 的定义

### IRdbViewInterface

同 `IRdbTableInterface` 一样，我们抽象出 `IRdbViewInterface`来进行视图的定义。IRdbViewInterface 的实现代码如下：

```c++
template<typename T, bool enabled = true>
class IRdbViewInterface : public IBeanInterface<T, enabled>
{
public:
    IRdbViewInterface() = default;

public:
    static const IRdbViewInfo& staticEntityInfo();
};

template<typename T, bool enabled>
const IRdbViewInfo &IRdbViewInterface<T, enabled>::staticEntityInfo()
{
    static IRdbViewInfo s_info(T::staticMetaObject);
    return s_info;
}
```

他是一个`CRTP` 基类。模板类的第一个参数`T`是类类型名称。第二个参数 `enabled`和类型注册相关,默认为`true`。用户继承这个类来实现自己的View类型。我们先定义一个最简单的View：

```c++
#include "rdb/entity/IRdbViewInterface.h"

class PersonView : public IRdbViewInterface<PersonView>
{
    Q_GADGET
}
```

这样，我们的最简单的View就实现了，但他一个字段也没有。下面我们讲述如何添加字段。



### 宏注解

和Table一致，添加字段需要使用的宏注解。View的宏注解定义在 `IRdbViewPreprocessor.h` 中。他的源码很简单，如下:

```c++
#pragma once

#include "rdb/pp/IRdbPreProcessor.h"

#define $AsView(viewName)   \
    Q_CLASSINFO("sql_entityName", #viewName)

#define $CreateViewSql( sql )       \
    Q_CLASSINFO("sql_createViewSql", sql)

#define $ViewField $Column
#define $ViewFieldDeclare $ColumnDeclare
```



#### $ViewField / $Column

我们在这里给 `$Column` 起了一个别名，`$ViewField`。用户可以使用两个中间的任意一个进行定义字段。 那我们定义一下我们的字段。

```c++
#include "rdb/entity/IRdbViewInterface.h"

class PersonView : public IRdbViewInterface<PersonView>
{
    Q_GADGET
public:
    $Column(qlonglong, id)

    $ViewField(QString, name)
}
```



#### $ViewFieldDeclare / $ColumnDeclare

$ViewFieldDeclare 是 $ColumnDeclare 的别名。他的具体用法参考 Table 中的用法，我们继续定义自己的字段：

```c++
#include "rdb/entity/IRdbViewInterface.h"

class PersonView : public IRdbViewInterface<PersonView>
{
    Q_GADGET
public:
    $Column(qlonglong, id)

    $ViewField(QString, name)

    $ColumnDeclare(bool, isMale)
    bool isMale{true};

    $ViewFieldDeclare(QDate, birthDate)
    QDate birthDate;
}
```

我这里混用各种写法的目的是为了展示使用方法，在实际的开发过程中，建议只使用一种方式。



#### $AsView

$AsView 字段是用于给当前的View起一个别名。如果没有这个宏注解，View的名称默认是类的名称。如下：

```c++
#include "rdb/entity/IRdbViewInterface.h"

class PersonView : public IRdbViewInterface<PersonView>
{
    Q_GADGET
    $AsView(person_view)
public:
    $Column(qlonglong, id)

    $ViewField(QString, name)

    $ColumnDeclare(bool, isMale)
    bool isMale{true};

    $ViewFieldDeclare(QDate, birthDate)
    QDate birthDate;
}
```

第6行中，我们添加了该宏注解。所以当前View映射的是数据库的 `person_view` 视图，而不是 `PersonView` 视图。如果注释掉改行，则是映射到的是 `PersonView`视图。



#### $CreateViewSql

这个是创建View 的语句。在使用的时候需要将语句使用双引号括起来。

如下：

```c++
#include "rdb/entity/IRdbViewInterface.h"

class PersonView : public IRdbViewInterface<PersonView>
{
    Q_GADGET
    $AsView(person_view)
    $CreateViewSql("create view person_view as select id, name, is_male as isMale, birthDate from StudentTable")
public:
    $Column(qlonglong, id)

    $ViewField(QString, name)

    $ColumnDeclare(bool, isMale)
    bool isMale{true};

    $ViewFieldDeclare(QDate, birthDate)
    QDate birthDate;
}
```

以上就是如何定义一个View。

关于创建的具体内容可以查看 `IRdbViewModelInterface` 的相关内容。