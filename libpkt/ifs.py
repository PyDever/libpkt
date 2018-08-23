
"""
list and view interfaces
"""

import socket # for network stuff
import random # building packets
import struct # for packing headers

import fcntl  # file descriptor ops
import array  # for building arrays
import time   # for building timeouts

# globals
SOCKET = socket.socket(socket.AF_INET,
    socket.SOCK_DGRAM)

FCNTL = fcntl

def ls_ifs (fileno=SOCKET.fileno(), ioctl=FCNTL.ioctl): 
    """listing available network interfaces"""
    max_possible = 128
    bytes = max_possible * 32 

    names = array.array('B', '\0' * bytes)

    outbytes = struct.unpack('iL', ioctl(
        fileno,
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

def fmt_ip(interface=None):
    """format the IP address of one interface"""

    return str(ord(interface[1][0])) + '.' + \
           str(ord(interface[1][1])) + '.' + \
           str(ord(interface[1][2])) + '.' + \
           str(ord(interface[1][3]))

def fmt_summary (interfaces=None):
    """format the IP addresses of all interfaces"""
    ips = []
    for interface in interfaces:
        ips.append(
            fmt_ip(interface[1])
        )
    return ips

