#! /usr/bin/env python
import json
import sys

match_string = ''.join(sys.argv[1:])

with open("command-database.json") as db_file:
    commands = json.load(db_file)

for command in commands:
    command_string = command['invocation']['string']
    if match_string in command_string:
        print command_string
