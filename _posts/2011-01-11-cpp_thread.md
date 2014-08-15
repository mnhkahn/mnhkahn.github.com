---
layout: post
title: "在main函数中创建2个线程，一个运行冒泡排序算法，另一个运行选择排序算法，分别对两个一样的数组进行"
description: "操作系统作业。"
category: "computer science"
tags: ["Computer Science", "Operating System", "Windows"]
---

	#include<Windows.h>
	#include<iostream>
	#include<stdlib.h>
	#include<strsafe.h>
	#include<time.h>
	 
	#defineMAX_THREADS 2
	#defineDATASIZE 100000
	usingnamespacestd;
	 
	voidErrorHandler(LPTSTRlpszFunction);
	DWORDWINAPIBubble( LPVOIDlpParam);
	DWORDWINAPISelectSort(LPVOIDlpParam); 
	 
	DWORDtime1 = 0, time2= 0;
	 
	typedefstructMyData {
	        intvar[DATASIZE];
	} MYDATA,*PMYDATA;
	 
	int main()
	{
	    DWORD   dwThreadIdArray[MAX_THREADS];
	    HANDLE  hThreadArray[MAX_THREADS];
	    PMYDATApDataArray[MAX_THREADS];
	
	    for (inti = 0; i < MAX_THREADS; i++)
	    {
	            pDataArray[i] =(PMYDATA) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY,
	                    sizeof(MYDATA));
	
	            if( pDataArray[i] == NULL )
	            {
	                    ExitProcess(2);
	            }
	    }
	    srand((unsignedint)time(NULL));
	    for (intj = 0; j < DATASIZE; j++)
	    {
	            pDataArray[0]->var[j] = pDataArray[1]->var[j] = rand();
	    }
	
	    hThreadArray[0] = CreateThread(
	            NULL,
	            0,
	            Bubble,
	            pDataArray[0],
	            0,
	            &dwThreadIdArray[0]);
	
	    if (hThreadArray[0]== NULL) 
	    {
	            ErrorHandler(TEXT("CreateThread"));
	            ExitProcess(3);
	    }
	
	    hThreadArray[1] = CreateThread(
	            NULL,
	            0,
	            SelectSort,
	            pDataArray[1],
	            0,
	            &dwThreadIdArray[1]);
	
	    if (hThreadArray[1]== NULL) 
	    {
	            ErrorHandler(TEXT("CreateThread"));
	            ExitProcess(3);
	    }
	    
	    WaitForMultipleObjects(MAX_THREADS,hThreadArray, TRUE,INFINITE);
	
	    for(inti=0; i<MAX_THREADS; i++)
	    {
	            CloseHandle(hThreadArray[i]);
	    }
	
	    return 0;
	}
	 
	voidErrorHandler(LPTSTRlpszFunction) 
	{ 
	    // Retrieve the system error message for the last-errorcode.
	
	    LPVOIDlpMsgBuf;
	    LPVOIDlpDisplayBuf;
	    DWORDdw = GetLastError(); 
	
	    FormatMessage(
	            FORMAT_MESSAGE_ALLOCATE_BUFFER | 
	            FORMAT_MESSAGE_FROM_SYSTEM |
	            FORMAT_MESSAGE_IGNORE_INSERTS,
	            NULL,
	            dw,
	            MAKELANGID(LANG_NEUTRAL,SUBLANG_DEFAULT),
	            (LPTSTR) &lpMsgBuf,
	            0,NULL );
	
	    // Display the error message.
	
	    lpDisplayBuf = (LPVOID)LocalAlloc(LMEM_ZEROINIT,
	            (lstrlen((LPCTSTR)lpMsgBuf)+lstrlen((LPCTSTR)lpszFunction)+40)*sizeof(TCHAR)); 
	    StringCchPrintf((LPTSTR)lpDisplayBuf, 
	            LocalSize(lpDisplayBuf)/ sizeof(TCHAR),
	            TEXT("%s failedwith error %d: %s"), 
	            lpszFunction, dw,lpMsgBuf); 
	    MessageBox(NULL,(LPCTSTR)lpDisplayBuf,TEXT("Error"),MB_OK); 
	
	    // Free the error-handling buffer allocations.
	
	    LocalFree(lpMsgBuf);
	    LocalFree(lpDisplayBuf);
	}
	 
	DWORDWINAPIBubble( LPVOIDlpParam) 
	{
	    time1 = GetTickCount();
	    int *p = (int*)lpParam;
	    inttemp;
	    for(inti=DATASIZE - 1;i > 0; i--)
	    {
	            for(intj = 0; j < i; j++)
	            {
	                    if(p[j] > p[j + 1])
	                    {
	                            temp=p[j];
	                            p[j]=p[j + 1];
	                            p[j + 1]=temp;
	                    }
	            }
	    }
	    time2 = GetTickCount();
	    cout << "Timeof Bubble:" << time2 - time1 << "ms"<< endl;
	    return 0;
	}
	 
	DWORDWINAPISelectSort(LPVOIDlpParam) 
	{
	    time1 = GetTickCount();
	    int *p = (int*)lpParam;
	    intpos;
	    inttemp;
	    for (inti = 0; i < DATASIZE; i++)
	    {
	            pos = i;
	            for (intj = i; j < DATASIZE;j++)
	            {
	                    if (p[pos] > p[j])
	                    {
	                            pos = j;
	                    }
	            }
	            temp = p[pos];
	            p[pos] = p[i];
	            p[i] = temp;
	    }
	    time2 = GetTickCount();
	    cout << "Timeof SelectSort:" << time2 -time1 << "ms"<< endl;
	    return 0;
	}

计算结果：

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/64dadbf99418bf16242df233.jpg)

在main函数中加入

	SetThreadPriority(hThreadArray[0], THREAD_PRIORITY_HIGHEST);
    SetThreadPriority(hThreadArray[1], THREAD_PRIORITY_LOWEST);

修改两个线程的优先级，得到的结果：

![IMG-THUMBNAIL](http://cyeam.qiniudn.com/a208a344cc0786cdb3b7dc3c.jpg)


{% include JB/setup %}