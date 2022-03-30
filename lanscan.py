import netifaces
from scapy.all import *
import socket
import netaddr


def get_own_ip():
    own_ip = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']
    return own_ip

def get_broadcastaddr():
    broadcastaddr = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['broadcast']
    return broadcastaddr

def get_netmask():
    netmask = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['netmask']
    return netmask

#ネットワークアドレス部を求める
def get_networkaddr():
    ip=get_own_ip()
    ip = netaddr.IPNetwork(ip)

    
    return ip.network
    

# ipアドレスを求める関数

# macアドレスを求める関数

# ホスト名を取得
def get_hostname(ip_list):
    host_list=[]
    for ip in ip_list:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            host_list.append(hostname)
        except:
            host_list.append('None')

    return host_list


if __name__ == '__main__':
    own_ip=get_own_ip()
    broadcastaddr = get_broadcastaddr()
    netmask = get_netmask()
    
    print(get_networkaddr())
    
    