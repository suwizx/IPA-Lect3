from pathlib import Path

import paramiko

DEVICES = ["172.31.41.1", "172.31.41.2", "172.31.41.3",
           "172.31.41.4", "172.31.41.5"]

USERNAME = "admin"
KEY_FILE = str(Path.home() / ".ssh" / "id_rsa")

for ip in DEVICES:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=USERNAME, key_filename=KEY_FILE,
                   look_for_keys=False, allow_agent=False)
    print(f"{ip}  OK")
    client.close()