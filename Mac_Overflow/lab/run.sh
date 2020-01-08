#!/bin/bash
echo "start cs144 buffer bloat experiment"
sudo sysctl -w net.ipv4.tcp_congestion_control=reno
sudo python macoverflow.py
echo "cleaning up..."
sudo killall -9 tcpdump ping
mn -c > /dev/null 2>&1
echo "end"
