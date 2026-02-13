# Database

## Database Interfaces

### Five Databases

The base class for database creation in IRdbCore uses different database base classes depending on the database type. We provide support for five databases as follows:

| Name      | Interface                        |
| :-------- | :------------------------------- |
| MySql     | `IRdbMysqlDatabaseInterface`     |
| Sqlite    | `IRdbSqliteDatabaseInterface`    |
| Postgres  | `IRdbPostgreDatabaseInterface`   |
| SqlServer | `IRdbSqlServerDatabaseInterface` |
| MariaDb   | `IRdbMariaDbDatabaseInterface`   |

If users wish to implement support for their own database type, the naming should follow the same rules as the interfaces above. For example, if implementing a database named "Doggy," the interface should be named `IRdbDoggyDatabaseInterface`.

### IRdbXxxDatabaseInterface

Among the various database interfaces, they are largely similar. Let’s take `IRdbSqliteDatabaseInterface` as an example. Its interface is as follows:

```c++
template<typename T, bool enabled = true>  
class IRdbSqliteDatabaseInterface : public IRdbDatabaseInterface<T, IRdbSqliteDialect, enabled>  
{  
public:  
    IRdbSqliteDatabaseInterface() = default;  

public:  
    virtual QSqlDatabase openDatatbase(const IRdbSource &) override;  
};  
```

This base class implements the `openDatabase` function, which takes the `IRdbSource` parameter. The `IRdbSource` parameter is obtained from the `getSource` function in a deeper base class. This function is always a pure virtual function, so users must override it when implementing a database instance. We will revisit this function later.

### IRdbDatabaseInterface

As seen above, `IRdbSqliteDatabaseInterface` inherits from `IRdbDatabaseInterface`. In fact, all database base classes inherit from `IRdbDatabaseInterface`, which is implemented as follows:

```c++
template<typename T, typename Dialect, bool enabled = true>  
class IRdbDatabaseInterface : public IRdbDatabaseWare, public ITaskWareUnit<T, IRdbCatagory>, public ISingletonUnit<T>  
{  
public:  
    IRdbDatabaseInterface();  

public:  
    const IRdbDialect& getDialect() const;  

public:  
    virtual QString getClassName() const final;  

public:  
    virtual double $order() const final;  
    virtual void $task() final;  
};  
```

When inheriting `IRdbDatabaseInterface`, three template parameters must be provided:

1. **CRTP class name**: The name of the specific database class.
2. **`Dialect`**: The dialect implementation for the current database, which handles SQL variations across databases (explained later in the Dialect section).
3. **`bool enabled`**: Indicates whether the database connection is tested. If the test fails, an error is reported.

`IRdbDatabaseInterface` inherits from three classes:

1. `IRdbDatabaseWare`: Discussed later.
2. `ITaskWareUnit`: A task registration system. The overridden `$order()` and `$task()` functions are inherited from `ITaskWareUnit`, where `$order()` sorts tasks and `$task()` executes them.
3. `ISingletonUnit<T>`: Provides a `T& instance()` function for type `T`, allowing databases to be used as Meyer’s singletons.

### IRdbDatabaseWare

Its implementation is as follows:

```c++
class IRdbDatabaseWare  
{  
public:  
    explicit IRdbDatabaseWare(const IRdbDialect&);  
    virtual ~IRdbDatabaseWare();  

public:  
    ISqlQuery createQuery();  

public:  
    virtual IRdbSource getSource() const = 0;  
    virtual QString getClassName() const = 0;  
    QStringList getRdbTables() const;  
    QStringList getRdbViews() const;  
    virtual void dropTable(const IRdbTableInfo& table);  
    virtual void dropView(const IRdbViewInfo& view);  

protected:  
    virtual QSqlDatabase openDatatbase(const IRdbSource&) = 0;  

public:  
    const IRdbDialect& m_dialect;  
    QSqlDatabase m_db;  
};  
```

This base class holds a reference to `IRdbDialect& m_dialect`, which handles database-specific SQL generation.

Notable functions:

