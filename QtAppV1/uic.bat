echo off

rem ����Ŀ¼ QtApp �µ�.ui�ļ����Ƶ���ǰĿ¼�£����ұ���

pyuic5 -o ui_MainRhapsody.py  MainRhapsody.ui

pyuic5 -o ui_MainWelcome.py  MainWelcome.ui
pyrcc5 res.qrc -o res_rc.py