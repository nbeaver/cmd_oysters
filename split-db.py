import json
import os

commands = json.load(open("command-database.json"))
for command in commands:
    f = open("command-database/"+command['description']['sha1hex']+".json", 'w')
    json.dump(command, f, indent=4, sort_keys=True)
    f.close()
