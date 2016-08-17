#!/usr/bin/env python
# coding=utf-8
import simplejson


def to_integer(data, length):  # 转换成ascii码的码值
    # print data
    for i in range(length):
        data[i] = ord(data[i])
    return data


def output_number(data):  # 以hex输出
    output = "\t0x"
    for i in data:
        output += '%02x' % i  # 格式化输出 不足的地方在前面用0补齐
    print output


def output_char(data):
    output = ""
    for i in data:
        output += chr(i)
    print output


def get_certain_info(data, start, length, address):  # 获取一段数据中特定几个字节的信息
    for i in range(length):
        address.append(data[start + i])
    # print "this is the certain info: "
    # print address
    return address


def little_endian(data, length):  # 转换成小端法表示
    for i in range(length / 2):
        data[i], data[-i - 1] = data[-i - 1], data[i]
    return data


def change_sectors(sectors):  # 修改默认读入的sector数 通过 -s 选项修改
    fp = open("setting", 'w')
    temp = "\"sectors\":" + sectors + ' '  # 字符串的拼接
    fp.write(temp)
    fp.close()


def get_sectors():     # 读取文件的配置信息 读入的sector数
    fp = open("setting", 'r')
    content = fp.read()
    temp = '{' + content + '}'
    # print temp
    temp_dict = simplejson.loads(str(temp))
    # print temp_dict["sectors"]
    return temp_dict["sectors"]


def show_sectors():     # 读取文件的配置信息 读入的sector数
    fp = open("setting", 'r')
    content = fp.read()
    temp = '{' + content + '}'
    temp_dict = simplejson.loads(str(temp))
    print "Now the sectors to read is: ",
    print temp_dict["sectors"]


def analyze_date(data):
    date_number = data[0] * 0x100 + data[1]
    year = date_number >> 9
    month = (date_number & 0b0000000111100000) >> 5
    day = (date_number & 0b0000000000011111)
    date_sum = [year,month,day]
    return date_sum


def output_date(date):
    print date[0] + 1980,
    print '\\',
    print date[1],
    print '\\',
    print date[2]


def output_file_size(size):
    file_size = size[0] * 0x1000000 + size[1] * 0x10000 + size[2] * 0x100 + size[3]
    if file_size > 1048546:
        file_size /= 1048546
        print file_size,
        print "MegaBytes\n"
    elif file_size > 10240:
        file_size /= 1024
        print file_size,
        print "KiloBytes\n"
    else:
        print file_size,
        print "Bytes\n"


if __name__ == '__main__':
    sectors = raw_input("Please input the number of sectors that you want to read: ")
    change_sectors(sectors)
    show_sectors()








