# Introduction to IRdbCore

## Overview

In the Java network programming field, frameworks like Spring JPA, MyBatis, and Hibernate have introduced a series of database management solutions that are quite convenient. By simply defining beans, defining repositories, and defining how to connect to the database, one can manage databases, database tables, and database operations effectively.

However, in the C++ programming world, connecting to a database requires manually implementing a series of operations, which can be cumbersome and intimidating. IRdbCore was developed to address this issue.

IRdb-core leverages the reflection encapsulation provided by IWebCore to seamlessly handle bean encapsulation. It can easily convert database query results into C++ types and facilitate conversions between C++ types and JSON types. By inheriting from the `IRdbTableModelInterface` base class, developers can perform database CRUD operations by overriding the base class methods. Through a database base class and dialects (which allow for different SQL dialects for different databases), IRdbCore makes it easy to connect to various types of databases. Built-in utility classes help parse query results and other operations, improving coding efficiency.

## Features

1. **Object-Relational Mapping Support**

   By annotating C++ classes, IRdbCore enables mapping between C++ objects and database tables, achieving bidirectional mapping between objects and relational databases.

2. **Persistence Context for Simplified Data Access Layer**

   IRdbCore introduces the concept of a persistence context, responsible for managing the lifecycle of entities. It handles operations such as adding, deleting, updating, and querying data. Developers can execute database operations through related interfaces without explicitly writing implementation code.

3. **Built-in Support for Pagination, Sorting, Aggregation, and Conditional Queries**

   IRdbCore includes native support for pagination, sorting, aggregation, and conditional queries, simplifying query implementation.

4. **Easy to Extend**

   Users can manually write SQL statements to implement custom database operations.

5. **Multi-Database Support**

   IRdbCore natively supports databases such as SQLite, MySQL, MariaDB, SQL Server, and PostgreSQL. Users can also extend support for more databases using built-in interfaces.

6. **Cross-Platform Support**

   Any platform supporting Qt can host this framework, including but not limited to Linux, Windows, Mac, Android, and others.

7. **Utility Classes for Query Conversion**

   IRdbCore provides utility classes to further convert query results into the data types users need.

8. **Exception and Optional Return Value Management**

   The framework throws exceptions for various database errors and user misoperations. For cases where users expect data but none is found, it returns an `Optional`.

9. **Seamless Integration with Other Frameworks**

   IRdbCore can be easily integrated with other frameworks such as `IHttpCore` and `ICmdCore`, providing database operation capabilities.

10. **Runtime Logic Check**

    IRdbCore performs logic checks at the start of program execution, such as verifying entity definitions, database existence, and connectivity. This reduces runtime errors.

## Additional Notes

- **Why We Chose "IRdbCore" Instead of "IOrmCore"**

   Previously, the framework was named "IOrmCore." The term "ORM" stands for **Object-Relational Mapping**, which refers to object-relational mapping. However, we plan to add support for non-relational databases in the future, such as `IRedisCore`, `IMongoDbCore`, and others. To maintain consistency, we changed the name to **IRdbCore**, which signifies that this library will handle all relational data.

- **More Information**

   For additional details, please refer to the documentation provided later.