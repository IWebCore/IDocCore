# Table 实体

> 本文档描述 Table 实体的创建

![po_bheccichficdga](assets/7YVZH3I6ABAAG)

------

## ITableInterface

### 代码实现

我们在定义定义一个 table实体的时候，会继承 ***\*IRdbTableInterface\**** 这个类。IRdbTableInterface 的代码实现如下：

```c++
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



### IBeanInterface 简介

关于 IBeanInterface 的具体内容可以参考 ***\*Bean\**** 的内容，这里我们简单讲述以下这个东西。

代码简化后如下：

```c++
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

我们在 Bean 中实现了 Bean 的 `toJson` 和 `loadJson` 这两个函数。配合我们们 `IJsonUtil`工具库，可以将 Bean， Bean容器（QList<Bean>, std::list<Bean> std::vector<Bean>等一系列的复合类型），Bean关联容器（QMap<QString, Bean>, std:map<QString, Bean>）与 Json 类型相互转换。



当一个对象继承IBeanInterface之后，我我们还需要定义哪些字段用于反射字段。字段使用 `$BeanFieldDeclare` 和 `$BeanField` 两种定义方式。

$BeanFieldDeclare 是***\*声明\****这个字段, 之后需要跟上我们对这个字段的定义。 而$BeanField 则是证明加上定义在一起。如下，如果我们要定义一个 name 字段，那么如下两个定义方式都是合法且等价的。

```c++
// 方式一
$BeanFieldDeclare(QString, name)
QString name;

// 方式二
$BeanField(QString, name)
```



如果我们希望在参数定义的时候进行初始化，那么可以按照如下的方式进行初始化。第二种方式会生成相通的代码。

```c++
// 方式一
$BeanFieldDeclare(QString, name)
QString name {"hello world"};

// 方式二
$BeanField(QString, name, "hello world")
```



### IRdbTableInfo

在 IRdbTableInterface 中，我们看到了`static const IRdbTableInfo& staticEntityInfo();` 这一行的代码。他是将这个类的信息变换成成为静态成员函数调用返回给使用者。他的构造如下：

```c++
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

他继承了一个 `IRdbEntityInfo` 如下

```c++
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

通过上面的源码我们可以看到通过 IRdbTableInfo 保留一系列的原始信息。我们可以利用这些原始信息来操作数据库表



## 列相关注解

### $Column 和 $ColumnDeclare 宏注解

这两个宏注解的使用方法如下

```c++
class Student : public IRdbTableInterface<Student>
{
public:
    Student() = default;

public:
    $Column(qlonglong, id)    // 无默认值
    
    $Column(int, salary, 0)    // 默认为0
    
    $ColumnDeclare(int, age)   // 无默认值
    int age;

    $ColumnDeclare(bool, isMale)
    bool isMale{true};    // 默认为男性
}
```

在使用上述两种方式定字段之后，我们同样会自动定义一个静态成员常量 `$field_xxx`

举例 ColumnDeclare 实现如下：

```c++
#define $ColumnDeclare(type, name) \
    static constexpr char const * $field_##name = #name ; \
    $BeanFieldDeclare(type, name)

#define $Column_2(type, name) \
    static constexpr char const * $field_##name = #name ; \
    $BeanField(type, name)
```

如上所示，我们在代码中会自动添加如下的代码

```c++
class Student : public IRdbTableInterface<Student>
{
public:
    Student() = default;s

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

在之后的查询中，我们可以直接使用 `$field_id` 来表示 `id` 列，而不是使用`"id"` 这种硬编码方式，减少代码出错率。



### $SqlType 宏注解

该注解是用于生成Table时使用的，我们在生成 数据库表创建语句的时候，会将字段类型进行默认映射。比如 在 `MySql` 中，我们会将 `std::string` 类型映射成`VARCHAR(100)`这个类型。用户自定义映射方式可以使用这个字段，比如

```c++
$SqlType(name, TEXT)
$Column(std::string, name)
```

此时 name 的 SQL 类型会被映射成为 `TEXT`。

这列在Sqlite中会翻译成如下：

```c++
name TEXT,
```

### $NotNull

该注解标记，表示当前列在sql 中是非空，不能插入空值。该注解在生成创建表语句的时候使用，一般会添加 `NOT NULL` 约束。使用方法如下

```c++
$NotNull(name)
$Column(std::string, name)
```

此时如果 INSERT 插入如果忽略 name 列，则插入不成功。

这列在Sqlite 中会翻译成如下：

```c++
name VARCHAR NOT NULL,
```

### $Unique

该注解表示当前列不能重复。一般用于主键注解上面。但是也可以用在其他表示不重复的列上面。使用方法如下

```c++
$Unique(idNumber)
$Column(int, idNumber)
```

这个列在sqlite中会翻译成：

```c++
idNumber INTEGER UNIQUE,
```



### $Constraint

该注解是一个通用的注解，他会在创建数据库表的时候，将`$Constraint`中的内容拼接在后面。举例如下：

```c++
$Constraint("CHECK (age >= 18) default 20")
$Column(int, age)
```

这条语句在MySql中会翻译成如下：

```c++
age INT CHECK (age >= 18) default 20,
```



## 主键相关的注解

在 Table 实体中，要求需要有一个，必须且只能有一个主键，该主键使用`$PrimaryKey`进行标注。如果一个 Table 中没有主键，在运行初期，程序会报错提示没有主键。

 目前我们支持的主键数据类型为 字符串 和数字类型 两种主要类型。其他的类型会报错。

数字类型中我们建议的是 `qlonglong` 这种类型，因为作为主键类型，这种类型更安全。



### $PrimaryKey

该宏注解是将一个对象映射成为主键，使用方法如下：

```c++
$PrimaryKey(id)
$ColumnDeclare(qlonglong, id)
qlonglong id;
```

 上面的代码会生成如下的SQL

```c++
id INTEGER PRIMARY KEY,
```

### $AutoIncreament

该宏注解用于主键自增字段，注解数值类型的字段。如果不是数值类型，则程序会运行报错。使用方式如下：

```c++
$AutoIncrement(id)
$PrimaryKey(id)
$Column(qlonglong, id)
```

该代码在MySql数据库中生成如下:

```c++
BIGINT PRIMARY KEY AUTO_INCREMENT,
```

不同的数据库生成的内容不一致，但都能生成正常的代码。



### $GenerateValue

该宏注解用于主键。`$AutoInrecrement` 是用于数值字段，而该宏注解则是用户自定义的主键设置方式。默认的增长方式有`uuid`,用户则可以定义自己的增长方式。举个例子：

```c++
$GenerateValue(id, "uuid")
$PrimaryKey(id)
$ColumnDeclare(QString, id)
QString id;
```

那么在 数据库表在主键上增长方式则是`uuid`。关于

如何定义主键，请参考 `IRdbValueGeneratorInterface`。