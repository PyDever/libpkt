
import socket # for network stuff
import random # building packets
from struct import *

import fcntl, array, time

TCP_SOCK = socket.socket(socket.AF_INET,
    socket.SOCK_RAW, socket.IPPROTO_TCP)

# this function will send a raw TCP/IP packet
def send_to (packet, dst_ip='0.0.0.0', dst_p=0):
    try:
        TCP_SOCK.sendto(packet, (dst_ip, dst_p))
        return True 
    except socket.error: return False 

# this function will sniff for TCP/IP packet traffic
def s_sniff (max_bb=65565, cnt=2):
    try:
        packets = []

        for x in range (int(cnt)):
            packets.append(TCP_SOCK.recvfrom(65565))

        return list(packets)

    except socket.error:
        return False

def l_sniff (max_bb=65565, cnt=2):
    try:
        packets = []

        for x in range(int(cnt)):

            one = TCP_SOCK.recvfrom(65565)
            print one
            packets.append(one)

        return list(packets)

    except socket.error:
        return False 

