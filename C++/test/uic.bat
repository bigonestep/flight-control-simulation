echo off

rem 将子目录 QtApp 下的.ui文件复制到当前目录下，并且编译


gcc --shared -fpic -o getShareData.so getShareData.c

rem 编译并复制资源文件
