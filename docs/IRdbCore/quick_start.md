# 快速开始

> 本文档让用户快速开始一个 IRdb 使用示例

IRdbCore 或者 IRdb 是基于 Qt/Sql 模块封装而来的一个数据库访问框架。下面我们以一个简单的例子来说明如何使用 IRdbCore。

## 安装 IRdb

关于如何安装 IRdb，请参考 [包管理系统](../IMakeCore/quick_start.md)。

我们以QMake管理系统为例。这里列出包管理的 packages.json 最简单的配置

=== "packages.json"

    ```json
    {
        "packages":{
            "asio" : "*",
            "nlohmann.json" : "*",
            "ICore" : "*",
            "IRdb" : "*"
        }
    }
    ```

安装完成的项目的内容如下：

=== "目录结构"

    ```
    RdbDemo/
    ├── .lib/
    ├── RdbDemo.pro
    ├── main.cpp
    ├── packages.json
    ```

=== "RdbDemo.pro"

    > 注意，这里添加了 testlib 模块，用于开启测试。sql模块用于支持数据库操作。
    
    ```pro
    QT -= gui
    
    QT += testlib sql
    
    CONFIG += c++17 console
    CONFIG -= app_bundle
    
    SOURCES += \
            main.cpp
    
    include($$(IQMakeCore))
    IQMakeCoreInit()
    include($$PWD/.package.pri)
    ```


=== "main.cpp"

    ```cpp
    #include "core/application/IApplication.h"
    
    int main(int argc, char *argv[])
    {
        IApplication app(argc, argv);
        
        app.run();
    }
    ```

=== "项目面板截图"

    ![image-20250719145043554](assets/image-20250719145043554.png)

这样我们的前期内容就准备好了。

## 创建/连接一个数据库

目前 IRdb 支持5中类型的关系型数据库，用户可以通过扩展支持更多的数据库类型。


=== "SqliteDb.h"

    ```cpp
    #pragma once
    
    #include "rdb/database/IRdbSqliteDatabaseInterface.h"
    
    class SqliteDb : public IRdbSqliteDatabaseInterface<SqliteDb>
    {
    public:
        SqliteDb();
    
    public:
        virtual IRdbDataSource getDataSource() const final;
    };
    
    ```
=== "SqliteDb.cpp"

    ```cpp
    #include "SqliteDb.h"
    
    SqliteDb::SqliteDb()
    {
    
    }
    
    IRdbDataSource SqliteDb::getDataSource() const
    {
        IRdbDataSource source;
        source.databaseName = "SqliteDb.db";
        source.driverName = "QSQLITE";
        return source;
    }
    
    ```

=== "RdbDemo.pro"
    ```pro

    QT -= gui
    
    QT += testlib sql
    
    CONFIG += c++17 console
    CONFIG -= app_bundle
    
    SOURCES += \
            SqliteDb.cpp \
            main.cpp
    
    HEADERS += \
        SqliteDb.h


    include($$(IQMakeCore))
    IQMakeCoreInit()
    include($$PWD/.package.pri)
    
    ```

对于 Qt 中 Sqlite 数据库而言，如果有这个数据库`SqliteDb.db`，则数据库是进行连接操作，如果没有这个数据库文件，则进行创建操作。

我们在运行该程序，会发现程序会自动创建数据库文件`SqliteDb.db`， 创建的位置是程序运行目录，我们打开该目录，可以找到 SqliteDb.db 文件。

=== "当前程序目录"
    ![image-20250719150610678](assets/image-20250719150610678.png)

我们找到了该文件，他的大小是 0kb，数据库中还没有内容。

## 创建一个表

我们创建一个表，StudentTable，包含三个字段：id，name，age。

=== "StudentTable.h"

    ```cpp
    #pragma once
    
    #include "rdb/entity/IRdbTableInterface.h"
    
    class StudentTable : public IRdbTableInterface<StudentTable>
    {
        Q_GADGET
    public:
        StudentTable();
    
    public:
        $PrimaryKey(id)
        $AutoIncrement(id)
        $Column(std::int64_t, id)
    
        $Column(std::string, name)
    
        $Column(int, age)
    };
    
    ```

=== "StudentTable.cpp"

    ```cpp
    
    #include "StudentTable.h"
    
    StudentTable::StudentTable()
    {
    
    }
    ```

