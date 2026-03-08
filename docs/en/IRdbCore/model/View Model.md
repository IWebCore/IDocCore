# View Model

## Creating a ViewModel

Let's look at how to create a ViewModel. The code is as follows:

```cpp
// PersonModel.h
#pragma once

#include "rdb/model/IRdbViewModelInterface.h"
#include "PersonView.h"
#include "SqliteDb.h"

class PersonModel : public IRdbViewModelInterface<PersonModel, PersonView, SqliteDb>
{
public:
    StudentModel() = default;
};
// PersonModel.cpp
#include "PersonModel.h"
```

The code is as concise and clear as ever. In the `.h` file, inherit from `IRdbViewModelInterface` to create an object, and include the header file in the `.cpp` file to ensure the object is recognized and compiled by the compiler.

## IRdbViewModelInterface

Its implementation is as follows:

```cpp
template<typename T, typename View, typename Db, bool enabled = true>
class IRdbViewModelInterface
    : public IRdbEntityModelWare<View, Db>, public ITaskWareUnit<T, IRdbCatagory, enabled>
{
public:
    IRdbViewModelInterface();

public:
    virtual QString createViewSql() const;

protected:
    virtual double $order() const override;
    virtual void $task() final;

protected:
    const IRdbViewInfo& m_viewInfo;
};
```

This base class is a CRTP base class. The first parameter is the name of the Model subclass, the second parameter is the type of the corresponding View, the third parameter is the `Database` type, and the fourth parameter indicates whether to initialize and use the `$task` functionality.

Its inheritance classes are the following two: `IRdbEntityModelWare` and `ITaskWareUnit`.

### IRdbEntityModelWare

This class was also used in the TableModel. It provides some basic query functions. Its content is as follows:

```cpp
template<typename Entity, typename Db>
class IRdbEntityModelWare
{
public:
    IRdbEntityModelWare();

public:
    std::size_t count();
    std::size_t count(const IRdbCondition&);

public:
    IResult<Entity> findOne(const IRdbCondition&);
    QList<Entity> findAll();
    QList<Entity> findAll(const IRdbCondition&);
    QVariantList findColumn(const QString& column);
    QVariantList findColumn(const QString& column, const IRdbCondition& condition);
    QList<QVariantMap> findColumns(const QStringList& columns);
    QList<QVariantMap> findColumns(const QStringList& columns, const IRdbCondition& condition);

public:
    bool exist(const IRdbCondition& condition);

public:
    ISqlQuery createQuery();
    ISqlQuery createQuery(const QString& sql);
    ISqlQuery createQuery(const QString& sql, const QVariantMap& values);

protected:
    IRdbDatabaseWare& m_database;
    const IRdbEntityInfo& m_entityInfo;
    const IRdbDialectWare& m_dialect;
};
```

As can be seen, it implements the `count()` for statistics, various `find` query functions, and the `exist()` function for checking existence. Specific functional details are not elaborated upon here.

### Task

In addition to query functionality, the most important feature of `IRdbViewModelInterface` is the View table creation functionality, which is implemented in the Task. `ITaskWareUnit` registers the `$task()` implemented by the current class to `ITaskManage`, and `ITaskManage` executes these `$task()`s according to certain rules. In our overridden `$task()`, the following operations are performed:

- Check if the view exists; if not, attempt to create the `View`.
- It first calls the `IRdbViewModelInterface::createViewSql()` method to return a statement; if the statement is not empty, it executes it.
- If the above statement is empty, it tries to check if the `View` provides SQL. The View provides SQL through the `$CreateViewSql` macro annotation. If the SQL exists, it executes it to create the View.
- If the View still does not exist, it reports an error, prompting the user to provide a statement or manually create the `View` in the database.

## Example

Here is an example illustrating its specific usage.

```cpp
//TODO: