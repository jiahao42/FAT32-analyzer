#!/usr/bin/env python
# coding=utf-8


device_name = ""
lba_address = 0


def set_device_name(data):
    global device_name
    device_name = data


def set_lba_address(data):
    global lba_address
    lba_address = data[3] + data[2] * 0x100 + data[1] * 0x10000 + data[0] * 0x1000000
