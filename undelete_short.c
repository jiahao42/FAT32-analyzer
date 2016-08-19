#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
//#include <cstring>
//#include <iostream>
//#include <cstdio>

//argv[1] = path
//argv[2] = offset
int main(int argc,char* argv[]){
    //char* path = "/dev/sdb";
    if (argc < 3){
        printf("%s","Please input the path and offset\nThe Byte will be replaced by \"A\"\n");
        return 0;
    }
    char* path = argv[1];
    long offset = atoi(argv[2]);
	printf("%li",offset);
	undelete_for_short(path,offset);
}

int undelete_for_short(char* path,long offset){
	//char* device = "/dev/sdb";
	int fp = open(path,O_RDWR);//O_RDONLY //O_RDWR
	printf("%s\n",path);
	printf("%d\n",offset);
	char* a = "C";
	lseek(fp,offset,SEEK_SET);
	int b = write(fp,a,1);
	printf("%d\n",b);
	printf("%s\n","working");
	close(fp);
}