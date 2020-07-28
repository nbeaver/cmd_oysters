#! /usr/bin/env python3
from __future__ import print_function
import json
import os
import glob
import sys
import argparse
import string


class QueryInfo:
    pass


def tokenize(text):
    """Strip punctuation from free text sentences and split into tokens."""
    table = {ord(punc): None for punc in string.punctuation}
    return text.translate(table).split()


def lowercase_subset(A, B):
    """Check that A is a subset of B when case is ignored."""
    set_a = set([a.lower() for a in A])
    set_b = set([b.lower() for b in B])
    return set_a.issubset(set_b)

def display_invocation(invocation):
    try :
        comment = invocation["comment"]
        for line in comment.splitlines():
            yield "# " + line
    except KeyError:
        pass
    yield invocation["invocation-string"]

def print_oysters(topdir, query):
    json_filepaths = glob.glob(topdir + "/*.json")
    for filepath in json_filepaths:
        with open(os.path.join(topdir, filepath)) as json_file:
            try:
                oyster = json.load(json_file)
            except ValueError:
                sys.stderr.write("Invalid JSON for file: `{}'\n".format(
                    json_file.name))
                raise

        if query.commands:
            if not set(query.commands).issubset(
                    set(oyster['component-commands'])):
                # The command list is not a subset of the component commands,
                # so try next oyster.
                continue

        if query.description:
            if not query.description.lower(
            ) in oyster['description']['verbose-description'].lower():
                continue

        if query.description_tokens:
            if not lowercase_subset(
                    query.description_tokens,
                    tokenize(oyster['description']['verbose-description'])):
                continue

        matching_invocations = []
        for invocation in oyster['invocations']:
            try:
                invocation_string = invocation['invocation-string']
            except KeyError:
                sys.stderr.write(
                    "Error: no 'invocation-string' in file `{}'\n".format(
                        json_file.name))
                raise

            if query.substring:
                if not query.substring in invocation_string:
                    # This doesn't match, so try the next invocation.
                    continue
            if query.tokens:
                invocation_tokens = invocation_string.split()
                if not set(query.tokens).issubset(set(invocation_tokens)):
                    # At least one of the query tokens doesn't match,
                    # so try the next invocation.
                    continue
            # At this point, the command must be a match.
            matching_invocations.append(invocation)

        if len(matching_invocations) > 0:
            print('# ' + filepath)
            print('# ' + oyster['description']['verbose-description'])
        for matching_invocation in matching_invocations:
            for line in display_invocation(matching_invocation):
                print(line)

def main():
    parser = argparse.ArgumentParser(description='search CmdOysters')
    parser.add_argument(
        '-c',
        '--commands',
        help='component command search',
        required=False,
        nargs='+')
    parser.add_argument(
        '-s',
        '--substring',
        help='simple command substring search',
        required=False)
    parser.add_argument(
        '-t',
        '--tokens',
        help='unordered token subset command search',
        required=False,
        nargs='+')
    parser.add_argument(
        '-d', '--description', help='command description', required=False)
    parser.add_argument(
        '-D',
        '--description-tokens',
        help='description token search (case-insensitive)',
        required=False,
        nargs='+')

    default_json_path = os.path.join(
        sys.path[0],
        "cmdoysters")  # need to do it this way for symlinks to work.
    parser.add_argument(
        '-j',
        '--json',
        help='path to root directory of JSON input files',
        required=False,
        default=default_json_path)

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    cmd_query = QueryInfo()
    cmd_query.commands = args.commands
    cmd_query.substring = args.substring
    cmd_query.tokens = args.tokens
    cmd_query.description = args.description
    cmd_query.description_tokens = args.description_tokens

    print_oysters(args.json, cmd_query)

if __name__ == '__main__':
    main()
