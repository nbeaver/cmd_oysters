#! /usr/bin/env python
import json
import jsonschema
import sys
import os

def get_slice(string_to_slice, slice_index_list):
    # We're slicing a string, so the list should only have the start and stop of the slice.
    assert len(slice_index_list) == 2
    i1 = slice_index_list[0]
    i2 = slice_index_list[1]
    return str(string_to_slice)[i1:i2]

def pretty_print_slice(string_to_slice, slice_indices):
    assert len(slice_indices) == 2
    i1, i2 = slice_indices
    assert i2 > i1
    slice_string = ""
    slice_string += ' '*i1 + str(string_to_slice)[i1:i2] + '\n'
    slice_string += string_to_slice + '\n'
    slice_string += ' '*i1 + '^' + ' '*(i2-i1-2) + '^\n'
    return slice_string

def find_slice(string, substring):
    # TODO: find all the slices, not just the first one.
    if substring not in string:
        return None
    else:
        start = string.find(substring)
        stop = start + len(substring)
        return (start, stop)

def assert_with_path(assertion, error_string):
    try:
        assert assertion, error_string
    except AssertionError:
        sys.stderr.write("Error in file: "+ filepath +'\n')
        raise

def assert_subset(subset, superset):
    assert_with_path(subset.issubset(superset), repr(subset)+ "is not a subset of " + repr(superset))

def assert_in(A, B):
    assert_with_path(A in B, repr(A)+ "is not in " + repr(B))

def validate_invocation(invocation, component_commands):
    if 'changeable-arguments' in invocation:
        arg_dict = invocation['changeable-arguments']
        if arg_dict:
            for arg, arginfo in arg_dict.iteritems():
                # Check that the argument actually matches the sliced command.
                arg_slice = get_slice(invocation['invocation-string'], arginfo['invocation-slice'])
                try:
                    assert_with_path(arg == arg_slice, "arg is:\n'"+arg+"'\nbut slice is:\n'"+arg_slice+"'")
                except AssertionError:
                    pretty_print_slice(invocation['invocation-string'], arginfo['invocation-slice'])
                    slice_candidate = find_slice(invocation['invocation-string'], arg)
                    if slice_candidate:
                        sys.stderr.write("Slice in file:"+ str(arginfo['invocation-slice'])+'\n')
                        sys.stderr.write("Suggested slice:"+ str(slice_candidate)+'\n')
                        sys.stderr.write(pretty_print_slice(invocation['invocation-string'], slice_candidate))
                    raise

                if 'component-command' in arginfo:
                    assert_in(arginfo['component-command'], component_commands)

                if 'component-command-flag' in arginfo:
                    assert_in(arginfo['component-command-flag'], invocation['invocation-string'])

    for component_command in component_commands:
        assert_in(component_command, invocation['invocation-string'])


def validate_oyster(oyster, uuid_from_filename):

    if 'component-command-info' in oyster:

        assert_subset(set(oyster['component-command-info'].keys()), set(oyster['component-commands']))

        for command_name, info in oyster['component-command-info'].iteritems():
            for info_key, info_item in info.iteritems():

                if info_key == 'debian':
                    if 'executable-path' in info_item and info_item['executable-path']:
                        # e.g. `ls` is in `/bin/ls`
                        assert_in(command_name, info_item['executable-path'])

    if uuid_from_filename != oyster['uuid']:
            sys.stderr.write("Warning in file: "+ filepath+'\n')
            sys.stderr.write("Filename does not match UUID. Should be: {}.json\n".format(oyster['uuid']))

    for invocation_dict in oyster['invocations']:
        validate_invocation(invocation_dict, oyster['component-commands'])

def main(oyster_path, schema_path):

    global filepath

    filepath = oyster_path

    with open(schema_path) as schema_file:
            try:
                oyster_schema = json.load(schema_file)
            except:
                sys.stderr.write("Invalid JSON in schema: `"+schema_file.name+"'"+'\n')
                raise

    with open(oyster_path) as json_file:
            try:
                oyster = json.load(json_file)
            except:
                sys.stderr.write("Invalid JSON in file: `"+json_file.name+"'"+'\n')
                raise
            try:
                jsonschema.validate(oyster, oyster_schema)
            except jsonschema.exceptions.ValidationError:
                sys.stderr.write(json_file.name+'\n')
                raise
            basename_no_extension = os.path.splitext(os.path.basename(json_file.name))[0]
            validate_oyster(oyster, basename_no_extension)

# It's easier to make this a global variable
# than to thread it through every function.
filepath = None

if __name__ == '__main__':
    num_args = len(sys.argv) - 1
    if num_args != 2:
        sys.stderr.write("Usage: python "+sys.argv[0]+" cmd-oyster.json schema.json"+'\n')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
