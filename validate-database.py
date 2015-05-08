#! /usr/bin/env python2
import json
import hashlib
import sys
import os
import glob
import traceback

try:
    import nilsimsa
except ImportError:
    pass


class NoDuplicates:
    def __init__(self, iterable=[]):
        self.set = set()
        for elem in iterable:
            if elem in self.set:
                raise RuntimeError("Duplicate element: "+repr(elem))
            else:
                self.set.add(elem)
    def add(self, elem):
        if elem in self.set:
            raise RuntimeError("Duplicate element: "+repr(elem))
        else:
            self.set.add(elem)

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

def count_invocations(command):
    return len(command['invocations'].keys())

def validate_command(command, expected_description_SHA1):

    def assert_custom(assertion, error_string):
        try:
            assert assertion, error_string
        except AssertionError:
            print "Error in file:", json_filepath
            traceback.print_exc()
            raise

    def assert_custom_warn_only(assertion, error_string):
        if assertion:
            return
        else:
            print "Warning in file: ", json_filepath
            print error_string
            pass

    def assert_subset(subset, superset):
        assert_custom(subset.issubset(superset), repr(subset)+ "is not a subset of " + repr(superset))

    def assert_in(A, B):
        assert_custom(A in B, repr(A)+ "is not in " + repr(B))


    # Required fields.
    def required_field(field, field_list):
        assert_custom(field in field_list, "Error: required field `"+field+"` not in "+repr(field_list))

    required_field('description', command)
    required_field('string', command['description'])

    def recommended_field(field, field_list=None):
        if field_list:
            assert_custom_warn_only(field in field_list, "Warning: recommended field `"+field+"` not in "+repr(field_list))
        else:
            assert_custom_warn_only(False, "Warning: recommended field `"+field+"` not present.")
    try:
        # We don't need .keys(), but it makes the warnings less verbose.
        recommended_field('authors', command['copying'].keys())
        recommended_field('license-name', command['copying'].keys())
        recommended_field('license-url', command['copying'].keys())
        recommended_field('year', command['copying'].keys())
    except KeyError:
        recommended_field('copying')

    def check_sha1(string, nominal_sha1):
        calculated_sha1 = hashlib.sha1(string).hexdigest()
        assert_custom(nominal_sha1 == calculated_sha1, \
            "SHA1s do not match:\n%s (in file)\n%s (calculated)\n%r (command representation)" \
            % (nominal_sha1, calculated_sha1, string))

    def supply_sha1(string):
        sys.stderr.write("Warning: No SHA1 for `" + string + "'")
        sys.stderr.write("Should be: "+hashlib.sha1(string).hexdigest())

    if 'nilsimsa' in sys.modules:
        def check_nilsimsa(string, nominal_nilsimsa):
            calculated_nilsimsa = nilsimsa.Nilsimsa(string).hexdigest()
            assert_custom_warn_only(nominal_nilsimsa == calculated_nilsimsa, \
                "nilsimsas do not match:\n%s (in file)\n%s (calculated)\n%r (command representation)" \
                % (nominal_nilsimsa, calculated_nilsimsa, string))

        def supply_nilsimsa(string):
            assert_custom_warn_only(False, \
                "No nilsimsa for `" + string + "'\n"+\
                "Should be: "+nilsimsa.Nilsimsa(string).hexdigest()+"\n")

    if 'component-command-info' in command.keys():
        #TODO: make this less of a horrific mess.

        assert_subset(set(command['component-command-info'].keys()), set(command['component-commands']))

        for command_name, info in command['component-command-info'].iteritems():
            for info_key, info_item in info.iteritems():
                if info_key == 'bash-type':
                    bash_types = set(['alias', 'builtin', 'file', 'function', 'keyword',"builtin | keyword | file"])
                    assert_in(info_item, bash_types)

                elif info_key == 'debian':
                    if 'executable-path' in info_item.keys() and info_item['executable-path']:
                        # e.g. `ls` is in `/bin/ls`
                        assert_in(command_name, info_item['executable-path'])
                elif info_key == 'requirements-in-general':
                    for requirement, incidence in info_item.iteritems():
                        frequencies = set(['always', 'sometimes', 'never', "always | sometimes | never"])
                        assert_in(incidence, frequencies)

    if 'can-modify' in command.keys():
        # Make sure these are all booleans.
        for key in command['can-modify']:
            true_false = command['can-modify'][key]
            assert_custom(type(true_false) == bool, "`"+str(true_false)+"` is not a boolean.")

    try:
        check_sha1(command['description']['string'],
                   command['description']['sha1-hex'])
        unique_SHA1s.add(command['description']['sha1-hex'])
    except KeyError:
        supply_sha1(command['description']['string'])

    assert_custom_warn_only(expected_description_SHA1 == hashlib.sha1(command['description']['string']).hexdigest(),
        "Filename does not match SHA1 of description.\n" + \
        "Should be: " + hashlib.sha1(command['description']['string']).hexdigest())

    if 'nilsimsa' in sys.modules:
        try:
            check_nilsimsa( command['description']['string'], command['description']['nilsimsa-hex'])
        except KeyError:
            supply_nilsimsa(command['description']['string'])

    def validate_invocation(invocation):
        try:
            check_sha1(invocation['string'], invocation['sha1-hex'])
            unique_SHA1s.add(invocation['sha1-hex'])
        except KeyError:
            supply_sha1(invocation['string'])

        if 'nilsimsa' in sys.modules:
            try:
                check_nilsimsa( invocation['string'], invocation['nilsimsa-hex'])
            except KeyError:
                supply_nilsimsa(invocation['string'])

        if 'changeable-arguments' in invocation_dict.keys():
            arg_dict = invocation_dict['changeable-arguments']
            if arg_dict:
                for arg, arginfo in arg_dict.iteritems():
                    # Check that the argument actually matches the sliced command.
                    arg_slice = get_slice(invocation_dict['string'], arginfo['invocation-slice'])
                    try:
                        assert_custom(arg == arg_slice, "arg is:\n'"+arg+"'\nbut slice is:\n'"+arg_slice+"'")
                    except AssertionError:
                        pretty_print_slice(invocation_dict['string'], arginfo['invocation-slice'])
                        slice_candidate = find_slice(invocation_dict['string'], arg)
                        if slice_candidate:
                            print "Suggested slice:", str(slice_candidate)
                            pretty_print_slice(invocation_dict['string'], slice_candidate)
                        raise
                    if 'component-command' in arginfo.keys():
                        assert_in(arginfo['component-command'], command['component-commands'])

        for component_command in command['component-commands']:
            assert_in(component_command, invocation_dict['string'])

    for invocation_name, invocation_dict in command['invocations'].iteritems():

        validate_invocation(invocation_dict)


