#! /usr/bin/env python
import json
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='search for shell commands')
parser.add_argument('-c', '--commands', help='component command search', required=False, nargs='+')
parser.add_argument('-s', '--substring', help='simple substring search', required=False)
parser.add_argument('-t', '--tokens', help='unordered token subset search',required=False, nargs='+')
parser.add_argument('-d', '--description', help='command description', required=False)

default_json_file = os.path.join(sys.path[0],"command-database.json") # need to do it this way for symlinks to work.
parser.add_argument('-j', '--json', help='path to JSON input file', required=False, default=default_json_file)

args = parser.parse_args()

with open(args.json) as db_file:
    commands = json.load(db_file)

for command in commands:
    if args.commands:
        if not set(args.commands).issubset(set(command['component-commands'])):
            # The command list is not a subset of the component commands,
            # so try next command.
            continue
    if args.description:
        if not args.description in command['description']['string']:
            continue
    for invocation in command['invocations'].keys():
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
        if args.description:
            print '# ' + command['description']['string']
        print command_string

# DONE: take --commands argument and search in component commands.
# TODO: take multiple arguments to --substring so it's effectively a regex search for 'arg1.*arg2.*arg3'
# TODO: make the description search case-insensitive.
# TODO: make the description search into a full regex search.
# TODO: do some unit tests instead of the hacky makefile tests.
