#! /usr/bin/env python2
import json
import jsonschema
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

def validate_command(command, description_SHA1_from_filename):
    global modify_file

    def assert_custom(assertion, error_string):
        try:
            assert assertion, error_string
        except AssertionError:
            sys.stderr.write("Error in file: "+ json_filepath+'\n')
            traceback.print_exc()
            raise

    def assert_custom_warn_only(assertion, error_string):
        if assertion:
            return
        else:
            sys.stderr.write("Warning in file: "+ json_filepath+'\n')
            sys.stderr.write(error_string+'\n')
            pass

    def assert_subset(subset, superset):
        assert_custom(subset.issubset(superset), repr(subset)+ "is not a subset of " + repr(superset))

    def assert_in(A, B):
        assert_custom(A in B, repr(A)+ "is not in " + repr(B))

    def prompt_yes_no(message):
        print message
        while True:
            reply = raw_input("Enter yes/no: ").lower()
            if reply in ['yes', 'y']:
                return True
            elif reply in ['no', 'n']:
                return False

    def match_sha1(string, nominal_sha1):
        calculated_sha1 = hashlib.sha1(string).hexdigest()
        if nominal_sha1 != calculated_sha1:
            assert_custom_warn_only(False, \
                "SHA1s do not match:\n%s (in file)\n%s (calculated)\n%r (command representation)" \
                % (nominal_sha1, calculated_sha1, string))
            return False
        else:
            return True

    def supply_sha1(string):
        assert_custom_warn_only(False, \
            "Warning: No SHA1 for `" + string + "'\n"+\
            "Should be: "+hashlib.sha1(string).hexdigest()+"\n")

    def check_sha1_dict(dict_to_check):
        global modify_file
        try:
            if match_sha1(dict_to_check['string'], dict_to_check['sha1-hex']):
                unique_SHA1s.add(dict_to_check['sha1-hex'])
            else:
                if not modify_file:
                    modify_file = prompt_yes_no("SHA1 hashes do not match. Allow modification of "+json_filepath+"?")
                if modify_file:
                    dict_to_check['sha1-hex'] = hashlib.sha1(dict_to_check['string']).hexdigest()
        except KeyError:
            supply_sha1(dict_to_check['string'])
            if not modify_file:
                modify_file = prompt_yes_no("SHA1 hash not present. Allow modification of "+json_filepath+"?")
            if modify_file:
                dict_to_check['sha1-hex'] = hashlib.sha1(dict_to_check['string']).hexdigest()

    if 'nilsimsa' in sys.modules:
        def match_nilsimsa(string, nominal_nilsimsa):
            calculated_nilsimsa = nilsimsa.Nilsimsa(string).hexdigest()
            if nominal_nilsimsa != calculated_nilsimsa:
                assert_custom_warn_only(False, \
                    "nilsimsas do not match:\n%s (in file)\n%s (calculated)\n%r (command representation)" \
                    % (nominal_nilsimsa, calculated_nilsimsa, string))
                return False
            else:
                return True

        def supply_nilsimsa(string):
            assert_custom_warn_only(False, \
                "No nilsimsa for `" + string + "'\n"+\
                "Should be: "+nilsimsa.Nilsimsa(string).hexdigest()+"\n")

        def check_nilsimsa_dict(dict_to_check):
            # TODO: combine with check_sha1_dict().
            # This will require passing the hash function,
            # the name of the hash,
            # and possibly the keys as well.
            global modify_file
            try:
                if match_nilsimsa(dict_to_check['string'], dict_to_check['nilsimsa-hex']):
                    pass
                else:
                    if not modify_file:
                        modify_file = prompt_yes_no("Nilsimsa hashes do not match. Allow modification of "+json_filepath+"?")
                    if modify_file:
                        dict_to_check['nilsimsa-hex'] = nilsimsa.Nilsimsa(dict_to_check['string']).hexdigest()
            except KeyError:
                supply_sha1(dict_to_check['string'])
                if not modify_file:
                    modify_file = prompt_yes_no("Nilsimsa hash not present. Allow modification of "+json_filepath+"?")
                if modify_file:
                    dict_to_check['nilsimsa-hex'] = nilsimsa.Nilsimsa(dict_to_check['string']).hexdigest()

    if 'component-command-info' in command.keys():

        assert_subset(set(command['component-command-info'].keys()), set(command['component-commands']))

        for command_name, info in command['component-command-info'].iteritems():
            for info_key, info_item in info.iteritems():

                if info_key == 'debian':
                    if 'executable-path' in info_item.keys() and info_item['executable-path']:
                        # e.g. `ls` is in `/bin/ls`
                        assert_in(command_name, info_item['executable-path'])

    if 'relevant-urls' in command.keys():
        for url in command['relevant-urls']:
            if 'url-sha1-hex' in url.keys():
                if match_sha1(url['url-string'], url['url-sha1-hex']):
                    # We don't add check these SHA-1 hashe for uniqueness
                    # because two different commands might link to the same URI,
                    # and that's ok.
                    pass
                else:
                    if not modify_file:
                        modify_file = prompt_yes_no("SHA1 hashes do not match. Allow modification of "+json_filepath+"?")
                    if modify_file:
                        url['url-sha1-hex'] = hashlib.sha1(url['url-string']).hexdigest()

            else:
                supply_sha1(url['url-string'])

            if 'nilsimsa' in sys.modules:
                if 'url-nilsimsa-hex' in url.keys():
                    if match_nilsimsa(url['url-string'], url['url-nilsimsa-hex']):
                        pass
                    else:
                        if not modify_file:
                            modify_file = prompt_yes_no("Nilsimsa hashes do not match. Allow modification of "+json_filepath+"?")
                        if modify_file:
                            url['url-nilsimsa-hex'] = nilsimsa.Nilsimsa(url['url-string']).hexdigest()
                else:
                    supply_nilsimsa(url['url-string'])

    check_sha1_dict(command['description'])

    assert_custom_warn_only(description_SHA1_from_filename == hashlib.sha1(command['description']['string']).hexdigest(),
        "Filename does not match SHA1 of description.\n" + \
        "Should be: " + str(hashlib.sha1(command['description']['string']).hexdigest()) + ".json")

    if 'nilsimsa' in sys.modules:
        check_nilsimsa_dict(command['description'])

    def validate_invocation(invocation):
        check_sha1_dict(invocation)

        if 'nilsimsa' in sys.modules:
            check_nilsimsa_dict(invocation)

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
                            print "Slice in file:", str(arginfo['invocation-slice'])
                            print "Suggested slice:", str(slice_candidate)
                            pretty_print_slice(invocation_dict['string'], slice_candidate)
                        raise
                    if 'component-command' in arginfo.keys():
                        assert_in(arginfo['component-command'], command['component-commands'])

        for component_command in command['component-commands']:
            assert_in(component_command, invocation_dict['string'])

    for invocation_name, invocation_dict in command['invocations'].iteritems():
        validate_invocation(invocation_dict)

