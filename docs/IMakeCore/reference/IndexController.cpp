#include "IndexController.h"

IndexController::IndexController()
{

}

QString IndexController::index()
{
    return "hello world";
}

QString IndexController::hello(std::string name)
{
    return "hello " + QString::fromStdString(name);
}

QString IndexController::welcome(QString $Query(name))
{
    return "welcome " + name;
}
