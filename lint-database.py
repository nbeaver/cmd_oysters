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

def check_bytes(string, nominal_bytes):
    calculated_bytes = len(string)
    assert nominal_bytes == calculated_bytes, \
        "String lengths do not match: %d != %d\n%s" \
        % (nominal_bytes, calculated_bytes, string)

def prompt_sha1(string):
    sys.stderr("No SHA1 for `" + string + "'")
    sys.stderr("Should be: "+hashlib.sha1(string).hexdigest())

def prompt_bytes(string):
    sys.stderr("No bytes for `" + string + "'")
    sys.stderr("Should be: "+len(string))

def get_slice(string_to_slice, slice_index_list):
    # We're slicing a string, so the list should only have the start and stop of the slice.
    assert len(slice_index_list) == 2
    i1 = int(slice_index_list[0])
    i2 = int(slice_index_list[1])
    return str(string_to_slice)[i1:i2]

def pretty_print_slice(string_to_slice, slice_index_list):
    assert len(slice_index_list) == 2
    i1 = int(slice_index_list[0])
    i2 = int(slice_index_list[1])
    assert i2 > i1
    print " "*i1 + str(string_to_slice)[i1:i2]
    print string_to_slice
    print ' '*i1 + '^' + ' '*(i2-i1-2) + '^'

for command in commands:
    assert 'description' in command.keys(), "Error: no description."
    assert 'string' in command['description'].keys(), "Error: no description string."

    try:
        check_bytes(command['description']['string'],
                   int(command['description']['bytes']))
    except KeyError:
        prompt_bytes(command['description']['string'])

    try:
        check_sha1(command['description']['string'],
                   command['description']['sha1hex'])
    except KeyError:
        prompt_sha1(command['description']['string'])

    invocations = command['invocations'].keys()
    for shell in invocations:

        invocation_dict = command['invocations'][shell]

        if 'bytes' in invocation_dict.keys():
            check_bytes(invocation_dict['string'], int(invocation_dict['bytes']))

        try:
            check_sha1(invocation_dict['string'], invocation_dict['sha1hex'])
        except KeyError:
            prompt_sha1(invocation_dict['string'])

        if 'changeable-arguments' in invocation_dict.keys():
            arg_dict = invocation_dict['changeable-arguments']
            if arg_dict:
                for arg, arginfo in arg_dict.iteritems():
                    # Check that the argument actually matches the sliced command.
                    arg_slice = get_slice(invocation_dict['string'], arginfo['invocation-slice'])
                    try:
                        assert arg == arg_slice, "arg is:\n'"+arg+"'\nbut slice is:\n'"+arg_slice+"'"
                    except AssertionError:
                        pretty_print_slice(invocation_dict['string'], arginfo['invocation-slice'])
                        raise

# TODO: check all the commands in component commands are substrings of the main command.
# TODO: check that the commands in component-command-info
# TODO: check that bash-type is one of `keyword', `builtin', or `file'.
# TODO: check debian-path is correct using `which`.
