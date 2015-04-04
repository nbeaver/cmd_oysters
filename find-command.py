#! /usr/bin/env python
import json
import sys

match_string = ''.join(sys.argv[1:])

with open("command-database.json") as db_file:
    commands = json.load(db_file)

# TODO: take --commands argument and search in component commands.

for command in commands:
    invocations = command['invocations'].keys()
    for shell in invocations:
        command_string = command['invocations'][shell]['string']
        if match_string in command_string:
            print command_string