if len(sys.argv) == 1:
    sys.stderr.write("Usage: python "+sys.argv[0]+" path-to-json-files/"+'\n')
    sys.exit(1)

unique_SHA1s = NoDuplicates()
num_invocations = 0
modify_file = False
root_directory = sys.argv[1]
json_filepaths = glob.glob(root_directory + "/*.json")

#TODO: pass this as a parameter with `--schema` instead of hard-coding it.
full_schema = json.load(open("schemas/full-schema.json"))

for i, json_filepath in enumerate(json_filepaths):
    with open(json_filepath) as json_file:
        try:
            json_data = json.load(json_file)
        except:
            sys.stderr.write("Invalid JSON in file: `"+json_file.name+"'"+'\n')
            raise
        basename_no_extension = os.path.splitext(os.path.basename(json_file.name))[0]
        try:
            jsonschema.validate(json_data, full_schema)
        except jsonschema.exceptions.ValidationError:
            sys.stderr.write(json_file.name+'\n')
            raise
        validate_command(json_data, basename_no_extension)
        num_invocations += count_invocations(json_data)
    if modify_file:
        sys.stderr.write("Warning: overwriting "+json_filepath+"\n")
        new_file = open(json_filepath, 'w')
        json.dump(json_data, new_file, indent=4, separators=(',', ': '), sort_keys=True)
        modify_file = False # very important!

num_commands = i + 1 # enumerate starts from 0.
print "Validated", num_commands ,"files(s) and", num_invocations, "invocation(s)."
