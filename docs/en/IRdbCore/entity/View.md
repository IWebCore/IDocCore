*: The query performance of views may be poor, especially if the view queries involve complex joins or aggregate operations. In such cases, ensure the database performance is sufficient to avoid performance issues caused by frequent view queries. Users need to consider these scenarios and use tools like `index` to improve performance.

## Definition of a View

### IRdbViewInterface

Similar to `IRdbTableInterface`, we abstract out `IRdbViewInterface` for defining views. The implementation code for `IRdbViewInterface` is as follows:

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

It is a `CRTP` base class. The first template parameter `T` is the class name. The second parameter `enabled` is related to type registration and defaults to `true`. Users inherit from this class to implement their own view types. Let's define a simple view:

```c++
#include "rdb/entity/IRdbViewInterface.h"

class PersonView : public IRdbViewInterface<PersonView>
{
    Q_GADGET
}
```

This completes the implementation of our simplest view, but it has no fields. Below, we will explain how to add fields.

### Macros

Similar to Tables, adding fields requires using macro annotations. The macros for Views are defined in `IRdbViewPreprocessor.h`. Its source code is simple, as shown below:

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

Here, we alias `$Column` to `$ViewField`. Users can use either macro to define fields. Let's define our fields:

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

`$ViewFieldDeclare` is an alias for `$ColumnDeclare`. For its usage, refer to the Table section. We continue to define our fields:

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

The reason for mixing different styles here is to demonstrate usage. In actual development, it is recommended to use only one method.

#### $AsView

The `$AsView` macro is used to give the current view an alias. If this macro is not used, the default view name is the class name. For example:

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

In line 6, we added the macro. Therefore, the current view maps to the database's `person_view` view, not the `PersonView` view. If this line is commented out, it maps to the `PersonView` view.

#### $CreateViewSql

This macro is used to provide the SQL statement for creating the view. The statement should be enclosed in double quotes when used. For example:

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

This completes the definition of a view.

For more details on creating views, refer to the relevant content of `IRdbViewModelInterface`.