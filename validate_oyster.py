#! /usr/bin/env python2
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

def pretty_print_slice(string_to_slice, slice_index_list):
    assert len(slice_index_list) == 2
    i1 = slice_index_list[0]
    i2 = slice_index_list[1]
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
        return [start, stop]


def validate_command(command, uuid_from_filename, oyster_path):

    def assert_custom(assertion, error_string):
        try:
            assert assertion, error_string
        except AssertionError:
            sys.stderr.write("Error in file: "+ oyster_path+'\n')
            raise

    def assert_subset(subset, superset):
        assert_custom(subset.issubset(superset), repr(subset)+ "is not a subset of " + repr(superset))

    def assert_in(A, B):
        assert_custom(A in B, repr(A)+ "is not in " + repr(B))

    if 'component-command-info' in command.keys():

        assert_subset(set(command['component-command-info'].keys()), set(command['component-commands']))

        for command_name, info in command['component-command-info'].iteritems():
            for info_key, info_item in info.iteritems():

                if info_key == 'debian':
                    if 'executable-path' in info_item.keys() and info_item['executable-path']:
                        # e.g. `ls` is in `/bin/ls`
                        assert_in(command_name, info_item['executable-path'])

    if uuid_from_filename != command['uuid']:
            sys.stderr.write("Warning in file: "+ oyster_path+'\n')
            sys.stderr.write("Filename does not match UUID. Should be: {}.json\n".format(command['uuid']))

    def validate_invocation(invocation):

        if 'changeable-arguments' in invocation_dict.keys():
            arg_dict = invocation_dict['changeable-arguments']
            if arg_dict:
                for arg, arginfo in arg_dict.iteritems():
                    # Check that the argument actually matches the sliced command.
                    arg_slice = get_slice(invocation_dict['invocation-string'], arginfo['invocation-slice'])
                    try:
                        assert_custom(arg == arg_slice, "arg is:\n'"+arg+"'\nbut slice is:\n'"+arg_slice+"'")
                    except AssertionError:
                        pretty_print_slice(invocation_dict['invocation-string'], arginfo['invocation-slice'])
                        slice_candidate = find_slice(invocation_dict['invocation-string'], arg)
                        if slice_candidate:
                            sys.stderr.write("Slice in file:"+ str(arginfo['invocation-slice'])+'\n')
                            sys.stderr.write("Suggested slice:"+ str(slice_candidate)+'\n')
                            sys.stderr.write(pretty_print_slice(invocation_dict['invocation-string'], slice_candidate))
                        raise
                    if 'component-command' in arginfo.keys():
                        assert_in(arginfo['component-command'], command['component-commands'])
        for component_command in command['component-commands']:
            assert_in(component_command, invocation_dict['invocation-string'])

    for invocation_dict in command['invocations']:
        validate_invocation(invocation_dict)

def main(oyster_path, schema_path):

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
            validate_command(oyster, basename_no_extension, oyster_path)

if __name__ == '__main__':
    num_args = len(sys.argv) - 1
    if num_args != 2:
        sys.stderr.write("Usage: python "+sys.argv[0]+" cmd-oyster.json schema.json"+'\n')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
