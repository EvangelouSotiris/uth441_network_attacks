## Introduction

The Heartbleed bug is a severe implementation flaw in the OpenSSL library, which enables attackers to steal data from the 
memory of the victim server. The contents of the stolen data depend on what is there in the memory of the server. 

It could potentially contain private keys, TLS session keys, user names, passwords, credit cards, etc. 
The vulnerability is in the implementation of the Heartbeat protocol,which is used by SSL/TLS to keep the connection alive.

## Enviroment Setup

In this lab, we need to set up two VMs: one called attacker machine and the other called victim server.We use the pre-built 
<a href="https://seedsecuritylabs.org/lab_env.html">SEEDUbuntu12.04</a> VM. The VMs need to use the NAT-Network adapter for
the network setting. This can be done by going to the VM settings, picking Network, and clicking the Adaptor tag to switch 
the adapter to NAT-Network. Make sure both VMs are on the same NAT-Network.

The website used in this attack can be any HTTPS website that uses SSL/TLS. However, since it is
illegal to attack a real website, we have set up a website in our VM, and conduct the attack on our own VM. We use an open-source social network application called ELGG, and host it in the following URL: https://www.heartbleedlabelgg.com.

## Launch the attack

The actual damage of the Heartbleed attack depends on what kind of information
is stored in the server memory. If there has not been much activity on the server, you will not be able to steal 
useful data. Therefore, we need to interact with the web server as legitimate users. Let us do it as the administrator, 
and do the followings:item Visit https://www.heartbleedlabelgg.com from your browser.

* Visit https://www.heartbleedlabelgg.com from your browser.
* Login as the site administrator. (User Name:admin; Password:seedelgg)
* Add Boby as friend.
* Send Boby a private message.

After you have done enough interaction as legitimate users, you can launch the attack and see what information you can 
get out of the victim server.The code that we use is called <a href="http://www.cis.syr.edu/~wedu/seed/Labs_12.04/Networking/Heartbleed/attack.py">attack.py</a> which was originally written by Jared Stafford.

You may need to run the attack code multiple times to get useful data. Try and see whether you can get the following 
information from the target server:

* User name and password.
* Admin Activity

To fix the Heartbleed vulnerability, the best way is to update the OpenSSL library to the newest version.This can be 
achieved using the following commands:

* sudo apt-get update
* sudo apt-get upgrade
