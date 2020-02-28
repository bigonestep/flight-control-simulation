echo
pyinstaller -F -w -i ./Icon6.ico ./myWidget.py ./myMainWindow.py ./ui_MainWelcome.py ./ui_MainRhapsody.py ./res_rc.py ./QMyLed.py  ./myFigureCanvas.py ./GetDataFromShareMem.py ./dataStack.py 


pyinstaller -F -w -i ./Icon6.ico ./myWidget.py ./myMainWindow.py ./ui_MainWelcome.py ./ui_MainRhapsody.py ./res_rc.py ./QMyLed.py ./myFigureCanvas.py ./GetDataFromShareMem.py ./dataStack.py ./buttonFunc.py updataQTread.py ./conf.py ledFunc.py 


Failed to decode wchar_t from UTF-8 MultiByteToWideChar:传递给系统调用的数