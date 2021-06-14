import yaml

file  = open("Tools\\Configuration\\Sequences.yaml")

Contents = yaml.full_load(file)
import json
print(json.dumps(Contents, indent=2))