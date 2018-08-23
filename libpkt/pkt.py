

import socket # for network stuff
import random # building packets
from struct import *
import fcntl  # file descriptor ops
import array  # for building arrays
import time   # for building timeouts

def checksum(msg):
    """grab the checksum of a string"""
    s = 0
     
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
        s = s + w
     
    # complement and mask to 4 byte short
    s = ~s & 0xffff
     
    return s

def make (src_ip='0.0.0.0', dst_ip='0.0.0.0',
    ip_id=00000, ip_ver=4, tcp_seq=454, d_hdr=random._urandom(8)):

    """
    perhaps the most complicated of our functions, this function
    will build a TCP/IP packet in real time.
    """
    source_ip = src_ip
    dest_ip = dst_ip
    data_header = d_hdr

    # ip header fiels_addr
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0 
    ip_id = 54321   #Id of this packet

    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0    # kernel will fill the correct checksum

    ip_saddr = socket.inet_aton ( source_ip )   #Spoof the source ip address if you want to

    ip_daddr = socket.inet_aton ( dest_ip )
    
    ip_ihl_ver = (ip_ver << 4) + ip_ihl
    
    # the ! in the pack format string means network order
    ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
    
    # tcp header fields
    tcp_source = 1234   # source port

    tcp_dest = 80   # destination port

    tcp_seq = 454
    tcp_ack_seq = 0
    tcp_doff = 5    #4 bit field, size of tcp header, 5 * 4 = 20 bytes

    #tcp flags

    tcp_fin = 0
    tcp_syn = 1
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = 0
    tcp_urg = 0
    tcp_window = socket.htons (5840)    #   maximum allowed window size

    tcp_check = 0
    tcp_urg_ptr = 0
    
    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)
    
    # the ! in the pack format string means network order
    tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
    
    user_data = data_header
    
    # pseudo header fields
    source_address = socket.inet_aton( source_ip )
    dest_address = socket.inet_aton(dest_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header) + len(user_data)
    
    psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
    psh = psh + tcp_header + user_data;
    
    tcp_check = checksum(psh)
    #print tcp_checksum
    
    # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
    tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)
    
    # final full packet - syn packets dont have any data
    packet = ip_header + tcp_header + user_data
    return packet

def open (packet):
    #take first 20 characters for the ip header
    ip_header = packet[0:20]
    #now unpack them :)
    iph = unpack('!BBHHHBBH4s4s' , ip_header[0][0:20])
     
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
     
    iph_length = ihl * 4
     
    ttl = iph[5]
    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8])
    d_addr = socket.inet_ntoa(iph[9])
     
    #get data from the packet
    data = packet[0]

    return {"src_ip":s_addr, "dst_ip":d_addr, "d_hdr":data}

