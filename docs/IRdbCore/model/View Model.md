# View Model

## 创建一个ViewModel

我们看一看如何创建一个 ViewModel。代码如下：



```c++
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

代码一如既往的简洁明了。在 `.h` 文件中继承 `IRdbViewModelInterface` 建立一个对象,并在 `.cpp` 文件中包含该头文件，以保证该对象会被编译器识别并编译。



## IRdbViewModelInterface

他的实现如下：

```c++
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

 该基类是一个 CRTP 基类。第一个参数是 Model 子类的名称，第二个参数是要对应上的View的类型，第三个参数是 `Database`数据库的类型， 第四个参数表示是否初始化和使用`$task` 功能。

 他的继承类有一下两个，`IRdbEntityModelWare` 和 `ITaskWareUnit`两个。

### IRdbEnityModelWare

这个类我们在 TableModel中同样使用过，他提供了一些基本的查询功能。他的内容如下：

```c++
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

可以看到，他实现了 `count()`统计功能， 各种`find` 查找功能，以及 `exist()` 判断存在与否的功能。具体的功能点这里不详细说明。

### Task

除了查询功能之外，`IRdbViewModelInterface` 中最重要的一个功能是View表创建功能，这个在Task中实现。`ITaskWareUnit` 会将当前类实现的`$task()`注册到 `ITaskManage`, `ITaskManage`会按照一定的规则执行这些 `$task()`。在我们的重载的 `$task()` 中，会进行以下操作：

- 判断 view 是否存在， 不存在则会设法创建该 `View`
- 他首先会调用 `IRdbViewModelInterface::createViewSql()`方法返回一条语句，如果语句不为空，则执行该语句。
- 如果上述语句为空，则会尝试从 `View`中查看是否提供了 sql。View中提供Sql 是通过 `$CreateViewSql` 这个宏注解进行的。如果存在该 Sql，则会执行该Sql创建View。
- 如果View还不纯在，报错，提示用户提供一条语句，或则手动在数据库中创建该`View`



## 举例说明

这里举例说明其具体用法。

```c++
//TODO:
```