# Table Model

## 创建一个实例

IRdbTableModelInterface 的接口如下。

```c++
template<typename T, typename Table, typename Db, bool enabled = true>
class IRdbTableModelInterface
    : public IRdbEntityModelWare<Table, Db>, public ITaskWareUnit<T, IRdbCatagory, enabled>, public ISingletonUnit<T>
{
public:
    IRdbTableModelInterface();

public:
    bool insertOne(Table& table);
    bool insertOne(const Table& table);
    bool insertAll(const QList<Table>& tables);

public:
    bool existById(const QVariant& id);

public:
    IResult<Table> findById(const QVariant& id);
    QList<Table> findAllByIds(const QVariantList& list);

public:
    void updateOne(const Table& table);
    void updateOne(const Table& table, const QStringList& columns);
    void updateAll(const QList<Table>& tables);
    void updateAll(const QList<Table>& tables, const QStringList& columns);
    void updateWhere(const QVariantMap& map, const IRdbCondition& condition);
    void updateById(const QVariant& id, const QVariantMap& map);

public:
    bool deleteOne(const Table&);
    bool deleteAll();
    bool deleteAll(const QList<Table>& tables);
    bool deleteAll(const IRdbCondition& condition);
    bool deleteById(const QVariant& id);
    bool deleteAllByIds(const QVariantList& ids);

public:
    virtual QString createTableSql() const;

public:
    bool truncateTable();

private:
    bool containsTable(const QString& tableName);

    virtual void $task() final;
};
```



他的基类如下：

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
};
```

我们一点一点分解代码

## 我们创建一个model 对象

### 创建`model`

```c++
#pragma once

#include "rdb/model/IRdbTableModelInterface.h"
#include "Student.h"
#include "SqliteDb.h"

class StudentModel : public IRdbTableModelInterface<StudentModel, Student, SqliteDb>
{
public:
    StudentModel() = default;
};
```

我们创建StudentModel对象，对象通过`***\*CRTP\****`继承 `***\*IRdbTableModelInterface\****`。此外，我们还有额外的参数，第二个参数是要映射的对象 Table,第三个参数是需要连接的数据库 DB, 第四个参数是是否启用当前Model。Student将与DB数据库中的相关表连接起来。

### 数据库表生成

在程序开始运行的时候,会运行`$task`功能，内容如下：

- Model会首先判断当前的表是否存在，如果不存在，则会做一下的事情。
- 如果***\*model\**** 重载了`QString createTableSql() const` 这个函数，则会优先使用这个函数生成创建语句。
- 如果不存在，则会根据当前的Table注解生成一条创建数据库表语句。生成规则参考`***\*Table\****` 信息。
- 运行这条语句创建Table对应的表，生成数据库表。

## 基本操作

model 中提供了一些默认操作



### 插入数据

我们提供了以下的数据插入操作

- `bool insertOne(Table& table);`

`Table`是我们定义的实体。这条语句是插入数据库，并且插入时，会将主键值赋值到我们实体的标记的主键字段上面。

- `bool insertOne(const Table& table);`

这个是和上面一致做插入功能，但是不会将主键值赋值到实体字段。

- `bool insertAll(const QList<Table>& tables);`

这是批量插入操作。如果用户有大量数据，优先使用这个函数。



### 数据统计

- `std::size_t count()`

这个统计出当前表有多少跳数据。他统计出当前表共有多少条数据。

- `std::size_t count(const IRdbCondition&)`

这个是条件统计，统计在 `IRdbCondition`条件下一共有多少跳数据。

- `bool exist(const IRdbCondition& condition)`

查询在当前 condition 条件下是否能够查询到数据。

-  `bool existById(const QVariant& id)`

查找当前表是否存在主键值值为 `id` 的数据，如果存在，返回 `true`，否则，返回`false`



### 数据查找

查找操作如下：

- `IResult<Entity> findOne(const IRdbCondition&)`

这个是根据 `IRdbCondition`查找一条数据，如果找到多条数据，返回 std::nullopt, 没有找到数据，也返回 std::nullopt。

注意这里 `IResult` 是 `std::optional` 的别名。

- `QList<Entity> findAll()`

这个是查找表中的所有数据， 返回所有数据。

- `QList<Entity> findAll(const IRdbCondition&)`

这个是条件查找，根据 `IRdbCondition` 查找相关的数据。

- `QVariantList ``***\*findColumn\****``(``**const**`` QString& ``column)`

查找一列数据，返回 QList<QVariant>

- `QVariantList ``***\*findColumn\****``(``**const**`` QString& ``column,`` ``**const**`` IRdbCondition& ``condition)`

根据condition查找一列数据，返回`QVariantList`

- `QList<QVariantMap> findColumns(const QStringList& columns)`

这个是查找指定的列。传入内容为列名，传出的数据为 QMap<QString, QVariant> 的列表。QMap<QString, QVariant>中，键为名称，值为具体的数据。

- `QList<QVariantMap> findColumns(const QStringList& columns, const IRdbCondition& condition)`

同上，查找指定列，带上条件查询。

- `IResult<Table> findById(const QVariant& id)`

根据表的主键进行查询，如果值数量为0或者数量超过1个，返回 `std::nullopt`,意思是没有数据返回。如果数量是一个，则返回查询到的数据。 

- `QList<Table> findAllByIds(const QVariantList& list)`

查询一系列的数据，传入QList<QVariant>数据，传出Table列表。





### 删除数据

- `bool deleteOne(const Table&)`

删除一条数据。删除逻辑是根据 Table的

- `bool deleteAll()`

删除所有记录

- `bool deleteAll(const QList<Table>& tables)`

删除所有在`tables` 中的记录，根据Table的主键进行删除。

- `bool deleteAll(const IRdbCondition& condition)`

根据 conditon 进行删除数据。

- `bool deleteById(const QVariant& id)`

根据id进行数据删除

- `bool deleteAllByIds(const QVariantList& ids)`

根据 ids 中所列举的 主键进行删除数据。



### 更新数据

- `void updateOne(const Table& table)`

更新一条数据

- `void updateOne(const Table& table, const QStringList& columns)`

更新一条数据，只更新 columns 列的内容

- `void updateAll(const QList<Table>& tables)`

更新指定的数据集合。

- `void updateAll(const QList<Table>& tables, const QStringList& columns)`

更新指定的数据集合，更新固定的 列 `columns`

- `void updateWhere(const QVariantMap& map, const IRdbCondition& condition)`

根据 condition更新表。更新的内容为 `map`

- `void updateById(const QVariant& id, const QVariantMap& map)`

根据 id 更新吧数据集。



## 自定义操作

当默认提供的查询无法解决需要的时候，用户可以自定义SQL语句进行查询。

### 通过已有的算法进行组合

```c++
#pragma once

