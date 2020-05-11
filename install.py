#!/usr/bin/python3
import subprocess
import sys
import os
import argparse
import platform

OK = "[\033[92m OK \033[0m] "
FAIL = "[\033[91m FAIL \033[0m] "
CHANGE = "[\033[93m CHANGE \033[0m]"
PS="C:\\Windows\\System32\WindowsPowerShell\\v1.0\\powershell.exe"

def success(msg):
    sys.stdout.write(f"{OK} {msg} \n")

def fail(msg):
    sys.stdout.write(f"{FAIL} {msg} \n")

def linux():
    try:
        subprocess.run(["cp","./cfddns","/usr/sbin/cfddns.py","-Z"], check=True)
        success("Installed exec file")
        subprocess.run(["chmod","755","/usr/sbin/cfddns.py"], check=True)
        success("Set file permissions ")
        subprocess.run(["chmod","+x","/usr/sbin/cfddns.py"],check=True)
        success("Set execution bit")
        if os.path.isdir("/etc/cfddns"):
            subprocess.run(["chmod","755","/etc/cfddns"])
        else:
            subprocess.run(["mkdir","-m","755","/etc/cfddns"],check=True)
        success("Created /etc/cfddns/ directory")
        subprocess.run(["cp","./cfddns.conf","/etc/cfddns/cfddns.conf","-Z"],check=True)
        success("Copied config to /etc/cfddns/cfddns.conf")
        subprocess.run(["cp","./cfddns.service","/etc/systemd/system/cfddns.service","-Z"],check=True)
        success("Copied service file to /etc/systemd/system")
        subprocess.run(["cp","./cfddns.timer","/etc/systemd/system/cfddns.timer","-Z"],check=True)
        success("Copied timer file to /etc/systemd/system")
    except subprocess.CalledProcessError as e:
        fail(e)

def windows():
    # Create a folder in Program Files
    if not os.path.isdir("C:\Program Files\cfddns"):
        subprocess.run([PS,"mkdir","'C:\Program Files\cfddns'"],check=True)
        success("Created Program Files Directory")
    else:
        success("Program Files already exists")
    subprocess.run([PS,"cp","-r","-Force","'./dist/cfddns/'","'C:\\Program Files\\'"], check=True)
    success("Copied executable to PF directory")
    subprocess.run([PS,"setx /M PATH ($env:PATH + ';C:\\Program Files\\cfddns;')"])
    success("Installed executable to path")
    if not os.path.isdir("C:\\ProgramData\\cfddns"):
        subprocess.run([PS,"mkdir","C:\\ProgramData\\cfddns"], check=True)
        success("Created cfddns ProgramData configuration folder")
    else:
        success("ProgramData folder already exists")
    subprocess.run([PS,"cp","'./cfddns.conf'","'C:\\ProgramData\\cfddns\\cfddns.conf'"], check=True)
    success("Copied configuration file to ProgramData")
    try:
        subprocess.run([PS,"Get-ScheduledTask CFDDNS"],check=True)
    except subprocess.CalledProcessError:
        ps_task_creation = f"""
        $A = New-ScheduledTaskAction -Execute "cfddns.exe";
        $T = New-ScheduledTaskTrigger -Daily -DaysInterval 1 -At 11:29PM;
        $S = New-ScheduledTaskSettingsSet;
        $D = New-ScheduledTask -Action $A -Trigger $T -Settings $S;
        Register-ScheduledTask CFDDNS -InputObject $D;
        """
        subprocess.run([PS,ps_task_creation],check=True)
    finally:
        success("Scheduled task for CFDDNS")

if __name__ == "__main__":
    if platform.system() == "Windows":
        windows()
    else:
        linux()