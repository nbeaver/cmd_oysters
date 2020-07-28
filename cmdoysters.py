#! /usr/bin/env python3
from __future__ import print_function
import json
import os
import glob
import sys
import argparse
import string
import logging

class QueryInfo:
    def __dict__(self):
        info_dict = {
            "commands" : self.commands,
            "substring" : self.substring,
            "tokens": self.tokens,
            "description": self.description,
            "description_tokens": self.description_tokens,
        }
        return info_dict

    def __repr__(self):
        return str(self.__dict__())

    def __str__(self):
        info = ''
        info += "commands = {}\n".format(self.commands)
        info += "substring = {}\n".format(self.substring)
        info += "tokens = {}\n".format(self.tokens)
        info += "description = {}\n".format(self.description)
        info += "description_tokens = {}\n".format(self.description_tokens)
        return info

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
    try :
        example_outputs = invocation["example-outputs"]
        for i, output in enumerate(example_outputs):
            yield "# Example output:".format(i+1)
            for line in output.splitlines():
                yield line
    except KeyError:
        pass

def oyster_matches(oyster, query):
    if query.commands:
        if not set(query.commands).issubset(
                set(oyster['component-commands'])):
            # The command list is not a subset of the component commands,
            # so it's not a match.
            return False

    if query.description:
        if not query.description.lower(
        ) in oyster['description']['verbose-description'].lower():
            return False

    if query.description_tokens:
        if not lowercase_subset(
                query.description_tokens,
                tokenize(oyster['description']['verbose-description'])):
            return False

    return True

def invocation_matches(invocation, query):
    invocation_string = invocation['invocation-string']
    if query.substring:
        if not query.substring in invocation_string:
            # The substring isn't in the invocation,
            # so it doesn't match.
            return False
    if query.tokens:
        invocation_tokens = invocation_string.split()
        if not set(query.tokens).issubset(set(invocation_tokens)):
            # At least one of the query tokens doesn't match.
            return False
    # At this point, the command invocation must be a match.
    return True

def get_matching_invocations(oyster, query):
    matching_invocations = []
    for invocation in oyster['invocations']:
        if invocation_matches(invocation, query):
            matching_invocations.append(invocation)
    return matching_invocations

def print_oysters(topdir, query):
    json_filepaths = glob.glob(topdir + "/*.json")
    for filepath in json_filepaths:
        with open(os.path.join(topdir, filepath)) as json_file:
            try:
                oyster = json.load(json_file)
            except ValueError:
                logging.error("Invalid JSON for file: '{}'".format(json_file.name))
                raise

        if not oyster_matches(oyster, query):
            # Try next oyster.
            continue

        try:
            matching_invocations = get_matching_invocations(oyster, query)
        except KeyError:
            logging.error("in file '{}'".format(json_file.name))
            raise
        except IndexError:
            logging.error("in file '{}'".format(json_file.name))
            raise

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
        help="component command search (case-sensitive, order doesn't matter)",
        nargs='+')
    parser.add_argument(
        '-s',
        '--substring',
        help='command substring search (case-sensitive, order matters)',
        nargs=1)
    parser.add_argument(
        '-t',
        '--tokens',
        help="command token subset command search (case-sensitive, order doesn't matter)",
        nargs='+')
    parser.add_argument(
        '-d',
        '--description',
        help="description substring search (case-insensitive, order matters)",
        nargs=1)
    parser.add_argument(
        '-D',
        '--description-tokens',
        help="description token search (case-insensitive, order doesn't matter)",
        nargs='+')

    default_json_path = os.path.join(
        sys.path[0],
        "cmdoysters")  # need to do it this way for symlinks to work.
    parser.add_argument(
        '-j',
        '--json',
        help='path to root directory of JSON input files',
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
