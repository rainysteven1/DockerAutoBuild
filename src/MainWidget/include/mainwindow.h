/*
 * @Author: Rainy
 * @Email: rainysteven1@gmail.com
 * @Date: 2022-09-15 11:35:20
 * @Project: DockerAutoBuild
 * @Description:
 */

#ifndef DOCKERAUTOBUILD_SRC_MAINWIDGET_MAINWINDOW_H_
#define DOCKERAUTOBUILD_SRC_MAINWIDGET_MAINWINDOW_H_

#include <QWidget>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QWidget {
 Q_OBJECT

 public:
  explicit MainWindow(QWidget *parent = nullptr);
  ~MainWindow() override;

 private:
  Ui::MainWindow *ui;
};

#endif //DOCKERAUTOBUILD_SRC_MAINWIDGET_MAINWINDOW_H_
