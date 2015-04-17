#! /usr/bin/env python2
import json
import os
import sys

def is_wildcard_field(child_name):
    # If the child starts with '$',
    # e.g. "$COMMAND",
    # it is a wildcard.
    if child_name[0] == '$':
        return True
    else:
        return False

def check_pseudoschema(parent_json, parent_pseudoschema, trace_path=""):
    try:
        children_json = parent_json.keys()
    except AttributeError:
        # Stop recursing, since the JSON object doesn't have child objects.
        return

    children_pseudoschema = os.listdir(parent_pseudoschema)
    if len(children_pseudoschema) == 1 and is_wildcard_field(children_pseudoschema[0]):
        # This is a wildcard in the schema, so just continue recursing.
        for child_json in children_json:
            next_path = os.path.join(parent_pseudoschema, children_pseudoschema[0])
            check_pseudoschema(parent_json[child_json], next_path, trace_path+":"+child_json)
    else:
        for child_json in children_json:
            # We're only checking that the JSON child objects are in the pseudoschema;
            # if the JSON doesn't have all of the pseudoschema, that's ok.
            if child_json in children_pseudoschema:
                next_path = os.path.join(parent_pseudoschema, child_json)
                check_pseudoschema(parent_json[child_json], next_path, trace_path+":"+child_json)
            else:
                raise ValueError, "Input does not match pseudoschema: `"+trace_path+":"+child_json+"' not one of "+str(children_pseudoschema)+" in "+parent_pseudoschema
                # TODO: Figure out a way to trace back to the line of the original JSON file. Will be hard, since we've already parsed the JSON.

if len(sys.argv) == 1:
    print "Usage: python check-pseudoschema.py database.json"
    sys.exit(1)

root_directory = sys.argv[1]
json_filenames = os.listdir(root_directory)
for i, filename in enumerate(json_filenames):
    with open(os.path.join(root_directory, filename)) as json_file:
        try:
            json_data = json.load(json_file)
        except:
            print "Invalid JSON for file: `"+filename+"'"
            raise
        check_pseudoschema(json_data, "pseudo-schema/")
