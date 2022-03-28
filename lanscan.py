import netifaces
from scapy.all import *


def get_own_ip():
    own_ip = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']
    return own_ip

def get_broadcastaddr():
    broadcastaddr = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['broadcast']
    return broadcastaddr

def get_netmask():
    netmask = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['netmask']
    return netmask


if __name__ == '__main__':
    own_ip=get_own_ip()
    broadcastaddr = get_broadcastaddr()
    netmask = get_netmask()
    
    frame=IP(dst=broadcastaddr)/ICMP()
    receive = sr(frame,timeout=1,iface='en0')
    
    print(receive)
    print(broadcastaddr)