# FAT32-analyzer

##### 本工具用于分析FAT32文件系统，分析内容包括包括：
* MBR(Master Boot Record) - 使用-m参数
* VBR(Volumn Boot Record) - 使用-v参数 同时需要输入需跳过的扇区数 该项数据可以在-m指令中找到

-a选项可以同时分析MBR与VBR

##### 同时，本工具也可以用于FAT32设备的文件恢复工作，可以恢复最近删除的文件，参数为-r.

##### 请注意本工具的用法，本工具仅运行在Linux环境下：
* 1. 将需要分析或者恢复文件的设备通过USB口连接到主机
* 2. 除-s/-h参数选项外，使用其他选项运行时还需输入设备名称，设备名称请使用fdisk -l命令来查看。
* 3. 参见下方[Usage]

#### 请注意，恢复文件只能恢复文件内容，文件名无法完全恢复，且文件内容必须在Linux系统下查看。

### 关于FAT32文件系统的更多信息，请移步[Wiki](https://github.com/Jameeeees/FAT32-analyzer/wiki/FAT32-reference)。
---

	
### Usage: 
	python fat32_analyzer.py [options] [argument]
	

### Options: 
```
-h, -- help               get help                 

-s [sectors]              change the number of sectors that you want to read 

-m [device]               analyze the MBR                         

-v [device] [sectors]     analyze the VBR, MUST input the sectors to skip

-a [device]               analyze things above                    

-r [device]               recover file as possible       
```


### Example:
* on Linux:
	* just type in the terminal ```python fat32_analyzer.py -r sdb```.
	* then you can recover the files that recently deleted on sdb.
	* As for the device name, you can use the ``` fdisk -l ```command to see.

#### Attention:
* This tool can only run on Linux.
* This tool can only undelete the files that are RECENTLY DELETED.You can find the completed content of the undeleted files on Linux,but the undeleted files'names might be a little different.

### If you want to know more about FAT32 file system,please go to [Wiki](https://github.com/Jameeeees/FAT32-analyzer/wiki/FAT32-reference).

```
                                                                            Created by James 
                                                                            
                                                                            2016.8.15-2016.8.20
```

![How to use it to analyze MBR?](https://raw.githubusercontent.com/Jameeeees/FAT32-analyzer/master/images/1.PNG)
![How to use it to analyze VBR?](https://raw.githubusercontent.com/Jameeeees/FAT32-analyzer/master/images/2.PNG)
![File analyzation](https://raw.githubusercontent.com/Jameeeees/FAT32-analyzer/master/images/4.PNG)


![How to read long file name?](https://raw.githubusercontent.com/Jameeeees/FAT32-analyzer/master/images/how-to-read-long-file-name.PNG)
![How to recover files?](https://raw.githubusercontent.com/Jameeeees/FAT32-analyzer/master/images/how-to-recover-files.PNG)
![How to decode date?](https://raw.githubusercontent.com/Jameeeees/FAT32-analyzer/master/images/how-to-decode-date.PNG)