- `ISqlQuery createQuery()`: Creates an `ISqlQuery` object for executing database operations (used in models for CRUD operations).
- `getRdbTables()`: Retrieves all table names.
- `getRdbViews()`: Retrieves all view names.
- `dropTable()` and `dropView()`: Delete tables and views, respectively.
- `getSource()`: Returns an `IRdbSource` object containing database connection details.

## IRdbSource

`IRdbSource` contains driver name, database name, and other connection details. The required fields vary by database type.

## IRdbDialect

The `IRdbDialect` implementation is as follows:

```c++
class IRdbDialectWare  
{  
public:  
    IRdbDialectWare() = default;  
    virtual ~IRdbDialectWare() = default;  

public:  
    virtual QString databaseType() const = 0;  

public:  
    virtual QString createTableSql(const IRdbTableInfo& info) const;  
    virtual QString dropTableSql(const IRdbTableInfo& info) const;  
    virtual QString dropViewSql(const IRdbViewInfo& info) const;  

    QString countSql(const IRdbEntityInfo& info) const;  
    QString countSql(const IRdbEntityInfo& info, const IRdbCondition& condition) const;  

    virtual void insert(ISqlQuery &query, const IRdbTableInfo &info, void *) const;  
    virtual void insert(ISqlQuery& query, const IRdbTableInfo& info, const void*) const;  

    void insertAll(ISqlQuery& query, const IRdbTableInfo& info, QVector<const void*>) const;  

    QString findOneSql(const IRdbEntityInfo& info, const IRdbCondition& condition) const;  
    QString findAllSql(const IRdbEntityInfo& info) const;  
    QString findAllSql(const IRdbEntityInfo &info, const IRdbCondition& condition) const;  
    QString findColumnSql(const IRdbEntityInfo& info, const QStringList& columns) const;  
    QString findColumnSql(const IRdbEntityInfo& info, const QStringList& columns, const IRdbCondition&) const;  

    QString existSql(const IRdbEntityInfo&, const IRdbCondition&) const;  

    QString updateOne(const IRdbTableInfo& info, const QStringList& columns) const;  
    QString updateWhere(const IRdbTableInfo& info, const QVariantMap& map, const IRdbCondition& condition) const;  

    QString deleteTableSql(const IRdbEntityInfo& info) const;  
    QString deleteTableSql(const IRdbEntityInfo& info, const IRdbCondition& condition) const;  
    QString truncateTableSql(const IRdbEntityInfo& info) const;  

    virtual QString getSqlType(const IRdbTableInfo& info, int index) const = 0;  

public:  
    QString conditionToSql(const IRdbCondition&) const;  

protected:  
    QString toWhereSql(const IRdbCondition&) const;  
    QString toOrderBySql(const IRdbCondition&) const;  
    QString toGroupBySql(const IRdbCondition&) const;  
    QString toHavingSql(const IRdbCondition&) const;  
    QString toLimitSql(const IRdbCondition&) const;  

    QString fromWhereClause(const IRdbWhereClause&) const;  
    QString fromOrderByClause(const IRdbOrderByClause&) const;  
    virtual QString fromLimitClause(const IRdbLimitClause&) const;  
    QString fromGroupByClause(const IRdbGroupByClause&) const;  
    QString fromHavingClause(const IRdbHavingClause&) const;  
    virtual QString createSqlCommonKeyClause(const IRdbTableInfo& info, int index) const;  

public:  
    virtual void bindParameter(QSqlQuery& query, const QString& field, const QVariant& value) const;  
    virtual QString quoteName(const QString& name) const;  

protected:  
    static QString getVividName(const QString&);  
};  
```

This class generates SQL statements, handling dialect differences. Common SQL logic is implemented in the base class, while database-specific logic is overridden in derived classes.

## Differences Across Databases

### Sqlite

Implementation example:

