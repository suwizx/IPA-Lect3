from netmiko import ConnectHandler

USERNAME = "admin"
PASSWORD = "cisco"

devices = {
    "s1": {"device_type": "cisco_ios", "ip": "172.31.41.3", "username": USERNAME, "password": PASSWORD},
    "r1": {"device_type": "cisco_ios", "ip": "172.31.41.4", "username": USERNAME, "password": PASSWORD},
    "r2": {"device_type": "cisco_ios", "ip": "172.31.41.5", "username": USERNAME, "password": PASSWORD},
}