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

def get_slice(string_to_slice, slice_index_list):
    # We're slicing a string, so the list should only have the start and stop of the slice.
    assert len(slice_index_list) == 2
    i1 = slice_index_list[0]
    i2 = slice_index_list[1]
    return str(string_to_slice)[i1:i2]

def pretty_print_slice(string_to_slice, slice_index_list):
    assert len(slice_index_list) == 2
    i1 = slice_index_list[0]
    i2 = slice_index_list[1]
    assert i2 > i1
    print " "*i1 + str(string_to_slice)[i1:i2]
    print string_to_slice
    print ' '*i1 + '^' + ' '*(i2-i1-2) + '^'

def find_slice(string, substring):
    # TODO: find all the slices, not just the first one.
    if substring not in string:
        return None
    else:
        start = string.find(substring)
        stop = start + len(substring)
        return [start, stop]

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
                        print "Suggested slice:", str(find_slice(invocation_dict['string'], arg))
                        pretty_print_slice(invocation_dict['string'], find_slice(invocation_dict['string'], arg))
                        raise
        if 'can-affect' in invocation_dict.keys():
            for key in invocation_dict['can-affect']:
                true_false = invocation_dict['can-affect'][key]
                assert type(true_false) == bool, true_false+" is not a boolean."

# TODO: check all the commands in component commands are substrings of the main command.
# TODO: check that the commands in component-command-info
# TODO: check that bash-type is one of `keyword', `builtin', or `file'.
# TODO: check debian-path is correct using `which`.
# TODO: make a proper JSON schema to check the types are correct.
