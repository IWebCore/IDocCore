---
hide:
  - navigation  # 隐藏导航栏
  - toc         # 隐藏目录
  - footer      # 隐藏页脚
layout: fullscreen  # 自定义布局标识
---

# IWebCore

<p align="center">
<pre> 
 _____  _    _        _      _____
|_   _|| |  | |      | |    /  __ \
  | |  | |  | |  ___ | |__  | /  \/  ___   _ __  ___
  | |  | |/\| | / _ \| '_ \ | |     / _ \ | '__|/ _ \
 _| |_ \  /\  /|  __/| |_) || \__/\| (_) || |  |  __/
 \___/  \/  \/  \___||_.__/  \____/ \___/ |_|   \___|
</pre>
</p>

## 📦 核心模块介绍

!!! info "IMakeCore - Cpper梦想中的包管理工具"
    **简单到极致的跨平台包管理工具** 
    IMakeCore站在巨人的肩膀上，提供了基于源代码的包管理工具。支持跨平台、qmake/cmake非侵入式集成，一行命令可以集成IMakeCore, 以如下的方式就可以引用包:

    ```json
    {
        "packages":{
            "ICore":"*",
            "ITcp":"*",
            "IHttp":"1.0.0",
            "IRdb":"1.0.0",
            "INody":"1.0.0",
            "asio":"*",
            "nlohmann.json": "*",
            "zlib":"1.3.1",
            "stachenov.quazip":"1.5.0"
        }
    }
    ```
    [查看文档 →](./IMakeCore/quick_start.md)

!!! warning "IHttpCore - 反射式/注解式的HTTP框架"
    **高性能用户友好的HTTP服务器框架**  
    IHttpCore是一个轻量级但功能强大的HTTP服务框架，用户可以使用注解来完成 Http 请求响应。
    ```cpp
    class PackageController : public IHttpControllerInterface<PackageController>
    {
        Q_GADGET
        $AsController(package)
    public:
        PackageController();

        $GetMapping(updatePackage)
        IStatusResponse updatePackage();
    
        $GetMapping(pagingList, /list)
        IJsonResponse pagingList(int $Query(page), int $Query(per_page), QString $Query(sort), QString $Query(order));
    
        $GetMapping(versions, /versions/<name>)
        QList<PackageInfo> versions(QString $Path(name));
    }
    ```
    
    [快速开始 →](IHttpCore/overview.md)

!!! success "IRdbCore - 关系数据库"
    **现代化傻瓜式数据库操作工具** 

    === "User.h"
        ```cpp
        class User : public IRdbTableInterface<User>
        {
            Q_GADGET
        public:
            User();
        
        public:
            $AutoIncrement(id)
            $PrimaryKey(id)
            $ColumnDeclare(std::int64_t, id)
            std::int64_t id{0};
        
            $Column(QString, user_name)
        
            $Column(QString, email)
        
            $Column(QString, password_hash)
        
            $Column(QString, salt)
        };
        ```
    === "Model.h"
        ```cpp
        class UserModel : public IRdbTableModelInterface<UserModel, User, PkgDatabase>
        {
        public:
            UserModel();
        };
        ```
    
    === "Usage.h"
        ```cpp
        UserModel m_userModel;
        
        // check email and user name
        if(m_userModel.exist(IRdb::whereEqual(User::$field_email, email))){
            return IHttpBadRequestInvalid("email has be used, please select another email, or login");
        }
        if(m_userModel.exist(IRdbCondition().whereEqual(User::$field_user_name, username))){
            return IHttpBadRequestInvalid("user name already exist");
        }
        
        // insert user
        User user;
        user.user_name = username;
        user.email = email;
        user.salt = xxxx;
        user.password_hash = xxxxx;
        m_userModel.insertOneRef(user);
        
        // find user by id
        auto user = m_userModel.findById(id);
        ```
    
    [了解详情 →](IRdbCore/overview.md)

!!! danger "IPubCore - 包发布/查询/下载系统"
    **企业级发布管理平台**  
    [IPubCore](https://pub.iwebcore.org)  提供一个企业级的包发布管理平台，支持：

    - 🏭 c++源代码包查询
    - 🛡️ 结合 IMakeCore 包自动下载
    - 📊 用户注册/用户管理
    - 🔗 用户包上传
    
    [使用指南 →](https://pub.iwebcore.org)

!!! note "ICore - 基础框架"
    **框架核心组件库**  
    ICore包含了框架的基础组件和工具类，为其他模块提供底层支持。

    - 🧰 依赖注入容器
    - ⏱️ 任务调度系统
    - 🔐 安全组件
    - 🛠️ 实用工具集
    - 🌈 配置系统
    - 🖥️ 事件循环
    - 🗄️ 数据库组件
    
    [核心功能 →](ICore/IApplication.md)

!!! tip "ICmd - 命令行开发套件"
    **用户友好的命令行解析，开发框架**
    ICmd是一个基于ICore的命令行开发框架，提供了命令行解析、命令行参数、命令行选项、命令行子命令等功能, 让用户专注于功能代码。

    === "UserSetEmail.h"
    
        ```cpp
        #pragma once
    
        #include "cmd/ICmdInterface.h"
    
        class UserSetEmail : public ICmdInterface<UserSetEmail>
        {
            Q_GADGET
            $AsCmd(user)
        public:
            UserSetEmail();
    
            $CmdArgs(QString, email)
            $CmdArgsPostHandle(email, emailPostHandle)
            void emailPostHandle();
    
        public:
            $CmdMappingMemo(setEmail, "set email info")
            $CmdMapping(setEmail, email, set)
            void setEmail();
        };
        ```
    
    === "UserSetEmail.cpp"
    
        ```cpp
        #include "UserSetEmail.h"
        #include "core/util/IFileUtil.h"
        #include "data/Env.h"
    
        UserSetEmail::UserSetEmail()
        {
    
        }
    
        void UserSetEmail::emailPostHandle()
        {
            if(!Env::isValidEmail(email)){
                qDebug().noquote().nospace() << "email is not valid";
                quick_exit(1);
            }
        }
    
        void UserSetEmail::setEmail()
        {
            auto path = Env::instance().imakeRoot() + "/.data/.INFO";
            IJson json = IJson::object();
            if(QFileInfo(path).exists()){
                auto content = IFileUtil::readFileAsString2(path);
                if(IJson::accept(content.toStdString())){
                    json = IJson::parse(content.toStdString());
                }
            }
    
            json["email"] = email.toStdString();
            IFileUtil::writeToFile(path, QString::fromStdString(json.dump(4)));
            quick_exit(0);
        }
        ```
    
    [开始使用 →](ICmd/overview.md)
