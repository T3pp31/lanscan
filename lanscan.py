import netifaces
from scapy.all import *
import socket
import netaddr
import ipaddress
from tqdm import tqdm
import socket
import os
import pandas as pd
import threading


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

def port_scan(ip_list):
    for ip in tqdm(ip_list):
        for port in tqdm(range(0,65535)):
            individual_port=[]
            s=socket.socket()
            errno = s.connect_ex((ip,port))
            s.close()
        
            if errno == 0 :
                individual_port.append(port)
        port.append(individual_port)
        
        
def port_run(ip):
    scan_range = [1, 65535];

    host = ip

    threads = [];
    ports = [];
    isopen = [];
    individual_port=[]

    def Run(port, i):
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_code = con.connect_ex((host, port))
        con.close()

        if return_code == 0:
            isopen[i]=1;
        
    
    count = 0;
    for port in tqdm(range(scan_range[0], scan_range[1])):
        ports.append(port);
        isopen.append(0);
        thread = threading.Thread(target=Run, args=(port, count));
        thread.start();
        threads.append(thread);
        count = count + 1;
    thread.join()
    
        
    for i in range(len(threads)):
        threads[i].join()
        if isopen[i] == 1:
            individual_port.append(ports[i])
            print('%d open' % ports[i])
    
    print(individual_port)

    return individual_port











# ipアドレス,macアドレス,host名,ポートを検索する
def get_hostinformation(networkaddr):
    ip_list=[]
    mac_list=[]
    host_name=[]
    port=[]

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
        
    host_name.append(get_hostname(ip_list))
    
    for ip in tqdm(ip_list):
        individual_port=port_run(ip)
        port.append(individual_port)
        
        
        
    
        
    return ip_list,mac_list,host_name,port


        
        
        
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
    

    print(f'ip:{ip}')
    print(f'mac:{mac}')
    print(f'hostname:{host}')
    print(f'port:{port}')