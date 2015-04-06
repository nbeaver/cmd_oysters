#! /usr/bin/env python
import json
import sys
import argparse

parser = argparse.ArgumentParser(description='search for shell commands')
parser.add_argument('-c', '--commands', help='component command search', required=False, nargs='+')
parser.add_argument('-s', '--substring', help='simple substring search', required=False)
parser.add_argument('-t', '--token-substring', help='unordered token subset search',required=False, nargs='+')
parser.add_argument('-d', '--database', help='path to database file', required=False, default="command-database.json")
args = parser.parse_args()

with open(args.database) as db_file:
    commands = json.load(db_file)

# TODO: take --commands argument and search in component commands.
# TODO: take multiple arguments to --substring so it's effectively a regex search for 'arg1.*arg2.*arg3'

for command in commands:
    invocations = command['invocations'].keys()
    for invocation in invocations:
        command_string = command['invocations'][invocation]['string']
        if args.substring in command_string:
            print command_string