def match_pseudoschema(json_value, directory, json_trace="", debug=False):
    print "jsontrace: pseudo-schema/"+json_trace
    print "directory: "+directory

    def is_wildcard_field(child_name):
        # If the child starts with '$',
        # e.g. "$COMMAND",
        # it is a wildcard.
        if child_name[0] == '$':
            return True
        else:
            return False

    def check_pair(key, value):
        directory_contents = os.listdir(directory)
        if debug:
            print directory_contents
        if key not in directory_contents and debug:
            print "Error! key="+repr(key)+" not in",directory_contents
            print "value=",value
        if len(directory_contents) == 1 and is_wildcard_field(directory_contents[0]):
            # This is a wildcard directory, so just continue recursing.
            next_path = os.path.join(directory, directory_contents[0])
            match_pseudoschema(value, next_path, json_trace+str(key)+'/', debug)
        else:
            # We're only checking that the JSON child objects are in the pseudoschema;
            # if the JSON doesn't have all of the pseudoschema, that's ok.
            if key in directory_contents:
                next_path = os.path.join(directory, key)
                match_pseudoschema(value, next_path, json_trace+str(key)+'/', debug)
            else:
                raise ValueError, "Not in pseudoschema: "+repr(key)+" not one of "+repr(directory_contents)+"\n"+\
                    "pseudoschema directory: "+directory+"\n"+\
                    "JSON trace: "+json_trace+"\n"+\
                    "Error in file: "+ json_filepath
                # TODO: Figure out a way to trace back to the line of the original JSON file.
                # This will be hard, since we've already parsed the JSON.

    def check_JSONObject(json_object):
        for key, value in json_object.iteritems():
            check_pair(key, value)

    def check_JSONList(json_list):
        for item in json_list:
            directory_contents = os.listdir(directory)
            next_path = os.path.join(directory, directory_contents[0])
            match_pseudoschema(item, next_path, json_trace, debug)

    if isinstance(json_value, dict):
        check_JSONObject(json_value)
    elif isinstance(json_value, list):
        check_JSONList(json_value)
    else:
        # Stop recursing, since the JSON object doesn't have children.
        if debug:
            print "in file: "+ json_filepath
            print "Terminating recursion on",json_trace,"in",directory
            print json_value
        return

if len(sys.argv) == 1:
    print "Usage: python "+sys.argv[0]+" path-to-json-files/"
    sys.exit(1)

unique_SHA1s = NoDuplicates()
num_invocations = 0
root_directory = sys.argv[1]
json_filepaths = glob.glob(root_directory + "/*.json")
for i, json_filepath in enumerate(json_filepaths):
    with open(json_filepath) as json_file:
        try:
            json_data = json.load(json_file)
        except:
            print "Invalid JSON in file: `"+json_file.name+"'"
            raise
        basename_no_extension = os.path.splitext(os.path.basename(json_file.name))[0]
        validate_command(json_data, basename_no_extension)
        match_pseudoschema(json_data, "pseudo-schema/")
        num_invocations += count_invocations(json_data)

num_commands = i + 1 # enumerate starts from 0.
print "Validated", num_commands ,"files(s) and", num_invocations, "invocation(s)."
