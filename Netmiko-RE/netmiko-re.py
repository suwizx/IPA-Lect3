from netmiko import ConnectHandler
import re

USERNAME = "admin"
PASSWORD = "cisco"

devices = {
    "r1": {"device_type": "cisco_ios", "ip": "172.31.41.4", "username": USERNAME, "password": PASSWORD},
    "r2": {"device_type": "cisco_ios", "ip": "172.31.41.5", "username": USERNAME, "password": PASSWORD},
}

interface_pattern = re.compile(
    r'^(?P<interface>\S+)\s+'
    r'(?P<ipaddr>\S+)\s+'
    r'(?P<ok>\S+)\s+'
    r'(?P<method>\S+)\s+'
    r'(?P<status>up|down|administratively down)\s+'
    r'(?P<protocol>up|down)\s*$',
    re.MULTILINE
)

uptime_pattern = re.compile(
    r'^\S+\s+uptime is\s+(?P<uptime>.+)$',
    re.MULTILINE
)

for name, params in devices.items():
    print(f"=== {name} ===")

    with ConnectHandler(**params) as conn:
        brief_output = conn.send_command("show ip interface brief")
        version_output = conn.send_command("show version")

    uptime_match = uptime_pattern.search(version_output)
    uptime = uptime_match.group("uptime") if uptime_match else "unknown"

    active_interfaces = []
    for match in interface_pattern.finditer(brief_output):
        if match.group("status") == "up" and match.group("protocol") == "up":
            active_interfaces.append(match.group("interface"))

    print(f"Device uptime: {uptime}")
    print("Active interfaces:")
    for intf in active_interfaces:
        print(f"  - {intf}")
    print()