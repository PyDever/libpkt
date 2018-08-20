
"""
list and view interfaces
"""

import socket # for network stuff
import random # building packets
import struct # for packing headers

import fcntl, array, time


def l (): 
    max_possible = 128
    bytes = max_possible * 32 

    my_socket = socket.socket(socket.AF_INET,
        socket.SOCK_DGRAM)

    names = array.array('B', '\0' * bytes)

    outbytes = struct.unpack('iL', fcntl.ioctl(
        my_socket.fileno(),

        0x8912, # SIOCGIFCONF

        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]

    namestr = names.tostring()
    lst = []

    for i in range(0, outbytes, 40):

        name = namestr[i:i+16].split('\0', 1)[0]
        ip   = namestr[i+20:i+24]

        lst.append((name, ip))

    return lst

def fmt_ip(addr):
    return str(ord(addr[0])) + '.' + \
           str(ord(addr[1])) + '.' + \
           str(ord(addr[2])) + '.' + \
           str(ord(addr[3]))

def fmt_summary (interfaces):
    ips = []
    for interface in interfaces:
        ips.append(
            fmt_ip(interface[1])
        )
    return ips




