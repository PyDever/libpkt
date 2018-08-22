
import socket # for network stuff
import random # building packets
import struct # for packing headers

import fcntl  # file descriptor ops
import array  # for building arrays
import time   # for building timeouts

# globals
TCP_SOCK = socket.socket(socket.AF_INET,
    socket.SOCK_RAW, socket.IPPROTO_TCP)

def send_to (packet, dst_ip='0.0.0.0', dst_p=0):
    """this function will send raw TCP/IP packet"""

    try:
        TCP_SOCK.sendto(packet, (dst_ip, dst_p))
        return True 
    except socket.error: return False 

def s_sniff (max_bb=65565, cnt=2):
    """ perform silent sniff"""
    try:
        packets = []

        for x in range (int(cnt)):
            packets.append(TCP_SOCK.recvfrom(65565))

        return list(packets)

    except socket.error:
        return False

def l_sniff (max_bb=65565, cnt=2):
    """perform live sniff"""
    try:
        packets = []

        for x in range(int(cnt)):

            one = TCP_SOCK.recvfrom(65565)
            print one
            packets.append(one)

        return list(packets)

    except socket.error:
        return False 

