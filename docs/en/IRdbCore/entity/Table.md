# Table Entity

> This document describes the creation of the Table entity.

![po_bheccichficdga](assets/7YVZH3I6ABAAG)

------

## ITableInterface

### Code Implementation

When defining a table entity, we inherit the `IRdbTableInterface` class. The code implementation of `IRdbTableInterface` is as follows:

```cpp
template<typename T, bool enabled=true>
class IRdbTableInterface : public IBeanInterface<T, enabled>
{
public:
    IRdbTableInterface() = default;

public:
    static const IRdbTableInfo& staticEntityInfo();
};

template<typename T, bool enabled>
const IRdbTableInfo& IRdbTableInterface<T, enabled>::staticEntityInfo()
{
    static IRdbTableInfo s_info(T::staticMetaObject);
    return s_info;
}
```

### IBeanInterface Introduction

For details on `IBeanInterface`, you can refer to the content of `Bean`. Here, we briefly explain this concept.

The simplified code is as follows:

```cpp
template<typename T, bool enabled = true, typename U=IBeanDefaultTrait>
class IBeanInterface : public ITaskInstantUnit<T, enabled>, protected U, protected IBeanRegisterTypeUnit<T>
{
public:
    IBeanInterface() = default;

public:
    virtual IJson toJson() const;
    virtual bool loadJson(const IJson &value);

protected:
    virtual void $task() override;
};
```

When a class inherits `IBeanInterface`, we need to define the fields used for reflection. Fields are defined using two methods: `$BeanFieldDeclare` and `$BeanField`. 

`$BeanFieldDeclare` is used to declare a field, followed by its definition. `$BeanField` combines the declaration and definition. For example, to define a `name` field, the following two methods are equivalent and valid.

```cpp
// Method 1
$BeanFieldDeclare(QString, name)
QString name;

// Method 2
$BeanField(QString, name)
```

If you want to initialize a field during definition, you can do so as follows. Both methods generate the same code.

```cpp
// Method 1
$BeanFieldDeclare(QString, name)
QString name {"hello world"};

// Method 2
$BeanField(QString, name, "hello world")
```

### IRdbTableInfo

In `IRdbTableInterface`, the code `static const IRdbTableInfo& staticEntityInfo();` converts the entity information into a static member function call to return to the user. Its implementation is as follows:

```cpp
class IRdbTableInfo : public IRdbEntityInfo, public INoCopyMoveUnit
{
public:
    struct ValueMaker{
        enum Type{
            ReadValue,
            InsertValue,
            GenerateValue,
        };
        int index{};
        Type type{ReadValue};
        QString insertValue;
        IRdbManage::GeneratorFunction generator;
    };

public:
    IRdbTableInfo() = delete;
    explicit IRdbTableInfo(const QMetaObject& meta);

public:
    int primaryKey {-1};
    int autoIncrement{-1};
    QList<int> notNullKeys;
    QList<int> uniqueKeys;
    QMap<int, QString> constraints;
    QMap<int, QString> sqlType;
    QVector<ValueMaker> valueMakers;
};
```

It inherits from `IRdbEntityInfo` as follows:

```cpp
class IRdbEntityInfo
{
public:
    struct Field
    {
        int index{};
        QString name;
        QString typeName;
        QMetaType::Type typeId;
        QMetaProperty property;
    };

public:
    explicit IRdbEntityInfo(const QMetaObject& meta);

public:
    const QMetaObject& m_metaObject;

public:
    QString className;
    QString entityName;

    QList<Field> fields;
    QStringList fieldNames;
};
```

From the above code, we can see that `IRdbTableInfo` retains a series of original information, which can be used to operate on database tables.

## Column Annotations

### $Column and $ColumnDeclare Macro Annotations

These macro annotations are used as follows:

```cpp
class Student : public IRdbTableInterface<Student>
{
public:
    Student() = default;

public:
    $Column(qlonglong, id)    // No default value
    
    $Column(int, salary, 0)    // Default is 0
    
    $ColumnDeclare(int, age)   // No default value
    int age;

    $ColumnDeclare(bool, isMale)
    bool isMale{true};    // Default is true
}
```

