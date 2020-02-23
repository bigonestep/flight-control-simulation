#include<stdio.h>
#include<stdlib.h>
#include<Windows.h>
#include<conio.h>
#pragma warning(disable: 4996)
#define GETSIZE 15
LPVOID lpbase = NULL;
HANDLE hmapfile = NULL;

//记录可以使用
char getMem(void) {
	int i;
	int ret = 0;
	hmapfile = OpenFileMappingA(FILE_MAP_ALL_ACCESS, FALSE, "szName");
	if (hmapfile == NULL)
	{
		ret = -1;
		return ret;
	}
	//创建指针，指向这片内存
	lpbase = MapViewOfFile(hmapfile, FILE_MAP_ALL_ACCESS, 0, 0, GETSIZE*8);
	if (lpbase == NULL)
	{

		ret = -2;    // 错误代码
		CloseHandle(hmapfile);
		return ret;
		

	}
	return 0;
}

int closeMem()
{
	if (lpbase != NULL) {
		UnmapViewOfFile(lpbase);//解除
	}
	if (hmapfile != NULL)
	{
		CloseHandle(hmapfile);
	}
}

double* readAllParam()
{
	double* p = lpbase;
	return p;
}



double readData(int num)
{
	double* p = lpbase;
	if (num < 0 && num >= GETSIZE)
	{
		
		return -1;
	}
	else {
		return p[num];
	}
}
int  writeData(int num, double f)
{
	if (num < 0 && num >= GETSIZE)
	{
		return -1;    
	}
	else {
		if (lpbase != NULL)
		{
			double r = f;
			double* p = lpbase;
			memcpy(p+num, &r, 8);
			return 0;
		}
		else
		{
			return -2;
		}
	}
}




