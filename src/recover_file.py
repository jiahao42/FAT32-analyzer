#!/usr/bin/env python
# coding=utf-8
import commands
from util import *
import sys


def recover_file(mbr, reserved_area, fat, start_cluster, sectors_per_cluster, device_name):
    root_directory = int(mbr) + int(reserved_area) + 2 * int(fat) + (int(start_cluster) - 2) * int(sectors_per_cluster)
    filename = device_name + "_root_directory"
    result = commands.getstatusoutput(
        "dd if=/dev/" + device_name + " skip=" + str(root_directory) + " count=" + str(get_sectors()) + ">" + filename)
    if result[0] != 0:
        sys.exit("WRONG device name !!! Please CHECK your input !!!")
    fp = open(filename, 'rb')
    sum_bytes = 512 * get_sectors()  # 读入的sector数是由使用者自行决定的 通过读配置文件得到
    accumulation = 0
    # 注意 python的read()方法 自动记录当前读到的位置
    # 先读入一行(32bytes) 若第0x0b个字节不是0x0f 则为短文件 读出文件名+拓展名 创建时间 最近访问日期 文件大小
    # 若这个字节是0x0f 则为长文件 通过判断第一个字节的大小来决定还需读入几行数据(-0x40)
    # 注意短文件名用ascii编码 长文件名用unicode编码
    while True:
        temp = fp.read(32)
        accumulation += 32  # 每个循环结束后都再读下一个文件的前32个字节作为判断用
        if is_short(temp):  # 是短文件名
            if is_delete(temp):
                is_done(accumulation, sum_bytes)
                print "Start to recover a file...: "
                offset = root_directory * 512 + accumulation - 32  # + accumulation - 64
                path = "/dev/" + device_name
                result = commands.getstatusoutput("./undelete_short " + path + " " + str(offset))
                if result[0] != 0:
                    sys.exit("Failed to execute !!! check your PATH please !!!")
                print "A Byte has been changed !!!" + "  offset: " + str(offset)
            else:
                is_done(accumulation, sum_bytes)
        else:  # 是长文件名 长文件需要再读 n * 32Bytes 数据
            if is_delete(temp):
                is_done(accumulation, sum_bytes)
                print "Start to recover a file...: "
                offset = root_directory * 512 + accumulation - 32
                important_offset = offset       # 第一行的第一个字节的偏移量 代表行数 重要
                path = "/dev/" + device_name
                one_more_line = fp.read(32)  # 一直向下读32个字节 直到第0xb个字节为0x10 或 0x20为止
                accumulation += 32
                temp += one_more_line  # 因为长文件至少占两行 所以直接向下读一行作为判断无风险
                offset = root_directory * 512 + accumulation - 32  # 第二行的偏移量
                result = commands.getstatusoutput("./undelete_long " + path + " " + str(offset) + " V")
                if result[0] != 0:
                    sys.exit("Failed to execute !!! check your PATH please !!!")
                print "A Byte has been changed !!!" + "  offset: " + str(offset)
                while recover_long_file_is_end(one_more_line):
                    one_more_line = fp.read(32)
                    accumulation += 32
                    offset = root_directory * 512 + accumulation - 32
                    result = commands.getstatusoutput("./undelete_long " + path + " " + str(offset) + " V")
                    if result[0] != 0:
                        sys.exit("Failed to execute !!! check your PATH please !!!")
                    print "A Byte has been changed !!!" + "  offset: " + str(offset)
                    temp += one_more_line
                final_lines = len(temp) / 32       # 最后再填写第一行的数据 因为要表示该长文件共占几行
                signal = chr(0x3f + final_lines)
                result = commands.getstatusoutput(
                    "./undelete_long " + path + " " + str(important_offset) + " " + signal)
                if result[0] != 0:
                    sys.exit("Failed to execute !!! check your PATH please !!!")
                print "A Byte has been changed !!!" + "  offset: " + str(offset)
            else:
                lines = ord(temp[0]) - 0x40  # 需要再读的行数
                fp.read(lines * 32)  # 文件所有的信息都在此
                accumulation += lines * 32
