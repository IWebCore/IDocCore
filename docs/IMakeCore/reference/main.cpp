#include <core/application/IApplication.h>
#include <http/IHttpServer.h>
#include <http/IHttpAnnomacro.h>

$EnableHttpPrintTrace(true)
int main(int argc, char *argv[])
{
    IApplication a(argc, argv);

    IHttpServer server;
    server.listen();

    return a.exec();
}