```c++
// SqliteDb.h  
#pragma once  

#include "rdb/database/IRdbSqliteDatabaseInterface.h"  

class SqliteDb : public IRdbSqliteDatabaseInterface<SqliteDb>  
{  
public:  
    SqliteDb() = default;  

public:  
    virtual IRdbSource getSource() const final;  
};  

// SqliteDb.cpp  
#include "SqliteDb.h"  

IRdbSource SqliteDb::getSource() const  
{  
    IRdbSource source;  
    source.databaseName = "abcde.db";  
    source.driverName = "QSQLITE";  
    return source;  
}  
```

This creates a database file `abcde.db` in the program’s root directory.

### MySql

MySQL support is not enabled by default on Windows. Users must manually compile the required DLLs.

Sample code (configured via Docker):

```c++
// MySqlDb.h  
#pragma once  

#include "rdb/database/IRdbMySqlDatabaseInterface.h"  
using namespace IWebCore;  

class MySqlDb : public IRdbMysqlDatabaseInterface<MySqlDb>  
{  
public:  
    MySqlDb() = default;  

public:  
    virtual IRdbSource getSource() const final;  
};  

// MySqlDb.cpp  
#include "MySqlDb.h"  

IRdbSource MySqlDb::getSource() const  
{  
    IRdbSource source;  
    source.driverName = "QMYSQL";  
    source.databaseName = "TestDb";  
    source.host = "127.0.0.1";  
    source.user = "root";  
    source.password = "xxxx";  
    source.port = 3306;  
    return source;  
}  
```

### MariaDb

Sample code (similar to MySQL):
```c++
// MariaDb.h  
#pragma once  

#include "rdb/database/IRdbMariaDbDatabaseInterface.h"  

class MariaDb : public IRdbMariaDbDatabaseInterface<MariaDb>  
{  
public:  
    MariaDb() = default;  

public:  
    virtual IRdbSource getSource() const final;  
};  

// MariaDb.cpp  
#include "MariaDb.h"  

IRdbSource MariaDb::getSource() const  
{  
    IRdbSource source;  
    source.driverName = "QMYSQL";  
    source.databaseName = "TestDb";  
    source.host = "127.0.0.1";  
    source.user = "root";  
    source.password = "xxxx";  
    source.port = 3305;  
    return source;  
}  
```

### SqlServer

Configured via ODBC:
```c++
// SqlServerDb.h  
#pragma once  

#include "rdb/database/IRdbSqlServerDatabaseInterface.h"  

class SqlServerDb : public IRdbSqlServerDatabaseInterface<SqlServerDb>  
{  
public:  
    SqlServerDb() = default;  

public:  
    virtual IRdbSource getSource() const final;  
};  

// SqlServerDb.cpp  
#include "SqlServerDb.h"  

IRdbSource SqlServerDb::getSource() const  
{  
    IRdbSource source;  
    source.driverName = "QODBC3";  
    source.databaseName = "TestDb";  
    source.user = "sa";  
    source.password = "xxxxxxxx";  
    source.host = "localhost";  
    source.port = 1433;  

    return source;  
}  
```

### Postgres

Sample code (Qt-supported):
```c++
// PostgresDb.h  
#pragma once  

#include "rdb/database/IRdbPostgreDatabaseInterface.h"  

class PostgreDb : public IRdbPostgreDatabaseInterface<PostgreDb>  
{  
public:  
    PostgreDb() = default;  

public:  
    virtual IRdbSource getSource() const final;  
};  

// PostgresDb.cpp  
#include "PostgreDb.h"  

IRdbSource PostgreDb::getSource() const  
{  
    IRdbSource source;  
    source.driverName = "QPSQL";  
    source.databaseName = "TestDb";  
    source.user = "postgres";  
    source.password = "xxx";  
    source.host = "127.0.0.1";  
    source.port = 5432;  

    return source;  
}  
```

## Extending Database Types

To extend a database type, users must create their own classes by inheriting the following base classes.

### Dialect

Users should inherit `IRdbDialectInterface` to create a custom dialect. Override necessary functions, ensuring consistency in naming (e.g., `IRdbXxxxDialect`).

### Database

Create a `DatabaseInterface` class following existing examples. Use the naming convention `IRdbXxxDatabaseInterface`.