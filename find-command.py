#! /usr/bin/env python
import json
import sys
import argparse

parser = argparse.ArgumentParser(description='search for shell commands')
parser.add_argument('-c', '--commands', help='component command search', required=False, nargs='+')
parser.add_argument('-s', '--substring', help='simple substring search', required=False)
parser.add_argument('-t', '--tokens', help='unordered token subset search',required=False, nargs='+')
parser.add_argument('-d', '--database', help='path to database file', required=False, default="command-database.json")
args = parser.parse_args()

with open(args.database) as db_file:
    commands = json.load(db_file)

# DONE: take --commands argument and search in component commands.
# TODO: take multiple arguments to --substring so it's effectively a regex search for 'arg1.*arg2.*arg3'

for command in commands:
    component_commands = command['component-commands']
    if args.commands:
        if not set(args.commands).issubset(set(component_commands)):
            # The command list is not a subset of the component commands,
            # so try next command.
            continue
    invocations = command['invocations'].keys()
    for invocation in invocations:
        command_string = command['invocations'][invocation]['string']
        if args.substring:
            if not args.substring in command_string:
                # This doesn't match, so try the next invocation.
                continue
        if args.tokens:
            invocation_tokens = command_string.split()
            if not set(args.tokens).issubset(set(invocation_tokens)):
                # At least one of the query tokens doesn't match,
                # so try the next invocation.
                continue
        # At this point, the command must be a match.
        print command_string
