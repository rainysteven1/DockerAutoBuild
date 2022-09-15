/*
 * @Author: Rainy
 * @Email: rainysteven1@gmail.com
 * @Date: 2022-09-15 11:35:20
 * @Project: DockerAutoBuild
 * @Description:
 */

// You may need to build the project (run Qt uic code generator) to get "ui_MainWindow.h" resolved

#include "mainwindow.h"
#include "form/ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent) :
	QWidget(parent), ui(new Ui::MainWindow) {
  ui->setupUi(this);
}

MainWindow::~MainWindow() {
  delete ui;
}
