# FAT32-analyzer


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
	



```
                                                                            Created by James 
                                                                            
                                                                            2016.8.15-2016.8.20
```
