
"""these imports are for low-level packet manipulation"""
import random               # building packets
import struct               # for packing headers
import fcntl                # file descriptor ops
import array                # for building arrays

"""these imports are for the network operations"""
import time                 # for building timeouts
import socket               # for network stuff
import netifaces            # OPTIONAL: for interface operations

"""these imports are for low-level system calls and terminal control"""
import sys                  # for system calls
import os                   # for OS calls
import tty                  # for terminal sys calls
import termios              # for terminal sys calls

"""
TERMINAL CONTROL FUNCTIONS

first we need to implement all the terminal control functions:
    - get_terminal_settings(): return the current UNIX terminal settings
    - update_terminal_settings(): wrapper to refresh UNIX terminal settings
    - flush_terminal_io_streams(): flush UNIX terminal i/o stream
    - enable_terminal_output(): enable UNIX terminal output stream
"""
def get_terminal_settings ():

    """return the current UNIX terminal settings"""

    UNIX_terminal_settings = termios.tcgetattr(
        sys.stdin.fileno())

    return UNIX_terminal_settings

def update_terminal_settings ():

    """wrapper to refresh UNIX terminal settings"""

    # DEPENDS ON get_terminal_settings()

    termios.tcsetattr(sys.stdin.fileno(), 
        termios.TCSANOW, get_terminal_settings())

def flush_terminal_io_streams ():

    """flush UNIX terminal i/o stream"""

    termios.tcflush(sys.stdin.fileno(), 
        termios.TCIOFLUSH)

    # in addition to the above, this function
    # will also flush the system i/o stream as a whole

    sys.stdin.flush(); sys.stdout.flush()

def enable_terminal_output ():

    """enable UNIX terminal output stream"""

    # DEPENDS ON get_terminal_settings()
    #            update_terminal_settings()

    UNIX_terminal_settings = get_terminal_settings()

    UNIX_terminal_settings[3] |= termios.ECHO

    termios.tcsetattr(sys.stdin.fileno(), 
        termios.TCSANOW, UNIX_terminal_settings)

"""
INTERFACE FUNCTIONS

second we need to implement all the interface functions:
    - list_interfaces(): wrapper to netifaces function
    - interface_configuration(): wrapper to netifaces function
    - get_interface_address(): wrapper to netifaces function
"""

def list_interfaces ():

   """wrapper to netifaces function"""

   # DEPENDS ON netifaces.interfaces()
   #            netifaces.ifaddresses()

   return netifaces.interfaces()

def interface_configuration (interface):

   """wrapper to netifaces function"""

   # DEPENDS ON netifaces.interfaces()
   #            netifaces.ifaddresses()

   return netifaces.ifaddresses(interface)

def get_interface_address (interface):

   """wrapper to netifaces function"""

   # DEPENDS ON netifaces.interfaces()
   #            netifaces.ifaddresses()
   #            interface_configuration()

   return interface_configuration(interface)[2][0]['addr']

"""
PACKET CONTROL FUNCTIONS

thirdly we need to implement all the packet control functions:

    SUB-CLASS: support functions
    - checksum(): grab the hashed checksum of ASCII text

    SUB-CLASS: packaging operations
    - build_packet(): build a TCP/IP packet from scratch with raw bytes
    - open_captured_packet(): read-in a TCP/IP packet and parse it out

    SUB-CLASS: socketing operations
    - live_packet_capture(): capture TCP/IP traffic, live in-terminal
    - silent_packet_capture(): capture TCP/IP traffic, silent 
    - send_packet(): send a raw TCP/IP packet over the line
"""

def checksum (message):

    """grab the hashed checksum of ASCII text"""
    
    s = 0
    # loop taking 2 characters at a time
    for i in range(0, len(message), 2):
        w = ord(message[i]) + (ord(message[i+1]) << 8 )
        s = s + w
    # complement and mask to 4 byte short
    s = ~s & 0xffff
     
    return s

