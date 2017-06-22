#!/usr/bin/env python
# coding=utf-8
import commands
from util import *
import sys
import ctypes

# undelete_lib = ctypes.CDLL('/mnt/hgfs/For-Linux/digital_forensics/undelete_lib.so')


def find_root_directory(mbr, reserved_area, fat, start_cluster, sectors_per_cluster, device_name):
    root_directory = int(mbr) + int(reserved_area) + 2 * int(fat) + (int(start_cluster) - 2) * int(sectors_per_cluster)
    filename = device_name + "_root_directory"
    # print "dd if=/dev/" + device_name + " skip=" + str(root_directory)
    # + " count=" + str(get_sectors()) + ">" + filename
    print str(root_directory)
    result = commands.getstatusoutput(
        "dd if=/dev/" + device_name + " skip=" + str(root_directory) + " count=" + str(get_sectors()) + ">" + filename)
    if result[0] != 0:
        sys.exit("Failed to execute !!! Please CHECK your input !!!")
    recover_name = []  # 0-11
    create_day = []  # 16-17
    access_day = []  # 18-19
    high_two_bytes = []  # 20-21
    low_two_bytes = []  # 26-27
    file_size = []  # 28-31
    file_info = [recover_name, create_day, access_day, high_two_bytes, low_two_bytes, file_size]
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
                pass
                # temp = fp.read(32)
                # accumulation += 32
            else:
                analyze_short_file(temp, file_info)
                for i in file_info:
                    del i[:]
                is_done(accumulation, sum_bytes)
                # temp = fp.read(32)
                # accumulation += 32
                # print "if: ",
                # print fp.tell()
        else:  # 是长文件名 长文件需要再读 n * 32Bytes 数据
            if is_delete(temp):
                is_done(accumulation, sum_bytes)
                one_more_line = fp.read(32)  # 一直向下读32个字节 直到第0xb个字节为0x10 或 0x20为止
                accumulation += 32
                temp += one_more_line  # 因为长文件至少占两行 所以直接向下读一行作为判断无风险
                while recover_long_file_is_end(one_more_line):
                    one_more_line = fp.read(32)
                    accumulation += 32
                    temp += one_more_line
                    # temp = fp.read(32)
                    # accumulation += 32
            else:
                lines = ord(temp[0]) - 0x40  # 需要再读的行数
                try:
                    temp += fp.read(lines * 32)  # 文件所有的信息都在此
                except IndexError:
                    sys.exit(
                        "\nThis is all the file information.\n"
                        "If you want more,\n maybe you can change the sectors using \"-s\" \n\tBye~")
                analyze_long_file(temp, file_info, lines)
                accumulation += lines * 32
                for i in file_info:
                    del i[:]
                is_done(accumulation, sum_bytes)
                # temp = fp.read(32)
                # accumulation += 32


def analyze_long_file(data, file_info, lines):
    file_name = []
    try:
        for i in range(lines):  # 需要倒序读取各行数据
            file_name = get_certain_info(data, 32 * (lines - i - 1) + 1, 10, file_name)
            file_name = get_certain_info(data, 32 * (lines - i - 1) + 14, 12, file_name)
            file_name = get_certain_info(data, 32 * (lines - i - 1) + 28, 4, file_name)
    except IndexError:
        sys.exit(
            "\nThis is all the file information.\n"
            "If you want more,\n maybe you can change the sectors using \"-s\" \n\tBye~")
    file_name = filter(lambda x: x != '\x00', file_name)
    file_name = filter(lambda x: x != '\xff', file_name)
    print "Filename: ",
    output_char(to_integer(file_name, len(file_name)))
    long_file_info = []
    for i in range(32):
        long_file_info.append(data[32 * lines + i])
    analyze_last_line_of_long_file(long_file_info)


def analyze_short_file(data, file_info):
    file_info[0] = get_certain_info(data, 0, 12, file_info[0])
    file_info[1] = get_certain_info(data, 16, 2, file_info[1])
    file_info[2] = get_certain_info(data, 18, 2, file_info[2])
    file_info[3] = get_certain_info(data, 20, 2, file_info[3])
    file_info[4] = get_certain_info(data, 26, 2, file_info[4])
    file_info[5] = get_certain_info(data, 28, 4, file_info[5])
    full_name = True       # 如果文件名恰好八个字节则没有空格 下面方法不适用 直接在第八个字节后加.
    for i in range(8):
        if ord(file_info[0][i]) == 0x20:
            full_name = False       # 前八个字节里有一个空格的话就不是 Full name
    if full_name:
        file_info[0].insert(8,'.')
    else:
        for i in range(len(file_info[0])):      # 将其中一个空格替换成点
            if ord(file_info[0][i]) == 0x20:
                file_info[0][i] = chr(0x2e)
                break
    file_info[0] = filter(lambda x: ord(x) != 0x20, file_info[0])       # 去除剩余空格
    print "Filename: ",
    output_char(to_integer(file_info[0], len(file_info[0])))
    print "Create Day: ",
    output_date(analyze_date(to_integer(little_endian(file_info[1], 2), 2)))
    # output_number(to_integer(little_endian(file_info[1], 2), 2))
    print "Access Day: ",
    output_date(analyze_date(to_integer(little_endian(file_info[2], 2), 2)))
    # output_number(to_integer(little_endian(file_info[2], 2), 2))
    print "High two bytes: ",
    output_number(to_integer(little_endian(file_info[3], 2), 2))
    print "Low two bytes: ",
    output_number(to_integer(little_endian(file_info[4], 2), 2))
    print "File Size: ",
    output_file_size(to_integer(little_endian(file_info[5], 4), 4))
    # output_number(to_integer(little_endian(file_info[5], 4), 4))


def analyze_last_line_of_long_file(data):
    create_day = []  # 16-17
    access_day = []  # 18-19
    high_two_bytes = []  # 20-21
    low_two_bytes = []  # 26-27
    file_size = []  # 28-31
    file_info = [create_day, access_day, high_two_bytes, low_two_bytes, file_size]
    # file_info[0] = get_certain_info(data, 0, 12, file_info[0])
    file_info[0] = get_certain_info(data, 16, 2, file_info[0])
    file_info[1] = get_certain_info(data, 18, 2, file_info[1])
    file_info[2] = get_certain_info(data, 20, 2, file_info[2])
    file_info[3] = get_certain_info(data, 26, 2, file_info[3])
    file_info[4] = get_certain_info(data, 28, 4, file_info[4])
    print "Create Day: ",
    output_date(analyze_date(to_integer(little_endian(file_info[0], 2), 2)))
    # output_number(to_integer(little_endian(file_info[1], 2), 2))
    print "Access Day: ",
    output_date(analyze_date(to_integer(little_endian(file_info[1], 2), 2)))
    # output_number(to_integer(little_endian(file_info[2], 2), 2))
    print "High two bytes: ",
    output_number(to_integer(little_endian(file_info[2], 2), 2))
    print "Low two bytes: ",
    output_number(to_integer(little_endian(file_info[3], 2), 2))
    print "File Size: ",
    output_file_size(to_integer(little_endian(file_info[4], 4), 4))
    # output_number(to_integer(little_endian(file_info[5], 4), 4))
