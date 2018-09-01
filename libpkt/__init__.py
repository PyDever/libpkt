
"""
Low-level TCP/IP packet manipulation library
for Python 2.7. 

Classes:
	- PSocket
	- IP, ICMP
"""

# data structure related imports
import fcntl
import array
import struct
import random

# network related imports
import socket
import time

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

def read (packet):
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

"""PSocket class, sending and receiving packets"""
class PSocket (object):

	def __init__ (self, timeout=0):

		self.socket = socket.socket(socket.AF_INET,
			socket.SOCK_RAW, socket.IPPROTO_TCP)

		self.timeout = timeout

	def sendp (self, packet, dst_ip='0.0.0.0', dst_p=0):
		"""send a raw TCP/IP packet over the line"""
		try:
			self.socket.sendto(packet, (dst_ip, dst_p))
			return True

		except (socket.error) as error_msg:
			return (False, error_msg)

	def recvp (self, live=True, max_bb=65565, count=2):
		"""receive some raw TCP/IP packets over the line"""

		try:
			packets = []
			for x in range(int(count)):
				
				one = self.socket.recvfrom(max_bb)
				packets.append(one)

				if (live == True): print(one)

			return list(packets)
		except (socket.error) as error_msg:
			return (False, error_msg)

class IP (object):

	def __init__ (self, src_ip='0.0.0.0', dst_ip='0.0.0.0', 
		ip_id=0000, d_hdr=0):

		self.src_ip = src_ip; self.dst_ip = dst_ip
		self.ip_id = ip_id
		self.d_hdr = d_hdr


	@property 
	def bin (self):

	    """build a TCP/IP packet from scratch with raw bytes"""

	    source_ip = self.src_ip; dest_ip = self.dst_ip; data_header = self.d_hdr
	    # ip header fiels_addr
	    ip_ihl = 5; ip_ver = 4; ip_tos = 0
	    ip_tot_len = 0; ip_id = self.ip_id   #Id of this packet
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

