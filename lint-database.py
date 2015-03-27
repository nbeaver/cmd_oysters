#! /usr/bin/env python
import json
import hashlib

with open("command-database.json") as db_file:
    commands = json.load(db_file)

for command in commands:

    if 'bytes' in command['invocation'].keys():
        nominal_bytes = int(command['invocation']['bytes'])
        calculated_bytes = len(command['invocation']['string'])
        assert nominal_bytes == calculated_bytes, \
            "String lengths do not match: %d != %d\n%r" \
            % (nominal_bytes, calculated_bytes, command['invocation']['string'])

    if 'sha1hex' in command['invocation'].keys():
        nominal_sha1 = command['invocation']['sha1hex']
        calculated_sha1 = hashlib.sha1(command['invocation']['string']).hexdigest()
        assert nominal_sha1 == calculated_sha1, \
            "SHA1s do not match:\n%r\n\n%r" \
            % (nominal_sha1, calculated_sha1)

    if 'invocation-long-flags' in command.keys():
        if 'bytes' in command['invocation-long-flags'].keys():
            assert int(command['invocation-long-flags']['bytes']) == len(command['invocation-long-flags']['string'])
        if 'sha1hex' in command['invocation-long-flags'].keys():
            assert command['invocation-long-flags']['sha1hex'] == hashlib.sha1(command['invocation-long-flags']['string']).hexdigest()

    if 'changeable-arguments' in command.keys():
        arg_dict = command['changeable-arguments']
        for arg, arginfo in arg_dict.iteritems():
            def get_slice(string_to_slice, slice_index_list):
                # We're slicing a string, so the list should only have the start and stop of the slice.
                assert len(slice_index_list) == 2
                i1 = int(slice_index_list[0])
                i2 = int(slice_index_list[1])
                return str(string_to_slice)[i1:i2]

            # Check that the argument actually matches the sliced command.
            assert arg == get_slice(command['invocation']['string'], arginfo['invocation-slice'])
            if 'invocation-long-flags' in command.keys():
                assert arg == get_slice(command['invocation-long-flags']['string'], arginfo['invocation-long-flags-slice'])
