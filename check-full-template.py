#! /usr/bin/env python
import json
import os
import sys

if len(sys.argv) == 1:
    print "Usage: python check-full-template.py full-command-template.json pseudo-schema"
    sys.exit(1)

json_file = sys.argv[1]
commands = json.load(open(json_file))
    
pseudoschema_root = sys.argv[2]
if not os.path.isdir(pseudoschema_root):
    print "`"+pseudoschema_root+"' is not a directory or does not exist."
    sys.exit(1)

def validate(path, json_object):
    for child in os.listdir(path):
        child_path = os.path.join(path, child)
        assert child in json_object.keys(), child_path+" not in "+json_file+"\nkeys: "+str(json_object.keys())
        if os.path.isdir(child_path):
            validate(child_path, json_object[child])

for command in commands:
    validate(pseudoschema_root, command)
