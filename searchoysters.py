#! /usr/bin/env python
from __future__ import print_function
import json
import os
import glob
import sys
import argparse
import string

def tokenize(text):
    """Strip punctuation from free text sentences and split into tokens."""
    table = {ord(punc): None for punc in string.punctuation}
    return text.translate(table).split()

def lowercase_subset(A, B):
    """Check that A is a subset of B when case is ignored."""
    set_a = set([a.lower() for a in A])
    set_b = set([b.lower() for b in B])
    return set_a.issubset(set_b)

parser = argparse.ArgumentParser(description='search CmdOysters')
parser.add_argument('-c', '--commands', help='component command search', required=False, nargs='+')
parser.add_argument('-s', '--substring', help='simple command substring search', required=False)
parser.add_argument('-t', '--tokens', help='unordered token subset command search',required=False, nargs='+')
parser.add_argument('-d', '--description', help='command description', required=False)
parser.add_argument('-D', '--description-tokens', help='description token search (case-insensitive)', required=False, nargs='+')

default_json_path = os.path.join(sys.path[0],"cmdoysters") # need to do it this way for symlinks to work.
parser.add_argument('-j', '--json', help='path to root directory of JSON input files', required=False, default=default_json_path)

args = parser.parse_args()

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

json_filepaths = glob.glob(args.json + "/*.json")
for filepath in json_filepaths:
    with open(os.path.join(args.json, filepath)) as json_file:
        try:
            command = json.load(json_file)
        except ValueError:
            sys.stderr.write("Invalid JSON for file: `{}'\n".format(json_file.name))

    if args.commands:
        if not set(args.commands).issubset(set(command['component-commands'])):
            # The command list is not a subset of the component commands,
            # so try next command.
            continue

    if args.description:
        if not args.description.lower() in command['description']['verbose-description'].lower():
            continue

    if args.description_tokens:
        if not lowercase_subset(args.description_tokens, tokenize(command['description']['verbose-description'])):
            continue

    matching_invocations = []
    for invocation in command['invocations']:
        invocation_string = invocation['invocation-string']
        if args.substring:
            if not args.substring in invocation_string :
                # This doesn't match, so try the next invocation.
                continue
        if args.tokens:
            invocation_tokens = invocation_string.split()
            if not set(args.tokens).issubset(set(invocation_tokens)):
                # At least one of the query tokens doesn't match,
                # so try the next invocation.
                continue
        # At this point, the command must be a match.
        if 'comment' in invocation.keys():
            matching_invocations.append((invocation_string, invocation['comment']))
        else:
            matching_invocations.append((invocation_string, None))


    if len(matching_invocations) > 0:
        print('# ' + filepath)
        # TODO: break the description on 80 lines (without splitting words),
        # and add a comment character at each point.
        print('# ' + command['description']['verbose-description'])
        for invocation_string, comment in matching_invocations:
            if comment:
                print('# ' + comment)
            print(invocation_string)
