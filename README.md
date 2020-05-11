# CFDDNS.py

Very simple script that pulls an IP off of a selected interface or queries a web API and then modifies an existing A record on CloudFlare. 

You can setup a Free Account to manage your domains allowing you to do this. 

## Requires:

- Python3
- Free CloudFlare Account

I had to setup the following permissions in my CF account for this to work. I KNOW that this is more than required but since this is a hobby project and I'm not as concerned about narrowing down the permissions.

Account.Access: Audit Logs, Account.Logs, Account.Rule Policies, Account.Account Filter Lists, Account.IP Prefixes: BGP On Demand, Account.Teams, Account.Access: Organizations, Identity Providers, and Groups, Account.Workers KV Storage, Account.Workers Scripts, Account.Load Balancing: Monitors And Pools, Account.Account Firewall Access Rules, Account.DNS Firewall, Account.Stream, Account.Billing, Account.Account Settings, User.Memberships, User.User Details, Zone.Zone Settings, Zone.Zone, Zone.Workers Routes, Zone.SSL and Certificates, Zone.Logs, Zone.Page Rules, Zone.Load Balancers, Zone.Firewall Services, Zone.DNS, Zone.Analytics, Zone.Access: Apps and Policies

## Setup (Windows):
### EXE not requiring Python3
Download from [Releases](https://github.com/vangourd/cfddns/releases)
Unzip and cd into `cfddns` 
Run from admin powershell `/dist/install/install.exe`

Frequency can be modified from the **Task Scheduler**

### Source:
Run `./install.py` from Administrative powershell

## Setup (Linux):

`git clone https://github.com/vangourd/cfddns`

`cd cfddns/`

*Edit the **.conf** file with your information or the script will fail*

Read this first to make sure it isn't doing anything you don't want it to. 
`sudo install.py`

`systemctl daemon-reload`

`systemctl start cfddns`

The timer file is set to update once a day but this can be changed.
'1d, 1h, 2m, 1w' Etc

