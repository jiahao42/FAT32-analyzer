#!/usr/bin/env python
# coding=utf-8


device_name = ""
lba_address = 0
reserved_area = 0
fat = 0
start_cluster = 0
sectors_per_cluster = 0


def set_device_name(data):
    global device_name
    device_name = data
    # print device_name


def set_lba_address(data):
    global lba_address
    lba_address = data[3] + data[2] * 0x100 + data[1] * 0x10000 + data[0] * 0x1000000
    # print lba_address


def set_reserved_area(data):
    global reserved_area
    # print data
    reserved_area = data[0] * 0x100 + data[1]
    # print "reserved: "
    # print reserved_area


def set_fat(data):
    global fat
    fat = data[3] + data[2] * 0x100 + data[1] * 0x10000 + data[0] * 0x1000000
    # print fat


def set_start_cluster(data):
    global start_cluster
    start_cluster = data[3] + data[2] * 0x100 + data[1] * 0x10000 + data[0] * 0x1000000
    # print "start: "
    # print start_cluster


def set_sectors_per_cluster(data):
    global sectors_per_cluster
    sectors_per_cluster = data
    print sectors_per_cluster
