#!/usr/bin/env python
# coding=utf-8
import commands
from util import *
from global_var import *
import sys

# mbr + reversed area = 6782    2 * FAT = 60802     mbr + reversed area + 2 * FAT = 67584


def analyze_vbr(sectors_to_skip, device_name, filename):
    result = commands.getstatusoutput(
        "dd if=/dev/" + device_name + " skip=" + str(sectors_to_skip) + " count=1 > " + filename)
    if result[0] != 0:
        sys.exit("Failed to execute !!! Please CHECK your input !!!")
    fp = open(filename, 'r')
    content = fp.read(512)
    fp.close()
    bytes_per_sector = []  # 11-12
    sectors_per_cluster = []  # 13-13
    size_in_sectors_reserved_area = []  # 14-15
    number_of_fats = []  # 16-16
    max_files_root_directory = []  # 17-18
    sectors_of_one_fat = []
    cluster_of_root_directory = []

    bytes_per_sector = get_certain_info(content, 11, 2, bytes_per_sector)
    sectors_per_cluster = get_certain_info(content, 13, 1, sectors_per_cluster)
    size_in_sectors_reserved_area = get_certain_info(content, 14, 2, size_in_sectors_reserved_area)
    number_of_fats = get_certain_info(content, 16, 1, number_of_fats)
    max_files_root_directory = get_certain_info(content, 17, 2, max_files_root_directory)
    sectors_of_one_fat = get_certain_info(content, 36, 4, sectors_of_one_fat)
    cluster_of_root_directory = get_certain_info(content, 44, 4, cluster_of_root_directory)

    print "**********************************************"
    print "Bytes per sector: "
    output_number(to_integer(little_endian(bytes_per_sector, 2), 2))
    print "Sector per cluster: "
    output_number(to_integer(little_endian(sectors_per_cluster, 1), 1))
    print "Size in sectors of reserved area: "
    output_number(to_integer(little_endian(size_in_sectors_reserved_area, 2), 2))
    set_reserved_area(size_in_sectors_reserved_area)
    print "Number of FATs: "
    output_number(to_integer(little_endian(number_of_fats, 1), 1))
    print "Sectors of one FAT area: "
    output_number(to_integer(little_endian(sectors_of_one_fat, 4), 4))
    set_fat(sectors_of_one_fat)
    print "Cluster where root directory can be found: "
    output_number(to_integer(little_endian(cluster_of_root_directory, 4), 4))
    set_start_cluster(cluster_of_root_directory)
    print "Maximum number of files in the root directory: "
    output_number(to_integer(little_endian(max_files_root_directory, 2), 2))
    print "**********************************************"


def little_endian(data, length):  # 转换成小端法表示
    for i in range(length / 2):
        data[i], data[-i - 1] = data[-i - 1], data[i]
    return data


if __name__ == '__main__':
    sectors = raw_input("Please input the sectors to skip: ")
    device = "sdb"
    filename = device + "_VBR"
    analyze_vbr(sectors, device, filename)
