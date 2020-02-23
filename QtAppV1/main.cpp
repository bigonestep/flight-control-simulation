#include "MainRhapsody.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainRhapsody w;
    w.show();
    return a.exec();
}
