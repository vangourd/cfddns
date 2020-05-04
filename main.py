#!/usr/bin/python3
from config import Config
import requests
import socket
import fcntl
import json
import struct

OK = "[\033[92m OK \033[0m] "
FAIL = "[\033[91m FAIL \033[0m] "
CHANGE = "[\033[93m CHANGE \033[0m]"
headers = {
        "Content-Type":"application/json",
        "Authorization": f"Bearer {Config.key}"
}

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])

def token_valid():
    r = requests.get(f"{Config.cfapi}user/tokens/verify",headers=headers)
    if not r.json()['success']:
        print(f"{FAIL} Token: {r.status_code}: {r.json()['messages']}")
        return False
    else:
        print(f"{OK} Token: {r.status_code}: {r.json()['messages']}")
        return True

def get_zone_id():
    result = requests.get(f"{Config.cfapi}zones",headers=headers)
    zones = result.json()['result']
    for zone in zones:
        if zone['name'] == Config.domain:
            domain_found = True
    if domain_found:
        print(f"{OK} Domain found [{zone['name']}] id is {zone['id']}")
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
    if(r.json()['result']['success']):
        print(f"{OK} IP Successfully Changed")
        exit(0)
    else:
        print(f"{FAIL} Unable to change IP")
        exit(1)
    
        
if __name__ == "__main__":
    ip_address = get_ip_address(Config.interface)
    if Config.changeme == True:
        print("You need to fill in the settings for the script to work")
        exit(1)
    if not token_valid():
        print("There is an issue with the api token.")
        exit(1)
    zone_id = get_zone_id()
    records = list_zone_records(zone_id)['result']
    for record in records:
        if record['name'] == "loganfamily.us" and record['type'] == "A":
            record_id = record['id']
            if record['content'] == ip_address:
                print(f"{OK} IP Address matches [No Change]")
                exit(0)
            else:
                print(f"{CHANGE} IP Address does not match [Updating...]")
                
    update_cloud_flare(zone_id,record_id,ip_address)

    