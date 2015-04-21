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

def validate_command(command, filepath):

    def assert_custom(assertion, error_string):
        try:
            assert assertion, error_string
        except AssertionError:
            print "In file:", filepath
            traceback.print_exc()
            raise

    # Required fields.
    def required_field(field, field_list):
        assert_custom(field in field_list, "Error: required field `"+field+"` not in "+repr(field_list))

    required_field('description', command.keys())
    required_field('string', command['description'].keys())

    def check_sha1(string, nominal_sha1):
        calculated_sha1 = hashlib.sha1(string).hexdigest()
        assert_custom(nominal_sha1 == calculated_sha1, "SHA1s do not match:\n%s (in database)\n%s (calculated)\n%r (command representation)"  % (nominal_sha1, calculated_sha1, string))

    # TODO: rename this so it doesn't sound like the user must enter the SHA1.
    def prompt_sha1(string):
        sys.stderr.write("Warning: No SHA1 for `" + string + "'")
        sys.stderr.write("Should be: "+hashlib.sha1(string).hexdigest())

    if 'nilsimsa' in sys.modules:
        def check_nilsimsa(string, nominal_nilsimsa):
            calculated_nilsimsa = nilsimsa.Nilsimsa(string).hexdigest()
            assert_custom(nominal_nilsimsa == calculated_nilsimsa, \
                "in file '%s'\n nilsimsas do not match:\n%s (in database)\n%s (calculated)\n%r (command representation)" \
                % (filepath, nominal_nilsimsa, calculated_nilsimsa, string))

        def prompt_nilsimsa(string):
            sys.stderr.write("Warning: in file '" + filepath + "'\n")
            sys.stderr.write("No nilsimsa for `" + string + "'\n")
            sys.stderr.write("Should be: "+nilsimsa.Nilsimsa(string).hexdigest()+"\n")


    if 'component-command-info' in command.keys():
        #TODO: make this less of a horrific mess.
        assert set(command['component-command-info'].keys()).issubset(set(command['component-commands'])), \
            "In file "+filepath+"\n"+ \
            repr(command['component-command-info'].keys())+ "is not a subset of "+repr(command['component-commands'])
        for command_name, info in command['component-command-info'].iteritems():
            for info_key, info_item in info.iteritems():
                if info_key == 'bash-type':
                    bash_types = set(['alias', 'builtin', 'file', 'function', 'keyword'])
                    assert info_item in bash_types or info_item == "builtin | keyword | file", \
                        "In file "+filepath+"\n"+"`"+info_item+"' not in "+repr(bash_types)

                elif info_key == 'debian':
                    if 'executable-path' in info_item.keys() and info_item['executable-path']:
                        # e.g. `ls` is in `/bin/ls`
                        assert command_name in info_item['executable-path']
                elif info_key == 'requirements-in-general':
                    for requirement, incidence in info_item.iteritems():
                        frequencies = set(['always', 'sometimes' , 'never'])
                        assert incidence in frequencies or incidence == "always | sometimes | never", \
                            "`"+incidence+"' not in "+repr(frequencies)

    try:
        check_sha1(command['description']['string'],
                   command['description']['sha1hex'])
        unique_SHA1s.add(command['description']['sha1hex'])
    except KeyError:
        prompt_sha1(command['description']['string'])

    if 'nilsimsa' in sys.modules:
        try:
            check_nilsimsa( command['description']['string'], command['description']['nilsimsa-hex'])
        except KeyError:
            prompt_nilsimsa(command['description']['string'])

    def validate_invocation(invocation):
        try:
            check_sha1(invocation['string'], invocation['sha1hex'])
            unique_SHA1s.add(invocation['sha1hex'])
        except KeyError:
            prompt_sha1(invocation['string'])

        if 'nilsimsa' in sys.modules:
            try:
                check_nilsimsa( invocation['string'], invocation['nilsimsa-hex'])
            except KeyError:
                prompt_nilsimsa(invocation['string'])

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
                        slice_candidate = find_slice(invocation_dict['string'], arg)
                        if slice_candidate:
                            print "Suggested slice:", str(slice_candidate)
                            pretty_print_slice(invocation_dict['string'], slice_candidate)
                        raise
                    if 'component-command' in arginfo.keys():
                        assert arginfo['component-command'] in command['component-commands'], arginfo['component-command']+" is not one of "+repr(command['component-commands'])

        if 'can-modify' in invocation_dict.keys():
            for key in invocation_dict['can-modify']:
                true_false = invocation_dict['can-modify'][key]
                assert type(true_false) == bool, true_false+" is not a boolean."

        for component_command in command['component-commands']:
            assert component_command in invocation_dict['string'], "component_command:\n"+component_command+"\nis not in invocation:\n"+invocation_dict['string']

    for invocation_name, invocation_dict in command['invocations'].iteritems():

        validate_invocation(invocation_dict)

        invocation_dict = command['invocations'][invocation_name]


def is_wildcard_field(child_name):
    # If the child starts with '$',
    # e.g. "$COMMAND",
    # it is a wildcard.
    if child_name[0] == '$':
        return True
    else:
        return False

def check_pseudoschema(parent_json, parent_pseudoschema, trace_path=""):
    try:
        children_json = parent_json.keys()
    except AttributeError:
        # Stop recursing, since the JSON object doesn't have child objects.
        return

    children_pseudoschema = os.listdir(parent_pseudoschema)
    if len(children_pseudoschema) == 1 and is_wildcard_field(children_pseudoschema[0]):
        # This is a wildcard in the schema, so just continue recursing.
        for child_json in children_json:
            next_path = os.path.join(parent_pseudoschema, children_pseudoschema[0])
            check_pseudoschema(parent_json[child_json], next_path, trace_path+":"+child_json)
    else:
        for child_json in children_json:
            # We're only checking that the JSON child objects are in the pseudoschema;
            # if the JSON doesn't have all of the pseudoschema, that's ok.
            if child_json in children_pseudoschema:
                next_path = os.path.join(parent_pseudoschema, child_json)
                check_pseudoschema(parent_json[child_json], next_path, trace_path+":"+child_json)
            else:
                raise ValueError, "Input does not match pseudoschema: `"+trace_path+":"+child_json+"' not one of "+str(children_pseudoschema)+" in "+parent_pseudoschema
                # TODO: Figure out a way to trace back to the line of the original JSON file. Will be hard, since we've already parsed the JSON.

if len(sys.argv) == 1:
    print "Usage: python "+sys.argv[0]+" path-to-json-files/"
    sys.exit(1)

unique_SHA1s = NoDuplicates()
num_invocations = 0
root_directory = sys.argv[1]
json_filepaths = glob.glob(root_directory + "/*.json")
for i, path in enumerate(json_filepaths):
    with open(path) as json_file:
        try:
            json_data = json.load(json_file)
        except:
            print "Invalid JSON in file: `"+json_file.name+"'"
            raise
        validate_command(json_data, path)
        check_pseudoschema(json_file.name, "pseudo-schema/")
        num_invocations += count_invocations(json_data)

num_commands = i + 1 # enumerate starts from 0.
print "Validated", num_commands ,"files(s) and", num_invocations, "invocation(s)."
