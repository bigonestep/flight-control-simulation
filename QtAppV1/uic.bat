echo off

rem 将子目录 QtApp 下的.ui文件复制到当前目录下，并且编译

pyuic5 -o ui_MainRhapsody.py  MainRhapsody.ui

pyuic5 -o ui_MainWelcome.py  MainWelcome.ui
pyrcc5 res.qrc -o res_rc.py