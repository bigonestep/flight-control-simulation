#include "MainRhapsody.h"
#include "ui_MainRhapsody.h"

MainRhapsody::MainRhapsody(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainRhapsody)
{
    ui->setupUi(this);
}

MainRhapsody::~MainRhapsody()
{
    delete ui;
}


void MainRhapsody::on_takeOffButton_clicked()
{

}

void MainRhapsody::on_programmedControlButton_clicked(bool checked)
{

}
