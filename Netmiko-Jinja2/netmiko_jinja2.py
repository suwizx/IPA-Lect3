from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import time

USERNAME = "admin"
PASSWORD = "cisco"

devices = {
    "s1": {"device_type": "cisco_ios", "ip": "172.31.41.3", "username": USERNAME, "password": PASSWORD},
    "r1": {"device_type": "cisco_ios", "ip": "172.31.41.4", "username": USERNAME, "password": PASSWORD},
    "r2": {"device_type": "cisco_ios", "ip": "172.31.41.5", "username": USERNAME, "password": PASSWORD},
}

common_vars = {
    "mgmt_subnet": "172.31.41.0",
    "mgmt_wildcard": "0.0.0.15",
    "pc_subnet": "192.168.1.0",
    "pc_wildcard": "0.0.0.255",
    "mask": "255.255.255.240",
    "ospf_wc": "0.0.0.15",
}

s1_vars = {**common_vars}

r1_vars = {
    **common_vars,
    "r1_g1_ip": "172.31.41.17",
    "r1_g2_ip": "172.31.41.33",
    "r1_loopback": "1.1.1.1",
    "ospf_net1": "172.31.41.16",
    "ospf_net2": "172.31.41.32",
}

r2_vars = {
    **common_vars,
    "r2_g1_ip": "172.31.41.34",
    "r2_g2_ip": "172.31.41.49",
    "r2_loopback": "2.2.2.2",
    "ospf_net2": "172.31.41.32",
    "ospf_net3": "172.31.41.48",
    "nat_subnets": [
        {"subnet": "172.31.41.0", "wildcard": "0.0.0.15"},
        {"subnet": "172.31.41.16", "wildcard": "0.0.0.15"},
        {"subnet": "172.31.41.48", "wildcard": "0.0.0.15"},
    ],
}

env = Environment(loader=FileSystemLoader("templates"))

config_map = {
    "s1": ("s1.j2", s1_vars),
    "r1": ("r1.j2", r1_vars),
    "r2": ("r2.j2", r2_vars),
}

for name, (template_name, variables) in config_map.items():
    print(f"=== Rendering + Configuring {name} ===")

    template = env.get_template(template_name)

    rendered_config = template.render(variables)

    print(rendered_config)

    cmds = rendered_config.strip().splitlines()

    with ConnectHandler(**devices[name]) as conn:
        output = conn.send_config_set(cmds)
        print(output)
        save = conn.save_config()
        print(save)

    time.sleep(1)

print("Done.")