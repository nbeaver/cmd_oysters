#! /usr/bin/env python
import json
import os
import sys

if len(sys.argv) == 1:
    print "Usage: python check-full-template.py full-command-template.json pseudo-schema"
    sys.exit(1)

with open(sys.argv[1]) as json_file:
    commands = json.load(json_file)
    
pseudoschema_root = sys.argv[2]
if not os.path.isdir(pseudoschema_root):
    print "`"+pseudoschema_root+"' is not a directory or does not exist."
    sys.exit(1)

def validate(directory, json_object, trace):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
                assert filename in json_object.keys(), os.path.join(trace,filename)+" is not in "+str(json_object.keys())

        for dirname in dirnames:
            assert dirname in json_object.keys()
            validate(dirname, json_object[dirname], os.path.join(trace, dirname))

for command in commands:
    validate(pseudoschema_root, command, pseudoschema_root)