=== "RdbDemo.pro"

    ```pro
    QT -= gui
    
    QT += testlib sql
    
    CONFIG += c++17 console
    CONFIG -= app_bundle
    
    SOURCES += \
            SqliteDb.cpp \
            StudentTable.cpp \
            main.cpp
    
    HEADERS += \
        SqliteDb.h \
        StudentTable.h


    include($$(IQMakeCore))
    IQMakeCoreInit()
    include($$PWD/.package.pri)
    
    ```

表我们已经创建好了，下一步我们需要将表和数据库关联起来。

## 创建 Model

将表和数据库关联起来的模块称之为 Model.下面我们创建一个 StudentModel, 如下：


=== "StudentModel.h"

    ```cpp
    #pragma once
    
    #include "rdb/model/IRdbTableModelInterface.h"
    #include "StudentTable.h"
    #include "SqliteDb.h"
    
    class StudentModel : public IRdbTableModelInterface<StudentModel, StudentTable, SqliteDb>
    {
    public:
        StudentModel();
    };
    
    ```


=== "StudentModel.cpp"

    ```cpp
    
    #include "StudentModel.h"
    
    StudentModel::StudentModel()
    {
    
    }
    
    ```

=== "RdbDemo.pro"

    ```pro
    QT -= gui
    
    QT += testlib sql
    
    CONFIG += c++17 console
    CONFIG -= app_bundle
    
    SOURCES += \
            SqliteDb.cpp \
            StudentModel.cpp \
            StudentTable.cpp \
            main.cpp
    
    HEADERS += \
        SqliteDb.h \
        StudentModel.h \
        StudentTable.h


    include($$(IQMakeCore))
    IQMakeCoreInit()
    include($$PWD/.package.pri)
    
    ```

Model 我们已经创建好了。此时我们执行程序，IRdb 会自动的在 SqliteDb.db 数据库中创建 StudentTable 表。

以下是执行程序的结果：

=== "当前程序目录"

    ![image-20250719152055156](assets/image-20250719152055156.png)

=== "console 输出"

    ```
     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
    
    table created class StudentTable
    StudentModel CREATE TABLE:  StudentTable
    ```

=== "SqliteDb.db打开截图"

    ![image-20250719152205194](assets/image-20250719152205194.png)

在上面的代码中，我们看见 SqliteDb.db 已经有数据， console 中告知我们数据表已经创建， SqliteExpert工具中也看见有一张表。

到此为止，我们已经完整的定义了数据库，表，和 模型。下面的案例中我们测试一下这个内容。

## 测试

我们定义测试类 TestRdb类，如下：


=== "TestRdb.h"

    ```cpp
    #pragma once
    
    #include "core/test/IUnitTestInterface.h"
    #include "StudentModel.h"
    
    class TestRdb : public IUnitTestInterface<TestRdb>
    {
        Q_OBJECT
    public:
        TestRdb();
    
    private slots:
        void testInsert();
        void testUpdate();
        void testDelete();
    
    private:
        StudentModel m_model;
    };
    
    ```

=== "TestRdb.cpp"

    ```cpp
    #include "TestRdb.h"
    
    TestRdb::TestRdb()
    {
    
    }
    
    void TestRdb::testInsert()
    {
        Q_ASSERT(m_model.count() == 0);
    
        StudentTable table;
        table.name = "yuekeyuan";
        table.age = 18;
        m_model.insertOne(table);
        Q_ASSERT(m_model.count() == 1);
    
        StudentTable mySon;
        mySon.name = "yueqichu";
        mySon.age = 3;
        m_model.insertOneRef(mySon);
    
        Q_ASSERT(mySon.id == 2);
        Q_ASSERT(m_model.count() == 2);
    }
    
    void TestRdb::testUpdate()
    {
        Q_ASSERT(m_model.count(IRdb::whereEqual(StudentTable::$field_name, "yuekeyuan")) == 1);
        Q_ASSERT(m_model.count(IRdb::whereEqual(StudentTable::$field_name, "zhiyongfei")) == 0);
    
        m_model.updateWhere({{"name", "zhiyongfei",}}, IRdb::whereEqual(StudentTable::$field_name, "yuekeyuan"));
    
        Q_ASSERT(m_model.count(IRdb::whereEqual(StudentTable::$field_name, "yuekeyuan")) == 0);
        Q_ASSERT(m_model.count(IRdb::whereEqual(StudentTable::$field_name, "zhiyongfei")) == 1);
    }
    
    void TestRdb::testDelete()
    {
        m_model.deleteAll(IRdb::whereEqual(StudentTable::$field_age, 18));
        Q_ASSERT(m_model.count() == 1);
    }
    ```
