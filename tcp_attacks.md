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

The first `SYN` informs the server that a client wants to establish a new connection. The server stores this request in a queue and the connection is called a *half-open connection*. When the third step (the client sending the `ACK` ) is completed the request is removed from this queue.

In this attack, the queue of the half-open connections is used to make the server unresponsive to new clients. The attacker sends a lot of `SYN` without replying `ACK`, filling the queue and binding resources of the server. When a legitimate client tries to connect to the server, the server will not be able to accept new `SYN` packets.
