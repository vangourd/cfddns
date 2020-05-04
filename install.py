#!/usr/bin/python3
import subprocess
import sys
import os

OK = "[\033[92m OK \033[0m] "
FAIL = "[\033[91m FAIL \033[0m] "
CHANGE = "[\033[93m CHANGE \033[0m]"

def success(msg):
    sys.stdout.write(f"[ {OK} ] {msg} \n")

def fail(msg):
    sys.stdout.write(f"[ {FAIL} {msg} \n")

try:
    subprocess.run(["cp","./cfddns.py","/usr/sbin/cfddns.py","-Z"], check=True)
    success("Installed exec file")
    subprocess.run(["chmod","755","/usr/sbin/cfddns.py"], check=True)
    success("Set file permissions ")
    subprocess.run(["chmod","+x","/usr/sbin/cfddns.py"],check=True)
    success("Set execution bit")
    if os.path.isdir("/etc/cfddns"):
        subprocess.run(["chmod","750","/etc/cfddns"])
    else:
        subprocess.run(["mkdir","-m","750","/etc/cfddns"],check=True)
    success("Created /etc/cfddns/ directory")
    subprocess.run(["cp","./cfddns.conf","/etc/cfddns/cfddns.conf","-Z"],check=True)
    success("Copied config to /etc/cfddns/cfddns.conf")
    subprocess.run(["cp","./cfddns.service","/etc/systemd/system/cfddns.service","-Z"],check=True)
    success("Copied service file to /etc/systemd/system")
    subprocess.run(["cp","./cfddns.timer","/etc/systemd/system/cfddns.timer","-Z"],check=True)
    success("Copied timer file to /etc/systemd/system")
except subprocess.CalledProcessError as e:
    fail(e)