After using the above methods to define fields, a static member constant `$field_xxx` is automatically defined. For example, the implementation of `ColumnDeclare` is as follows:

```cpp
#define $ColumnDeclare(type, name) \
    static constexpr char const * $field_##name = #name ; \
    $BeanFieldDeclare(type, name)

#define $Column_2(type, name) \
    static constexpr char const * $field_##name = #name ; \
    $BeanField(type, name)
```

As shown above, the following code is automatically added:

```cpp
class Student : public IRdbTableInterface<Student>
{
public:
    Student() = default;

public:
    static constexpr char const * $field_id = "id";
    Q_PROPERTY(qlonglong id MEMBER id)
    qlonglong id;

    static constexpr char const * $field_salary = "salary";
    Q_PROPERTY(int salary MEMBER salary)
    int salary{ 0 };
    
    static constexpr char const * $field_age = "age";
    Q_PROPERTY(int age MEMBER age)
    int age;

    static constexpr char const * $field_isMale = "isMale";
    Q_PROPERTY(int isMale MEMBER isMale)
    bool isMale{true};
}
```

In subsequent queries, we can directly use `$field_id` to represent the `id` column, reducing the likelihood of errors.

### $SqlType Macro Annotation

This annotation is used when generating the table. When generating the table creation statement, the field type is mapped by default. For example, in `MySql`, `std::string` is mapped to `VARCHAR(100)`. Users can define custom mappings using this annotation, as shown below:

```cpp
$SqlType(name, TEXT)
$Column(std::string, name)
```

This maps the `name` field to `TEXT` in SQL.

In SQLite, it is translated as follows:

```cpp
name TEXT,
```

### $NotNull

This annotation marks the column as non-null in SQL, meaning it cannot have a null value. It is used when generating the table creation statement, typically adding a `NOT NULL` constraint. The usage is as follows:

```cpp
$NotNull(name)
$Column(std::string, name)
```

In SQLite, it is translated as follows:

```cpp
name VARCHAR NOT NULL,
```

### $Unique

This annotation indicates that the column cannot have duplicate values. It is commonly used for primary keys but can also be used for other non-duplicate columns. The usage is as follows:

```cpp
$Unique(idNumber)
$Column(int, idNumber)
```

In SQLite, it is translated as follows:

```cpp
idNumber INTEGER UNIQUE,
```

### $Constraint

This is a general-purpose annotation. When creating a database table, the content of `$Constraint` is appended to the column definition. For example:

```cpp
$Constraint("CHECK (age >= 18) default 20")
$Column(int, age)
```

In MySQL, it is translated as follows:

```cpp
age INT CHECK (age >= 18) default 20,
```

## Primary Key Annotations

In the Table entity, there must be exactly one primary key. The primary key is annotated using `$PrimaryKey`. If a table does not have a primary key, an error is thrown during runtime.

Currently, the supported primary key data types are strings and numeric types. Other types will result in an error.

### $PrimaryKey

This macro annotation is used to designate a field as the primary key. The usage is as follows:

```cpp
$PrimaryKey(id)
$ColumnDeclare(qlonglong, id)
qlonglong id;
```

The generated SQL is as follows:

```cpp
id INTEGER PRIMARY KEY,
```

### $AutoIncrement

This macro annotation is used for auto-increment fields. It is applied to numeric fields. If the field is not numeric, an error is thrown. The usage is as follows:

```cpp
$AutoIncrement(id)
$PrimaryKey(id)
$Column(qlonglong, id)
```

In MySQL, the generated SQL is as follows:

```cpp
BIGINT PRIMARY KEY AUTO_INCREMENT,
```

Different databases may generate different SQL, but the code remains valid.

### $GenerateValue

This macro annotation is used for custom primary key generation. While `$AutoIncrement` is for numeric fields, `$GenerateValue` allows users to define their own generation method. For example:

```cpp
$GenerateValue(id, "uuid")
$PrimaryKey(id)
$ColumnDeclare(QString, id)
QString id;
```

The primary key generation method for the database table is set to `uuid`. For more details, refer to `IRdbValueGeneratorInterface`.