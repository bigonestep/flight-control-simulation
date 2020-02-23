#ifndef MAINRHAPSODY_H
#define MAINRHAPSODY_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainRhapsody; }
QT_END_NAMESPACE

class MainRhapsody : public QMainWindow
{
    Q_OBJECT

public:
    MainRhapsody(QWidget *parent = nullptr);
    ~MainRhapsody();

private slots:
    void on_takeOffButton_clicked();

    void on_programmedControlButton_clicked(bool checked);

private:
    Ui::MainRhapsody *ui;
};
#endif // MAINRHAPSODY_H
