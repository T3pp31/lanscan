import netifaces
from scapy.all import *
import socket
import netaddr
import ipaddress
from tqdm import tqdm
import socket
import os
import pandas as pd



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
# ホストアドレスが出てきてしまう→ネットワークアドレスを出したい
def get_networkaddr():
    ip=get_own_ip()
    netmask=get_netmask()
    network_addr = str(netaddr.IPNetwork(ip+'/'+netmask).cidr)
    
    return network_addr

#ホスト名を検索
def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        hostname='None'
    return hostname

# ipアドレス,macアドレス,host名,ポートを検索する
def get_hostinformation(networkaddr):
    ip_list=[]
    mac_list=[]
    host_name=[]
    open_port=[]
    for ip in tqdm(netaddr.IPNetwork(networkaddr)):
        print(ip)
        ip=str(ip)
        frame = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op=1, pdst = ip)
        receive = srp1(frame,timeout=0.1,iface='en0')
        try:
            mac_list.append(receive[Ether].src)
            ip_list.append(ip)
            print(receive)
        except:
            pass
        
    for ip in tqdm(ip_list):
        host_name.append(get_hostname(ip))
        ip=str(ip)
        individual_port = port_scan(ip)
        open_port.append(individual_port)
        
    return ip_list,mac_list,host_name,open_port

def port_scan(ip):
    individual_port=[]
    for port in tqdm(range(0,65535)):
        s=socket.socket()
        errno = s.connect_ex((ip,port))
        s.close()
        
        if errno == 0 :
            individual_port.append(port)
    return individual_port
        
        
        
def make_result(ip,mac,host,port):
    df=pd.DataFrame()
    df['ip']=ip
    df['mac']=mac
    df['host']=host
    df['port']=port
    
    return df


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
    network_addr = get_networkaddr()
    
    print(f'my_ip:{own_ip}')
    print(f'broadcast_address:{broadcastaddr}')
    print(f'netmask:{netmask}')
    print(f'network_address:{network_addr}')
    
    ip,mac,host,port=get_hostinformation(network_addr)
    df=make_result(ip,mac,host,port)

    print(df)
    