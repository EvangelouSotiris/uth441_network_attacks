# DNS SPOOFING ATTACK

## Protocol Description
Whenever we surf the internet, we mostly visit websites using their hostnames (e.g. google.com, github.com etc.), not the IP addresses where these websites are hosted. In order to do that, some IP-Hostname pairs must exist, and this is offered by the DNS <b>(Domain Name Server)</b> protocol.
DNS is a distributed database implemented in a hierarchy of name servers. It is an application layer protocol for message exchange between clients and servers.

<img src="https://flylib.com/books/2/203/1/html/2/images/cn061201.jpg">

Whenever we want to know the IP for a specific domain name we need to do a nameserver lookup (DNS Request), to specific DNS servers. If they have the answer they reply to us, or they might direct us to another nameserver that might have our answer.

## Preparation

In order to prepare for the DNS spoofing attack we need to have a victim machine's IP, the gateway's IP, and we need to be in the same local network as the targets.
In order to intercept all DNS requests from the victim we need to perform a MITM attack, so before moving on to this lab, one should perform the steps described in the [arp_spoofing](https://github.com/EvangelouSotiris/uth441_network_attacks/blob/master/arp_spoofing.md) markdown first.

## Intercepting DNS packets as a MITM

After doing the steps mentioned above, we are now the Man in the Middle of the connection between the victim machine and the gateway. This means we are intercepting all the packets between them, such as the <b>DNS Request</b> packets.

- We can check that by doing a simple ping from the victim to a domain name such as google.com:
![pinggoogle](https://user-images.githubusercontent.com/28576118/71663236-078b4e80-2d5d-11ea-81ac-aa07856b54de.png)
- On the attacker's machine we can intercept all the important DNS packets using appropriate filters:
![wiredns](https://user-images.githubusercontent.com/28576118/71663367-99935700-2d5d-11ea-8acd-0f92275a64a8.png)

## DNS Spoofing
As the attacker, since we are intercepting those DNS requests, we would also like to poison them in order to redirect to pages that we want (and control most often), instead of the domains the victim user asks for.

We can do this as well using ettercap, by choosing dns_spoof in the Plugins tab while arp poisoning the 2 targets:

![pluginsdns](https://user-images.githubusercontent.com/28576118/71663634-a82e3e00-2d5e-11ea-9ce4-08086bb290c5.png)

- Let's say that we want to intercept the DNS requests for <b> Facebook.com </b> and we want to redirect the victim to a replica of the facebook login page that we crafted in order to steal credentials.

- Firstly we create the replica of the facebook login page using HTML and CSS:

![fb](https://user-images.githubusercontent.com/28576118/71694799-ec4e2c80-2db8-11ea-866f-07b502b3c521.png)

- Then we need to set it up in our localhost as a website. We will use Apache2 for that cause. After moving the files in /var/www/html subdir we restart the apache2 service and we can now access the facebook replica page from http://127.0.0.1:80 .

![varwww](https://user-images.githubusercontent.com/28576118/71664879-68b62080-2d63-11ea-9d27-59f1fd54d2da.png)

- Now, we need to set up the appropriate file in ettercap in order to redirect the victim to our facebook replica when he asks for the facebook.com domain. Specifically in the <b> /etc/ettercap/etter.dns </b> we insert the following lines:

![etterdns](https://user-images.githubusercontent.com/28576118/71693463-38976d80-2db5-11ea-94b5-164de8a0632d.png)

So, we are directing the requests asking for these domain names (facebook.com or any subdirectory in facebook.com) to our own IP and thus our made index.html. When the victim tries to ping facebook.com we see the following message in ettercap:

![dnspoof](https://user-images.githubusercontent.com/28576118/71686435-e00ba480-2da3-11ea-806d-8c46baad67d0.png)

and from the victim side we can see that it looks for facebook.com on our attacker host:

![pingfb](https://user-images.githubusercontent.com/28576118/71693468-3af9c780-2db5-11ea-8497-344ac2261c56.png)

Thus, when the victim tries to enter credentials and log in, we will be able to grab them plaintext from wireshark:

![postreq](https://user-images.githubusercontent.com/28576118/71694221-30403200-2db7-11ea-9a16-402868f49985.png)


