import subprocess

import requests

try:

    response = requests.get("http://localhost:255/State/IsActive", timeout=0.25)

    print("Server is Running.")

except Exception:

    print("Server is not Running... Starting server in new cmd window.")

    CREATE_NO_WINDOW = 0x08000000
    subprocess.Popen(
        'python "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\AutomationBareNecessities\\Server.py"',
        creationflags=CREATE_NO_WINDOW,
    )
