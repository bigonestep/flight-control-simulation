#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#define GETSIZE 30
LPVOID lpbase = NULL;
HANDLE hmapfile = NULL;

double* lpData;     
int i;


       


//��¼����ʹ��
char getMem(char* str) {
	int i;
	int ret = 0;
	hmapfile = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE | SEC_COMMIT, 0, 1024, str);
	if (hmapfile == NULL)
	{
		ret = -1;
		return ret;
	}
	//����ָ�룬ָ����Ƭ�ڴ�
	lpbase = MapViewOfFile(hmapfile, FILE_MAP_ALL_ACCESS, 0, 0, 1024);
	if (lpbase == NULL)
	{
		ret = -2;    // �������
		CloseHandle(hmapfile);
		return ret;
	}
	return 0;
}

int closeMem()
{
	if (lpbase != NULL) {
		UnmapViewOfFile(lpbase);//���
	}
	else if (hmapfile != NULL)
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
double writeData(int num, double f)
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
			return f;
		}
		else
		{
			return -1;
		}
	}
}



// int main()
// {
// 	int ret = 0;
// 	double j = 0;
// 	double w = 0;
// 	int i = 0;
// 	char* str = "szName";

// 	double getdata[GETSIZE];
// 	double writeNum[GETSIZE];


// 	while (1) {
// 		ret = getMem(str);
// 		if (ret == -1)
// 		{
// 			printf("�����ڴ��ʧ�ܣ�����\n");
// 		}
// 		else if (ret == -2) {
// 			printf("�����ڴ�ָ��ʧ�ܣ�����\n");
// 			return ret;
// 		}
// 		else if (ret == 0) {
// 			for (i = 0; i < 4; i++)
// 			{
// 				w = writeData(i, j + i);
// 				if (w - (-1)>0.001)
// 				{
// 					printf("%.2lf,     ", w);
// 				}
// 			}

// 			j++;
// 			printf("%.2lf,     ", writeData(7, 1.0)); ;
// 			printf("\n");

// 		}

// 	}
// 	return ret;

// }