#include "rdb/model/IRdbTableModelInterface.h"
#include "Student.h"
#include "SqliteDb.h"

class StudentModel : public IRdbTableModelInterface<StudentModel, Student, SqliteDb>
{
public:
    StudentModel() = default;

public:
    QStringList getTopTenStudents() {
        auto value = findColumn("name", IRdbCondition().orderBy("score").limit(10));
        QStringList names;
        for(const auto& val : values){
            names.append(value.toString());    
        }
        return names;
    }
};
```

如上述13-20行所示，创建一个获取前十名的学生的功能。

### 直接写原生SQL

用户可以直接写SQL 语句来进行查询

```c++
QStrinList getTopTenStudents(){
    QString sql = "select name from student order by score limit 10";
    auto query = createQuery(sql);
    query.exec();

    auto value = IRdbUtil::getVariantList(query);
    QStringList names;
    for(const auto& val : values){
        names.append(value.toString());    
    }
    return names;
}
```

注意上方的 `createQuery` 的用法,这里要求用户必须使用 createQuery来创建查询。`createQuery`会负责创建一个新的 `ISqlQuery` 对象来进行查询。ISqlQuery 将会根据数据库不同类型选择是否开启一个新的数据库连接，从而保证数据查询不冲突。

### ISqlQuery

上述的createQuery函数返回的是 `ISqlQuery`对象。ISqlQuery 继承于 QSqlQuery。他的视线方式如下：

```c++
class ISqlQuery : public QSqlQuery
{
public:
    explicit ISqlQuery(QSqlDatabase db, const IRdbDialect&);

public:
    ISqlQuery& operator=(const ISqlQuery& other);
    void bindValue(const QString& placeholder, const QVariant& val, QSql::ParamType type = QSql::In) = delete;
    void bindValue(int pos, const QVariant& val, QSql::ParamType type = QSql::In) = delete;
    void addBindValue(const QVariant& val, QSql::ParamType type = QSql::In) = delete;

public:
    bool exec(const QString& sql);
    bool exec();

    void bindParameter(const QString& key, const QVariant& value);
    void bindParameters(const QVariantMap& map);
}
```

在上面我们看见ISqlQuery 禁止了原生的bindValue 方法，取而代之的是 `bindParameter` 方法。所以用户想要绑定数据的话，需要使用 `bindParameter` 和 `bindParameters`这两个方法。