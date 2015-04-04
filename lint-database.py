#! /usr/bin/env python
import json
import hashlib
import sys

if len(sys.argv) == 1:
    print "Usage: python lint-database.py database.json"
    sys.exit(1)

with open(sys.argv[1]) as db_file:
    commands = json.load(db_file)

def check_sha1(string, nominal_sha1):
    calculated_sha1 = hashlib.sha1(string).hexdigest()
    assert nominal_sha1 == calculated_sha1, \
        "SHA1s do not match:\n%s (in database)\n%s (calculated)\n%r (command representation)" \
        % (nominal_sha1, calculated_sha1, string)

def prompt_sha1(string):
    sys.stderr("No SHA1 for `" + string + "'")
    sys.stderr("Should be: "+hashlib.sha1(string).hexdigest())

def check_len(string, nominal_len):
    calculated_len = len(invocation_dict['string'])
    assert nominal_len == calculated_len, \
        "String lengths do not match: %d != %d\n%s" \
        % (nominal_len, calculated_len, string)

def get_slice(string_to_slice, slice_index_list):
    # We're slicing a string, so the list should only have the start and stop of the slice.
    assert len(slice_index_list) == 2
    i1 = int(slice_index_list[0])
    i2 = int(slice_index_list[1])
    return str(string_to_slice)[i1:i2]

for command in commands:
    assert 'description' in command.keys(), "Error: no description."
    assert 'string' in command['description'].keys(), "Error: no description string."

    try:
        check_sha1(command['description']['string'],
                   command['description']['sha1hex'])
    except KeyError:
        prompt_sha1(command['description']['string'])

    invocations = command['invocations'].keys()
    for shell in invocations:

        invocation_dict = command['invocations'][shell]

        if 'bytes' in invocation_dict.keys():
            check_len(invocation_dict['string'], int(invocation_dict['bytes']))

        try:
            check_sha1(invocation_dict['string'], invocation_dict['sha1hex'])
        except KeyError:
            prompt_sha1(invocation_dict['string'])

        if 'changeable-arguments' in invocation_dict.keys():
            arg_dict = invocation_dict['changeable-arguments']
            if arg_dict:
                for arg, arginfo in arg_dict.iteritems():
                    # Check that the argument actually matches the sliced command.
                    assert arg == get_slice(invocation_dict['string'], arginfo['invocation-slice'])
                    if 'invocation-long-flags' in command.keys():
                        assert arg == get_slice(command['invocation-long-flags']['string'], arginfo['invocation-long-flags-slice'])

# TODO: check all the commands in component commands are substrings of the main command.
# TODO: check that the commands in component-command-info
