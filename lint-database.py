#! /usr/bin/env python
import json
import hashlib

with open("command-database.json") as db_file:
    commands = json.load(db_file)

for command in commands:
    invocations = command['invocations'].keys()
    for shell in invocations:

        invocation_dict = command['invocations'][shell]

        if 'bytes' in invocation_dict.keys():
            nominal_bytes = int(invocation_dict['bytes'])
            calculated_bytes = len(invocation_dict['string'])
            assert nominal_bytes == calculated_bytes, \
                "String lengths do not match: %d != %d\n%s" \
                % (nominal_bytes, calculated_bytes, invocation_dict['string'])

        if 'sha1hex' in invocation_dict.keys():
            nominal_sha1 = invocation_dict['sha1hex']
            calculated_sha1 = hashlib.sha1(invocation_dict['string']).hexdigest()
            assert nominal_sha1 == calculated_sha1, \
                "SHA1s do not match:\n%s (in database)\n%s (calculated)\n%r (command representation)" \
                % (nominal_sha1, calculated_sha1, invocation_dict['string'])
        else:
            print "No SHA1 for `" + invocation_dict['string'] + "'"
            print "Should be:", hashlib.sha1(invocation_dict['string']).hexdigest()

        if 'changeable-arguments' in invocation_dict.keys():
            arg_dict = invocation_dict['changeable-arguments']
            if arg_dict:
                for arg, arginfo in arg_dict.iteritems():
                    def get_slice(string_to_slice, slice_index_list):
                        # We're slicing a string, so the list should only have the start and stop of the slice.
                        assert len(slice_index_list) == 2
                        i1 = int(slice_index_list[0])
                        i2 = int(slice_index_list[1])
                        return str(string_to_slice)[i1:i2]

                    # Check that the argument actually matches the sliced command.
                    assert arg == get_slice(invocation_dict['string'], arginfo['invocation-slice'])
                    if 'invocation-long-flags' in command.keys():
                        assert arg == get_slice(command['invocation-long-flags']['string'], arginfo['invocation-long-flags-slice'])

# TODO: check all the commands in component commands are substrings of the main command.
# TODO: check that the commands in component-command-info
