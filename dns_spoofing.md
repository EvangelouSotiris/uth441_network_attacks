# DNS SPOOFING ATTACK

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