=== "main.cpp"

    > 注意这里我们添加了 `$EnableUnitTest(true)` 宏注解，用于开启单元测试。
    
    > 添加 `$RdbShowSql(true)` 用于开启 SQL 日志输出。
    
    ```cpp
    #include "core/application/IApplication.h"
    #include "rdb/IRdbAnnomacro.h"

    $EnableUnitTest(true)
    $RdbShowSql(true)
    int main(int argc, char *argv[])
    {
        IApplication app(argc, argv);

        app.run();
    }

    ```

=== "console"

    ```txt

     _____  _    _        _      _____
    |_   _|| |  | |      | |    /  __ \
     | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
     | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
    _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
    \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|

    table created class StudentTable
    Sqlite: CREATE TABLE IF NOT EXISTS "StudentTable" ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "name" VARCHAR, "age" INTEGER)
    StudentModel CREATE TABLE:  StudentTable
    START UNIT TEST
    ********* Start testing of TestRdb *********
    Config: Using QtTest library 5.14.2, Qt 5.14.2 (i386-little_endian-ilp32 shared (dynamic) debug build; by MSVC 2017)
    PASS   : TestRdb::initTestCase()
    QDEBUG : TestRdb::testInsert() Sqlite: SELECT count(1) FROM "StudentTable"
    QDEBUG : TestRdb::testInsert() Sqlite: INSERT INTO "StudentTable" (name, age) VALUES (:name, :age)
    QDEBUG : TestRdb::testInsert() bound:  ":age" -> QVariant(int, 18)
    QDEBUG : TestRdb::testInsert() bound:  ":name" -> QVariant(std::string, "yuekeyuan")
    QDEBUG : TestRdb::testInsert() Sqlite: SELECT count(1) FROM "StudentTable"
    QDEBUG : TestRdb::testInsert() Sqlite: INSERT INTO "StudentTable" (name, age) VALUES (:name, :age)
    QDEBUG : TestRdb::testInsert() bound:  ":age" -> QVariant(int, 3)
    QDEBUG : TestRdb::testInsert() bound:  ":name" -> QVariant(std::string, "yueqichu")
    QDEBUG : TestRdb::testInsert() Sqlite: SELECT count(1) FROM "StudentTable"
    PASS   : TestRdb::testInsert()
    QDEBUG : TestRdb::testUpdate() Sqlite: SELECT count(1) FROM "StudentTable"  WHERE name = :name_0
    QDEBUG : TestRdb::testUpdate() bound:  ":name_0" -> QVariant(QString, "yuekeyuan")
    QDEBUG : TestRdb::testUpdate() Sqlite: SELECT count(1) FROM "StudentTable"  WHERE name = :name_1
    QDEBUG : TestRdb::testUpdate() bound:  ":name_1" -> QVariant(QString, "zhiyongfei")
    QDEBUG : TestRdb::testUpdate() Sqlite: UPDATE "StudentTable" SET name= :name WHERE name = :name_2
    QDEBUG : TestRdb::testUpdate() bound:  ":name" -> QVariant(QString, "zhiyongfei")
    QDEBUG : TestRdb::testUpdate() bound:  ":name_2" -> QVariant(QString, "yuekeyuan")
    QDEBUG : TestRdb::testUpdate() Sqlite: SELECT count(1) FROM "StudentTable"  WHERE name = :name_3
    QDEBUG : TestRdb::testUpdate() bound:  ":name_3" -> QVariant(QString, "yuekeyuan")
    QDEBUG : TestRdb::testUpdate() Sqlite: SELECT count(1) FROM "StudentTable"  WHERE name = :name_4
    QDEBUG : TestRdb::testUpdate() bound:  ":name_4" -> QVariant(QString, "zhiyongfei")
    PASS   : TestRdb::testUpdate()
    QDEBUG : TestRdb::testDelete() Sqlite: DELETE FROM "StudentTable" WHERE age = :age_5
    QDEBUG : TestRdb::testDelete() bound:  ":age_5" -> QVariant(int, 18)
    QDEBUG : TestRdb::testDelete() Sqlite: SELECT count(1) FROM "StudentTable"
    PASS   : TestRdb::testDelete()
    PASS   : TestRdb::cleanupTestCase()
    Totals: 5 passed, 0 failed, 0 skipped, 0 blacklisted, 27ms
    ********* Finished testing of TestRdb *********
    ```

=== "数据库截图"
    > 此截图是运行最终的截图

    ![image-20250719160712898](assets/image-20250719160712898.png)


测试完全没有问题，我们的程序运行也非常完美！


## 接下来

下面请继续阅读相关的文档，有对 IRdb 使用方式有更详细的说明。
