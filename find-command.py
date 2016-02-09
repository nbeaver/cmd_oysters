#! /usr/bin/env python2
import json
import os
import glob
import sys
import argparse
import string

def tokens(text):
    return text.encode('utf-8').translate(None, string.punctuation).split()

def lowercase_subset(A, B):
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

json_filenames = glob.glob(args.json + "/*.json")
for filename in json_filenames:
    with open(os.path.join(args.json, filename)) as json_file:
        try:
            command = json.load(json_file)
        except ValueError:
            print "Invalid JSON for file: `"+json_file.name+"'"

    if args.commands:
        if not set(args.commands).issubset(set(command['component-commands'])):
            # The command list is not a subset of the component commands,
            # so try next command.
            continue

    if args.description:
        if not args.description.lower() in command['description']['string'].lower():
            continue

    if args.description_tokens:
        if not lowercase_subset(args.description_tokens, tokens(command['description']['string'])):
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
        print '# ' + filename
        # TODO: break the description on 80 lines (without splitting words),
        # and add a comment character at each point.
        print '# ' + command['description']['string']
        for invocation_string, comment in matching_invocations:
            if comment:
                print '# ' + comment
            print invocation_string
