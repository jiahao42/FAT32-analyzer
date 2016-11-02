#!/usr/bin/env python
# coding=utf-8
import os
import commands
from util import *
from global_var import *
import sys


def find_lba(device_name):
    # device_name = raw_input("please input your device name: \n")
    filename = device_name + "_MBR"
    # os.system("dd if=/dev/" + device_name + " count=1 > " + filename)
    # 下面通过getstatusoutput方法来获取shell命令的返回值 若没有返回成功 则打印错误信息并退出
    result = commands.getstatusoutput("dd if=/dev/" + device_name + " count=1 > " + filename)
    if result[0] != 0:
        sys.exit("WRONG device name !!! Please CHECK your input !!!")
    fp = open(filename, "r")
    content = fp.read(512)
    fp.close()
    # print content
    signature_value = []
    partition1 = []
    partition2 = []
    partition3 = []
    partition4 = []
    partition1 = find_partition(content, 446, partition1)  # 下面三个分区可以依据情况优化
    partition2 = find_partition(content, 462, partition2)
    partition3 = find_partition(content, 478, partition3)
    partition4 = find_partition(content, 494, partition4)
    signature_value = get_signature_value(content, signature_value)
    print "\n**********************************************"
    print "/////Here is the info of partition 1" + "\\\\\\\\\\"
    print "**********************************************"
    if check_if_continue(partition1):
        analyze_partition(partition1)
    else:
        print "Something is WRONG !!! Please check if you input the right device name !!!"
    print "\n**********************************************"
    print "/////Here is the info of partition 2" + "\\\\\\\\\\"
    print "**********************************************"
    if check_if_continue(partition2):
        analyze_partition(partition2)
    else:
        print "Partition 2 NOT EXIST!!!!!!"
    print "\n**********************************************"
    print "/////Here is the info of partition 3" + "\\\\\\\\\\"
    print "**********************************************"
    if check_if_continue(partition3):
        analyze_partition(partition3)
    else:
        print "Partition 3 NOT EXIST!!!!!!"
    print "\n**********************************************"
    print "/////Here is the info of partition 4" + "\\\\\\\\\\"
    print "**********************************************"
    if check_if_continue(partition4):
        analyze_partition(partition4)
    else:
        print "Partition 4 NOT EXIST!!!!!!"


def find_partition(content, start, partition):  # 找到各自的分区数据
    for i in range(16):
        partition.append(content[start + i])
    return partition


def get_signature_value(content, temp):  # 找到扇区结束符
    temp.append(content[510])
    temp.append(content[511])
    return temp


def analyze_partition(partition):
    start_chs_address = []
    start_chs_address = get_certain_info(partition, 1, 3, start_chs_address)
    print "Starting CHS Address: "
    # print to_integer(little_endian(start_chs_address, 3), 3)
    output_number(to_integer(little_endian(start_chs_address, 3), 3))
    partition_type = []
    partition_type = get_certain_info(partition, 4, 1, partition_type)
    print "Partition Type: "
    output_number(to_integer(little_endian(partition_type, 1), 1))
    end_chs_address = []
    end_chs_address = get_certain_info(partition, 5, 3, end_chs_address)
    print "Ending CHS Address: "
    output_number(to_integer(little_endian(end_chs_address, 3), 3))
    start_lba_address = []
    start_lba_address = get_certain_info(partition, 8, 4, start_lba_address)
    print "Starting LBA Address: "
    output_number(to_integer(little_endian(start_lba_address, 4), 4))
    set_lba_address(start_lba_address)  # 将lba地址保存至全局变量
    size_in_sectors = []
    size_in_sectors = get_certain_info(partition, 12, 4, size_in_sectors)
    print "Size in Sectors: "
    output_number(to_integer(little_endian(size_in_sectors, 4), 4))


def check_if_continue(partition):  # 控制是否要继续查找下一个分区表
    for i in range(16):
        if partition[i] != '\x00':  # 只要分区表中有一个数字不为0则继续查找
            return True
    return False


if __name__ == '__main__':
    device_name = raw_input("please input your device name: \n")
    find_lba(device_name)
