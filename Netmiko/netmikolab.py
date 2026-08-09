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
    "interface range gi0/1, gi1/1",
    "switchport mode access",
    "switchport access vlan 101",
    "exit",
    "ip access-list standard MGMT-ACCESS",
    "permit 172.31.41.0 0.0.0.15",
    "permit 10.30.6.0 0.0.0.255",
    "exit",
    "line vty 0 4",
    "access-class MGMT-ACCESS in",
    "exit",
]

config_map = {"s1": s1_cmds}

for name, cmds in config_map.items():
    print(f"=== Configuring {name} ===")
    with ConnectHandler(**devices[name]) as conn:
        output = conn.send_config_set(cmds)
        print(output)
        save = conn.save_config()
        print(save)
    time.sleep(1)

print("Done.")