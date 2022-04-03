#!/usr/bin/env python
# coding=utf-8
from util import *
from analyze_mbr import *
from analyze_vbr import *
from analyze_root_directory import *
from recover_file import *
import global_var

import sys
import global_var


def show_help():
    print("\nUsage: ")
    print("\tpython fat32_analyzer.py [options] [argument]\n")

    print("Options: ")
    print('%-25s' % "-h, -- help", end=' ')
    print('%-40s' % "get help")

    print('%-25s' % "-s [sectors]", end=' ')
    print('%-40s' % "change the number of sectors that you want to read ")

    print('%-25s' % "-m [device]", end=' ')
    print('%-40s' % "analyze the MBR")

    print('%-25s' % "-v [device] [sectors]", end=' ')
    print('%-40s' % "analyze the VBR, MUST input the sectors to skip")

    # print '%-25s' % "-r [mbr] [reserved area] [fat] [start cluster] [sectors per cluster] [device], -- root directory"
    # print '%-40s' % "analyze the root directory"

    print('%-25s' % "-a [device] ", end=' ')
    print('%-40s' % "analyze things above")

    print('%-25s' % "-r [device] ", end=' ')
    print('%-40s' % "recover file as possible")


if len(sys.argv) == 1:
    sys.exit("Please input your argument !!! Type -h to get some help ")
elif sys.argv[1] == '-h':  # 获取帮助
    show_help()
elif sys.argv[1] == '-s':  # 改变读入扇区数目
    if len(sys.argv) == 2:
        sys.exit("Please input the sector number !!!")
    change_sectors(sys.argv[2])
    show_sectors()
elif sys.argv[1] == '-m':  # 找到并分析MBR
    if len(sys.argv) == 2:
        sys.exit("Please input your device name !!!")
    find_lba(sys.argv[2])
elif sys.argv[1] == '-v':  # 找到并分析VBR
    if len(sys.argv) == 2:
        sys.exit("Please input your device name !!!")
    elif len(sys.argv) == 3:
        sys.exit("Please input your sectors to skip !!!")
    device_name = sys.argv[2]
    filename = device_name + "_VBR"
    sectors_to_skip = sys.argv[3]
    analyze_vbr(sectors_to_skip, device_name, filename)
elif sys.argv[1] == '-a':  # 自动执行所有命令
    if len(sys.argv) == 2:
        sys.exit("Please input your device name !!!")
    device_name = sys.argv[2]
    find_lba(device_name)
    set_device_name(device_name)
    filename = device_name + "_VBR"
    # sectors_to_skip = raw_input("Please input the sectors to skip: ")
    # print "lba:",
    # print global_var.lba_address
	
    analyze_vbr(global_var.lba_address, device_name, filename)
    find_root_directory(global_var.lba_address, global_var.reserved_area, global_var.fat, global_var.start_cluster,
                        global_var.sectors_per_cluster, global_var.device_name)
elif sys.argv[1] == '-r':
    if len(sys.argv) == 2:
        sys.exit("Please input your device name !!!")
    device_name = sys.argv[2]
    find_lba(device_name)
    set_device_name(device_name)
    filename = device_name + "_VBR"
    # sectors_to_skip = raw_input("Please input the sectors to skip: ")
    analyze_vbr(global_var.lba_address, device_name, filename)
    print("\n**********************************************")
    print("Here is the Bytes which has been changed: ")
    recover_file(global_var.lba_address, global_var.reserved_area, global_var.fat, global_var.start_cluster,
                 global_var.sectors_per_cluster,
                 global_var.device_name)
else:
    show_help()
