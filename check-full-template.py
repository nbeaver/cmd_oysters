#! /usr/bin/env python2
import json
import os
import sys

if len(sys.argv) == 1:
    print "Usage: python check-full-template.py full-command-template.json pseudo-schema"
    sys.exit(1)

json_file = sys.argv[1]
command = json.load(open(json_file))
    
pseudoschema_root = sys.argv[2]
if not os.path.isdir(pseudoschema_root):
    print "`"+pseudoschema_root+"' is not a directory or does not exist."
    sys.exit(1)

def validate(path, json_object):
    for child in os.listdir(path):
        child_path = os.path.join(path, child)
        try:
            # An object.
            assert child in json_object, child_path+" not in "+json_file+"\nkeys: "+repr(json_object.keys())
        except AttributeError:
            # A list of objects.
            for item in json_object:
                assert child in item, child_path+" not in "+json_file+"\nlist item: "+repr(item)

        if os.path.isdir(child_path):
            validate(child_path, json_object[child])

validate(pseudoschema_root, command)
