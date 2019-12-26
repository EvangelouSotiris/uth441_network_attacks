# ARP SPOOFING ATTACK

## Preparation

In order to perform an ARP Spoofing attack, we created a victim VM (Ubuntu Server 19.04) in Virtualbox.

![vm_desc](https://user-images.githubusercontent.com/28576118/71472063-4d369d00-27da-11ea-9632-bfcdc2911ed8.png)

The MITM attack, through which we will perform ARP Spoofing will be performed from the host machine, using <b>Ettercap</b>.

After opening Ettercap in promiscuous mode and selecting Unified sniffing, we need to select our targets, that are 1) The victim VM and 2) The Gateway router. We are on the ethernet interface of our host so:


![ipa](https://user-images.githubusercontent.com/28576118/71472689-a56e9e80-27dc-11ea-9677-2de6851ab61f.png)

Using the default net tool ip we define our own IP and the gateway IP.
Let's use Ettercap's Host List utility to define the victim's IP:

![image](https://user-images.githubusercontent.com/28576118/71472904-89b7c800-27dd-11ea-9d88-01cd834c5934.png)

We now have the 3 IPs needed:
<ul>
  <li> Attacker's IP: 192.168.1.116 </li>
  <li> Victim's IP: 192.168.1.111 </li>
  <li> Gateway IP: 192.168.1.254 </li>
</ul>
We choose the latter two as targets in Ettercap:

![targets](https://user-images.githubusercontent.com/28576118/71473128-7c4f0d80-27de-11ea-83c4-60f21ed40f14.png)

## ARP Spoofing/Poisoning

After choosing the targets we are selecting the tab MITM (Man In The Middle) and then ARP-poisoning. Some seconds later we can check the Wireshark packet log and see that the attack has successfully launched, as our IP is using the MAC address of each of the two targets. We can see the duplicate IP warning that ensures that the attack is taking place.

![duparp](https://user-images.githubusercontent.com/28576118/71473381-6beb6280-27df-11ea-8321-5dc2be29c4c1.png)
