# https

## 说明

IHttpCore 使用 asio 进行网络支持，asio tcp 协议内置 ssl 支持。再IHttpCore中已经对 ssl 进行了支持。

在目前的版本中，启动 https 协议需要个人在启动 httpserver 的时候做以下的内容：


## 如何做

### 将 openssl 集成进程序当中

使用 https， 用户需要安装 openssl 库, 并将库导入到项目中去。由于openssl 库比较大，而且网络上有编译好的版本，用户可以直接使用，所以在 IPubCore 中并没有提供该包，用户需要自己安装，并导入到项目中去。

如下是我在测试的时候使用的配置，基于 qmake， 写在 pro文件中。用户可以作为参考，这里不做统一提供。

=== "openssl 包配置"
    ```pro
    windows {
        DEFINES += ENABLE_SSL

        INCLUDEPATH += $$quote(C:/Program Files/OpenSSL-Win64/include)

        LIBS += -L"C:\Program Files\OpenSSL-Win64\lib\VC\x64\MD" -llibcrypto
        LIBS += -L"C:\Program Files\OpenSSL-Win64\lib\VC\x64\MD" -llibssl
    }

    unix {
        DEFINES += ENABLE_SSL
        
        OPENSSL_LIB_PATH = $$system(openssl version -d | awk '{print $$2}' | tr -d '"')
        isEmpty(OPENSSL_LIB_PATH) {
            OPENSSL_LIB_PATH = /usr/lib/x86_64-linux-gnu
        }

        LIBS += -L$${OPENSSL_LIB_PATH} -lssl -lcrypto
        LIBS += -lpthread

        QMAKE_LFLAGS += -Wl,--no-as-needed
    }
    ```

### 开启 ENABLE_SSL 宏

注意在上面的代码的第一行 `DEFINES += ENABLE_SSL`。用户必须开启这个宏，才能进行 https。ENABLE_SSL 宏的作用是开启 ssl 功能。

### 修改 httpserver

修改 IHttpServer 使用方式如下：

=== "main.cpp"
    ```cpp
    #ifdef ENABLE_SSL
    static int ocsp_callback(SSL* ssl, void* arg) {
        return 0;
    }
    #endif

    int main(int argc, char *argv[])
    {
        IApplication a(argc, argv);
        IHttpServer server;
        
    #ifdef ENABLE_SSL
        auto sslContext = new asio::ssl::context(asio::ssl::context::tls_server);

        sslContext->use_certificate_chain_file("./ssl/fullchain1.pem");
        sslContext->use_private_key_file("./ssl/privkey1.pem", asio::ssl::context::pem);
        sslContext->set_options(
            asio::ssl::context::default_workarounds |
            asio::ssl::context::no_sslv2 |
            asio::ssl::context::no_sslv3 |
            asio::ssl::context::no_tlsv1 |
            asio::ssl::context::no_tlsv1_1 |
            asio::ssl::context::single_dh_use);

        SSL_CTX_set_cipher_list(sslContext->native_handle(),
            "ECDHE-ECDSA-AES256-GCM-SHA384:"
            "ECDHE-RSA-AES256-GCM-SHA384:"
            "ECDHE-ECDSA-CHACHA20-POLY1305:"
            "ECDHE-RSA-CHACHA20-POLY1305:"
            "ECDHE-ECDSA-AES128-GCM-SHA256:"
            "ECDHE-RSA-AES128-GCM-SHA256");

        SSL_CTX_set_tlsext_status_type(sslContext->native_handle(), TLSEXT_STATUSTYPE_ocsp);
        SSL_CTX_set_tlsext_status_cb(sslContext->native_handle(), ocsp_callback);

        server.setSslContext(sslContext);
    #endif


        server.listen();
        return a.run();
    }
    ```

上述代码是我在项目中使用的代码，用户可以参考。

注意这里第11行，`server.setSslContext(sslContext);` 用户必须将初始化好的 sslContext 对象设置进 server 中，否则 server 无法正常提供 ssl 服务。

## 总结

经此，https 服务器已经启动起来了。
