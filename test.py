
from libpkt import ifs, pkt, psocket
import random

# capture a random TCP packet from the network
packet = psocket.s_sniff(max_bb=65565, cnt=3)[2]

# disguise a new packet as the old packet
new_packet = pkt.ip(
    src_ip=pkt.rd_in(packet)['src_ip'], 
    dst_ip=pkt.rd_in(packet)['dst_ip'],
    ip_id=54321, ip_ver=4, tcp_seq=454,
    d_hdr=random._urandom(1024)
)

# send this new disguised packet off to the original packet's destination
psocket.send_to(new_packet, dst_ip=pkt.rd_in(packet)['dst_ip'], dst_p=0)

