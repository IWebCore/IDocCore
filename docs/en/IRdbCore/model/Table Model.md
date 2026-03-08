# Table Model

## Creating an Instance

The interface of `IRdbTableModelInterface` is as follows.

```cpp
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

The base classes are as follows:

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
};
```

We break down the code step by step.

## We Create a Model Object

### Creating the `model`

```cpp
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

We create a `StudentModel` object, which inherits from `IRdbTableModelInterface` using the **CRTP** pattern. Additionally, we have extra parameters: the second parameter is the Table to be mapped, the third is the database to connect to, and the fourth is whether the model is enabled. The `Student` class will connect to the corresponding table in the DB database.

### Database Table Generation

When the program starts, the `$task` function is executed, which does the following:

- The model first checks if the table exists. If it doesn't, the following actions are taken.
- If the `model` overrides the `QString createTableSql() const` function, this function is used to generate the create statement.
- If the table does not exist, a create statement for the database table is generated based on the `Table` annotations. The generation rules are referenced from the `Table` information.
- The SQL statement is executed to create the table corresponding to the Table, generating the database table.

## Basic Operations

The model provides several default operations.

### Inserting Data

We provide the following data insertion operations:

- `bool insertOne(Table& table);`

The `Table` is the entity we define. This statement inserts data into the database and assigns the primary key value to the entity's marked primary key field.

- `bool insertOne(const Table& table);`

This performs the same insertion function as the previous one, but does not assign the primary key value to the entity's field.

- `bool insertAll(const QList<Table>& tables);`

This is a batch insertion operation. Use this function for large datasets.

### Data Statistics

- `std::size_t count()`

This counts the number of data entries in the current table.

- `std::size_t count(const IRdbCondition&)`

This performs a conditional count, returning the number of data entries that meet the `IRdbCondition`.

- `bool exist(const IRdbCondition& condition)`

Checks if data exists under the current `condition`.

- `bool existById(const QVariant& id)`

Checks if a data entry with the primary key value `id` exists in the table. Returns `true` if it exists, otherwise `false`.

### Data Retrieval

The data retrieval operations are as follows:

- `IResult<Entity> findOne(const IRdbCondition&)`

This retrieves one data entry based on the `IRdbCondition`. If multiple entries are found, it returns `std::nullopt`. If no data is found, it also returns `std::nullopt`.

Note that `IResult` is an alias for `std::optional`.

- `QList<Entity> findAll()`

This retrieves all data from the table.

- `QList<Entity> findAll(const IRdbCondition&)`

This performs a conditional retrieval, fetching data based on the `IRdbCondition`.

- `QVariantList findColumn(const QString& column)`

This retrieves a single column of data, returning a `QVariantList`.

- `QVariantList findColumn(const QString& column, const IRdbCondition& condition)`

This retrieves a single column of data based on the `condition`, returning a `QVariantList`.

- `QList<QVariantMap> findColumns(const QStringList& columns)`

This retrieves specified columns. The input is the column names, and the output is a list of `QVariantMap`. In each `QVariantMap`, the key is the column name, and the value is the data.

- `QList<QVariantMap> findColumns(const QStringList& columns, const IRdbCondition& condition)`

This retrieves specified columns with a conditional query.

- `IResult<Table> findById(const QVariant& id)`

This queries data by the table's primary key. If the result has zero or more than one entry, it returns `std::nullopt`, indicating no data was found. If exactly one entry is found, it returns the queried data.

- `QList<Table> findAllByIds(const QVariantList& list)`

This queries a series of data entries, taking a `QVariantList` as input and returning a `Table` list.

### Deleting Data

- `bool deleteOne(const Table&)`

Deletes a single data entry. The deletion logic is based on the `Table`.

- `bool deleteAll()`

Deletes all records.

- `bool deleteAll(const QList<Table>& tables)`

Deletes all records in the `tables` list, based on the table's primary key.

- `bool deleteAll(const IRdbCondition& condition)`

Deletes data based on the `condition`.

- `bool deleteById(const QVariant& id)`

Deletes data based on the `id`.

- `bool deleteAllByIds(const QVariantList& ids)`

Deletes data based on the primary keys listed in the `ids`.

### Updating Data

- `void updateOne(const Table& table)`

Updates a single data entry.

- `void updateOne(const Table& table, const QStringList& columns)`

Updates a single data entry, modifying only the specified `columns`.

- `void updateAll(const QList<Table>& tables)`

Updates a specified set of data entries.

- `void updateAll(const QList<Table>& tables, const QStringList& columns)`

Updates a specified set of data entries, modifying the fixed columns in `columns`.

- `void updateWhere(const QVariantMap& map, const IRdbCondition& condition)`

Updates the table based on the `condition`. The content to update is provided in `map`.

- `void updateById(const QVariant& id, const QVariantMap& map)`

Updates data entries based on the `id`.

## Custom Operations

When the default queries cannot meet the requirements, users can define SQL statements for custom queries.

### Combining with Existing Algorithms

```cpp
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
        for(const auto& val : value) {
            names.append(val.toString());
        }
        return names;
    }
};
```

As shown in lines 13-20 above, this creates a function to retrieve the top ten students.

### Writing Native SQL Directly

Users can directly write SQL statements for queries.

```cpp
QStringList getTopTenStudents() {
    QString sql = "SELECT name FROM student ORDER BY score LIMIT 10";
    auto query = createQuery(sql);
    query.exec();

    auto values = IRdbUtil::getVariantList(query);
    QStringList names;
    for(const auto& val : values) {
        names.append(val.toString());
    }
    return names;
}
```

Note the usage of `createQuery` above. Users must use `createQuery` to create a query. `createQuery` creates a new `ISqlQuery` object for the query. `ISqlQuery` ensures the correct database connection is used based on the database type, preventing conflicts during data queries.

### ISqlQuery

The `createQuery` function returns an `ISqlQuery` object, which inherits from `QSqlQuery`. Its implementation is as follows:

```cpp
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
};
```

As seen above, the native `bindValue` methods in `ISqlQuery` are disabled, and replaced with `bindParameter`. Therefore, users must use `bindParameter` and `bindParameters` to bind data if they wish to do so.