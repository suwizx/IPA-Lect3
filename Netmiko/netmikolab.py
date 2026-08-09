from netmiko import ConnectHandler
import time

USERNAME = "admin"
PASSWORD = "cisco"

devices = {
    "s1": {"device_type": "cisco_ios", "ip": "172.31.41.3", "username": USERNAME, "password": PASSWORD},
    "r1": {"device_type": "cisco_ios", "ip": "172.31.41.4", "username": USERNAME, "password": PASSWORD},
    "r2": {"device_type": "cisco_ios", "ip": "172.31.41.5", "username": USERNAME, "password": PASSWORD},
}

s1_cmds = [
    "vlan 101",
    "name control-data",
    "exit",
    "interface range gi0/1, gi0/2",
    "switchport mode access",
    "switchport access vlan 101",
    "exit",
    "ip access-list standard MGMT-ACCESS",
    "permit 172.31.41.0 0.0.0.15",
    "permit 192.168.1.0 0.0.0.255",
    "exit",
    "line vty 0 4",
    "access-class MGMT-ACCESS in",
    "exit",
]

r1_cmds = [
    "interface gi0/1",
    "no vrf forwarding control-data",
    "ip address 172.31.41.17 255.255.255.240",
    "exit",
    "interface gi0/2",
    "no vrf forwarding control-data",
    "ip address 172.31.41.33 255.255.255.240",
    "exit",
    "router ospf 1",
    "network 172.31.41.16 0.0.0.15 area 0",
    "network 172.31.41.32 0.0.0.15 area 0",
    "network 1.1.1.1 0.0.0.0 area 0",
    "exit",
    "ip access-list standard MGMT-ACCESS",
    "permit 172.31.41.0 0.0.0.15",
    "permit 192.168.1.0 0.0.0.255",
    "exit",
    "line vty 0 4",
    "access-class MGMT-ACCESS in",
    "exit",
]

r2_cmds = [
    "interface gi0/1",
    "no vrf forwarding control-data",
    "ip address 172.31.41.34 255.255.255.240",
    "exit",
    "interface gi0/2",
    "no vrf forwarding control-data",
    "ip address 172.31.41.49 255.255.255.240",
    "exit",
    "router ospf 1",
    "network 172.31.41.32 0.0.0.15 area 0",
    "network 172.31.41.48 0.0.0.15 area 0",
    "network 2.2.2.2 0.0.0.0 area 0",
    "default-information originate",
    "exit",
    "interface g0/3",
    "ip nat outside",
    "exit",
    "interface g0/1",
    "ip nat inside",
    "exit",
    "interface g0/2",
    "ip nat inside",
    "exit",
    "access-list 1 permit 172.31.41.0 0.0.0.15",
    "access-list 1 permit 172.31.41.16 0.0.0.15",
    "access-list 1 permit 172.31.41.48 0.0.0.15",
    "ip nat inside source list 1 interface g0/3 overload",
    "ip access-list standard MGMT-ACCESS",
    "permit 172.31.41.0 0.0.0.15",
    "permit 192.168.1.0 0.0.0.255",
    "exit",
    "line vty 0 4",
    "access-class MGMT-ACCESS in",
    "exit",
]

config_map = {"r1": r1_cmds, "r2": r2_cmds}

for name, cmds in config_map.items():
    print(f"=== Configuring {name} ===")
    with ConnectHandler(**devices[name]) as conn:
        output = conn.send_config_set(cmds)
        print(output)
        save = conn.save_config()
        print(save)
    time.sleep(1)

print("Done.")