def build_packet (src_ip='127.0.0.1', dst_ip='127.0.0.1',
    ip_id=00000, ip_ver=4, tcp_seq=454, d_hdr=random._urandom(1024)):

    """build a TCP/IP packet from scratch with raw bytes"""

    source_ip = src_ip; dest_ip = dst_ip; data_header = d_hdr
    # ip header fiels_addr
    ip_ihl = 5; ip_ver = 4; ip_tos = 0
    ip_tot_len = 0; ip_id = 54321   #Id of this packet
    ip_frag_off = 0; ip_ttl = 255; ip_proto = socket.IPPROTO_TCP
    ip_check = 0    # kernel will fill the correct checksum

    ip_saddr = socket.inet_aton ( source_ip )   #Spoof the source ip address if you want to
    ip_daddr = socket.inet_aton ( dest_ip )
    ip_ihl_ver = (ip_ver << 4) + ip_ihl
    
    # the ! in the pack format string means network order
    ip_header = struct.pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, 
        ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
    
    # tcp header fields
    tcp_source = 1234; tcp_dest = 80; tcp_seq = 454
    tcp_ack_seq = 0; tcp_doff = 5 

    #tcp flags

    tcp_fin = 0; tcp_syn = 1; tcp_rst = 0
    tcp_psh = 0; tcp_ack = 0; tcp_urg = 0
    tcp_window = socket.htons (5840)    #   maximum allowed window size
    tcp_check = 0; tcp_urg_ptr = 0
    
    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) 
    tcp_flags = tcp_flags + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)
    
    # the ! in the pack format string means network order
    tcp_header = struct.pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, 
        tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
    
    user_data = data_header
    
    # pseudo header fields
    source_address = socket.inet_aton( source_ip )
    dest_address = socket.inet_aton(dest_ip); placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header) + len(user_data)
    
    psh = struct.pack('!4s4sBBH' , source_address , dest_address , 
        placeholder , protocol , tcp_length);
    psh = psh + tcp_header + user_data;
    
    tcp_check = checksum(psh)
    #print tcp_checksum
    
    # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
    tcp_header = struct.pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, 
        tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + struct.pack('H' , tcp_check) + struct.pack('!H' , tcp_urg_ptr)
    
    # final full packet - syn packets dont have any data
    packet = ip_header + tcp_header + user_data
    return packet

def open_captured_packet (packet):

    """read-in a TCP/IP packet and parse it out"""

    # take first 20 characters for the ip header
    ip_header = packet[0:20]

    iph = struct.unpack('!BBHHHBBH4s4s' , ip_header[0][0:20])
    version_ihl = iph[0]; version = version_ihl >> 4
    ihl = version_ihl & 0xF; iph_length = ihl * 4 

    ttl = iph[5]; protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8])
    d_addr = socket.inet_ntoa(iph[9])
    
    #get data from the packet
    data = packet[0]
    return {"src_ip":s_addr, 
        "dst_ip":d_addr, "d_hdr":data}

def send_packet (packet, dst_ip='0.0.0.0', dst_p=0):

    """send a raw TCP/IP packet over the line"""

    TCP_SOCK = socket.socket(socket.AF_INET,
        socket.SOCK_RAW, socket.IPPROTO_TCP)
    try:
        TCP_SOCK.sendto(packet, (dst_ip, dst_p))
        return True 
    except socket.error: return False 

def live_packet_capture (max_bb=65565, cnt=2):
    
    """capture TCP/IP traffic, live in-terminal"""

    TCP_SOCK = socket.socket(socket.AF_INET,
        socket.SOCK_RAW, socket.IPPROTO_TCP)
    try:
        packets = []

        for x in range(int(cnt)):

            one = TCP_SOCK.recvfrom(65565)
            packets.append(one)

        return list(packets)

    except socket.error:
        return False 

def silent_packet_capture (max_bb=65565, cnt=2):

    """capture TCP/IP traffic, silent"""

    TCP_SOCK = socket.socket(socket.AF_INET,
        socket.SOCK_RAW, socket.IPPROTO_TCP)
    try:
        packets = []

        for x in range (int(cnt)):
            packets.append(TCP_SOCK.recvfrom(65565))

        return list(packets)

    except socket.error:
        return False

