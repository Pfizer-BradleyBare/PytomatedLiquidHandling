import requests
import os

try:

    response = requests.get("http://localhost:8080/State/IsActive")

    print("Server is Running.")

except Exception:

    print("Server is not Running... Starting server in new cmd window.")

    os.system(
        'start cmd /K python "C:\\Program Files (x86)\\HAMILTON\\BAREB\\Script\\HamiltonVisualMethodEditor\\Server.py" 65535'
    )
