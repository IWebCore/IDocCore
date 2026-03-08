# HTTPS

## Description

IHttpCore uses asio for network support, and asio has built-in SSL support for the TCP protocol. SSL has already been supported in IHttpCore.

In the current version, to start the HTTPS protocol, users need to perform the following steps when starting the httpserver:

---

## How to Do It

### Integrate OpenSSL into the Program

To use HTTPS, users need to install the OpenSSL library and import it into their project. Since the OpenSSL library is large and compiled versions are available online, IHttpCore does not provide it. Users need to install it themselves and import it into their project.

The following is the configuration I used during testing, based on qmake, written in the pro file. Users can use this as a reference; it is not provided uniformly.

=== "OpenSSL Package Configuration"
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

### Enable the ENABLE_SSL Macro

Note the first line in the code above: `DEFINES += ENABLE_SSL`. Users must enable this macro to use HTTPS. The purpose of the ENABLE_SSL macro is to activate SSL functionality.

### Modify the HTTP Server

Modify the usage of IHttpServer as follows:

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

The above code is what I used in my project; users can refer to it.

Note line 11: `server.setSslContext(sslContext);`. Users must set the initialized `sslContext` object into the server; otherwise, the server cannot provide SSL services properly.

---

## Summary

Thus, the HTTPS server has been successfully started.