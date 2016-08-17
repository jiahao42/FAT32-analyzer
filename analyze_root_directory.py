#!/usr/bin/env python
# coding=utf-8
import commands
from util import *
import sys


def find_root_directory(mbr, reserved_area, fat, start_cluster, sectors_per_cluster, device_name):
    root_directory = int(mbr) + int(reserved_area) + 2 * int(fat) + (int(start_cluster) - 2) * int(sectors_per_cluster)
    filename = device_name + "_root_directory"
    print "dd if=/dev/" + device_name + " skip=" + str(root_directory) + " count=" + str(get_sectors()) + ">" + filename
    result = commands.getstatusoutput(
        "dd if=/dev/" + device_name + " skip=" + str(root_directory) + " count=" + str(get_sectors()) + ">" + filename)
    if result[0] != 0:
        print "something is WRONG !!! Please CHECK your input !!!"
        return
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
                # temp = fp.read(32)
                # accumulation += 32
            else:
                lines = ord(temp[0]) - 0x40  # 需要再读的行数
                temp += fp.read(lines * 32)  # 文件所有的信息都在此
                analyze_long_file(temp, file_info, lines)
                accumulation += lines * 32
                for i in file_info:
                    del i[:]
                is_done(accumulation, sum_bytes)
                # temp = fp.read(32)
                # accumulation += 32


def analyze_long_file(data, file_info, lines):
    file_name = []
    for i in range(lines):  # 需要倒序读取各行数据
        file_name = get_certain_info(data, 32 * (lines - i - 1) + 1, 10, file_name)
        file_name = get_certain_info(data, 32 * (lines - i - 1) + 14, 12, file_name)
        file_name = get_certain_info(data, 32 * (lines - i - 1) + 28, 4, file_name)
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
    for i in range(len(file_info[0])):
        if ord(file_info[0][i]) == 0x20:
            file_info[0][i] = chr(0x2e)
            break
    file_info[0] = filter(lambda x: ord(x) != 0x20, file_info[0])
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


def is_short(data):  # 是否是短文件名
    if ord(data[11]) == 0x0f:
        return False
    return True


def is_delete(data):  # 是否是被删除文件
    # print "is deleted: ",
    if ord(data[0]) == 0x00 or ord(data[0]) == 0xe5:
        return True
    return False


def is_done(accumulation, sum_bytes):
    if accumulation >= sum_bytes:  # 若读取的字节到达了配置文件中的要求 则直接退出
        sys.exit(
            "\nThis is all the file information. "
            "If you want more, maybe you can change the sectors using \"-s\" \n\tBye~")


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
