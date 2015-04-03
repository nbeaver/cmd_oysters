#! /usr/bin/env python
import json
import os

with open("command-database.json") as db_file:
    commands = json.load(db_file)

def generic_child(child_list):
    # If the child starts with '$',
    # e.g. "$COMMAND",
    # it is generic.
    if len(child_list) == 1 and child_list[0][0] == '$':
        return child_list[0]
    else:
        return None

def check_pseudoschema(parent, directory, trace_path=""):
    try:
        children = parent.keys()
        known_children = os.listdir(directory)
    except AttributeError:
        return

    for child in children:

        new_parent = parent[child]

        if generic_child(known_children):
            new_path = os.path.join(directory,generic_child(known_children))
        else:
            new_path = os.path.join(directory, child)
        
        if child in known_children or generic_child(known_children):
            check_pseudoschema(new_parent, new_path, trace_path+":"+child)
        else:
            # TODO: should this halt the script or not?
            print "Error: `"+trace_path+":"+child+"' not in",str(known_children),"in",directory
            # TODO: Can this trace back to the line of the original JSON file?
            return False

for command in commands:
    check_pseudoschema(command, "./pseudo-schema")
