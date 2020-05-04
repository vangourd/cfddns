#!/usr/bin/python3
from config import Config
import requests
import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])

def update_cloud_flare(key,email,domain):
    ip_addr = get_ip_address(Config.interface)

if __name__ == "__main__":
    if Config.changeme == True:
        print("You need to fill in the settings for the script to work")
    update_cloud_flare(Config.key,Config.email,Config.domain)