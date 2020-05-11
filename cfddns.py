#!/usr/bin/python3
import platform
platform = platform.system()
import configparser
import requests
import socket
if platform == "Linux":
    import fcntl
import re
import json
import struct
import sys

conf = configparser.ConfigParser()
if platform == "Windows":
    conf.read('C:\\ProgramData\\cfddns\\cfddns.conf')
else:
    conf.read('/etc/cfddns/cfddns.conf')
conf = conf['DEFAULT']

class Config:
    changeme = conf['changeme']
    key = conf['key']
    email = conf['email']
    domain = conf['domain']
    interface = conf['interface']
    cfapi = conf['cfurl']

OK = "[\033[92m OK \033[0m] "
FAIL = "[\033[91m FAIL \033[0m] "
CHANGE = "[\033[93m CHANGE \033[0m]"
headers = {
        "Content-Type":"application/json",
        "Authorization": f"Bearer {Config.key}"
}

def get_ip_address(ifname):
    if platform == "Linux":
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return str(socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15],'utf-8'))
        )[20:24]))
    else:
        sys.stdout.write(f"{OK} Windows detected: Falling back to web based IP determination")
        r = requests.get("http://checkip.dyndns.org/")
        m = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',r.text)
        print(m[0])
        return m[0]
        

def token_valid():
    r = requests.get(f"{Config.cfapi}user/tokens/verify",headers=headers)
    if not r.json()['success']:
        sys.stderr.write(f"{FAIL} Token: {r.status_code}: {r.json()['messages']} \n")
        return False
    else:
        sys.stdout.write(f"{OK} Token: {r.status_code}: {r.json()['messages']} \n")
        return True

def get_zone_id():
    result = requests.get(f"{Config.cfapi}zones",headers=headers)
    zones = result.json()['result']
    for zone in zones:
        if zone['name'] == Config.domain:
            domain_found = True
    if domain_found:
        sys.stdout.write(f"{OK} Domain found [{zone['name']}] id is {zone['id']}\n")
        return zone['id']

def list_zone_records(id):
    r = requests.get(f"{Config.cfapi}zones/{id}/dns_records",headers=headers)
    return r.json()

def update_cloud_flare(zone_id,record_id,ip_addr):
    ip_addr = get_ip_address(Config.interface)
    data = json.dumps({
            "type":"A",
            "name":f"{Config.domain}",
            "content":f"{ip_addr}",
            "ttl":1,
    })
    r = requests.put(
        f"{Config.cfapi}zones/{zone_id}/dns_records/{record_id}",
        data=data,
        headers=headers
    )
    if(r.json()['success']):
        sys.stdout.write(f"{OK} IP Successfully Changed \n")
        sys.exit(0)
    else:
        sys.stderr.write(f"{FAIL} Unable to change IP \n")
        sys.exit(1)
    
        
if __name__ == "__main__":
    ip_address = get_ip_address(Config.interface)
    if Config.changeme == True:
        sys.stdout.write("You need to fill in the settings for the script to work \n")
        sys.exit(1)
    if not token_valid():
        sys.stderr.write("There is an issue with the api token. \n")
        sys.exit(1)
    zone_id = get_zone_id()
    records = list_zone_records(zone_id)['result']
    for record in records:
        if record['name'] == "loganfamily.us" and record['type'] == "A":
            record_id = record['id']
            if record['content'] == ip_address:
                sys.stdout.write(f"{OK} IP Address matches [No Change] \n")
                sys.exit(0)
            else:
                sys.stdout.write(f"{CHANGE} IP Address does not match [Updating...] \n")
                
    update_cloud_flare(zone_id,record_id,ip_address)

    