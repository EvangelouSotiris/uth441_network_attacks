#!/usr/bin/python

"CS144 In-class exercise: MAC Address Overflow Attack"
import mininet
from mininet.topo import Topo
from mininet.node import CPULimitedHost, Controller, RemoteController
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process

import sys
import os

class StarTopo(Topo):
    "Star topology for MAC Address Overflow Attack Demo"

    def __init__(self, n=3, cpu=None, bw_host=1000, bw_net=1.5,
                 delay=10, maxq=None, diff=False):

        # Add default members to class.
        super(StarTopo, self ).__init__()

        # Create switch and host nodes
        self.addNode( 'alice', cpu=cpu )
        self.addNode( 'bob', cpu=cpu )
        self.addNode( 'eve', cpu=cpu )
            
        self.addSwitch('s0')
        self.addLink('alice', 's0', bw=bw_host)
        self.addLink('bob', 's0', bw=bw_host)
        self.addSwitch('s1')
        self.addLink('s1', 's0', bw=bw_host)
        self.addLink('eve', 's1', bw=bw_host)

def bbnet():
    "Create network and run Buffer Bloat experiment"
    print "starting mininet ...."
    # Seconds to run iperf; keep this very high
    seconds = 3600
    start = time()
    # set delay 
    # Reset to known state
    topo = StarTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=RemoteController, xterms=True,
                  autoPinCpus=True)
    net.start()
    #dumpNodeConnections(net.hosts)
    net.pingAll()
    os.system("bash tc_cmd.sh 20")
    sleep(2)
    alice = net.getNodeByName('alice')
    bob = net.getNodeByName('bob')
    eve = net.getNodeByName('eve')
    alice.cmd('ping -i 1 bob')
    print "Before the attack, Eve tries to do some eavesdropping"
    eve.cmd('sudo ifconfig eve-eth0 promisc')
    #eve.cmd('sudo tcpdump -n ip host 10.0.0.1')
    CLI( net )    

if __name__ == '__main__':
    bbnet()
