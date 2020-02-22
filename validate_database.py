#! /usr/bin/env python3
import json
import jsonschema
import sys
import os
import glob
import traceback
import argparse

class NoDuplicates:
    """A set that throws an error if a duplicate item is added."""
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

default_schema_path = os.path.join(sys.path[0],"schemas", "full-schema.json") # need to do it this way for symlinks to work.
parser = argparse.ArgumentParser(description='validate CmdOysters')
parser.add_argument('-i', '--input', help='path to root directory of JSON input files', required=True)
parser.add_argument('-s', '--schema', help='path to schema file', required=False, default=default_schema_path)
args = parser.parse_args()
root_directory = args.input

if len(sys.argv) == 1:
    sys.stderr.write("Usage: python "+sys.argv[0]+" path-to-json-files/"+'\n')
    sys.exit(1)

json_filepaths = glob.glob(root_directory + "/*.json")

full_schema = json.load(open(args.schema))

i = -1 # If the given folder is empty, this is what we need to be consistent with starting from 0.
for i, json_filepath in enumerate(json_filepaths):
    with open(json_filepath) as json_file:
        try:
            json_data = json.load(json_file)
        except:
            sys.stderr.write("Invalid JSON in file: `"+json_file.name+"'"+'\n')
            raise
        try:
            jsonschema.validate(json_data, full_schema)
        except jsonschema.exceptions.ValidationError:
            sys.stderr.write(json_file.name+'\n')
            raise

        uuids = NoDuplicates()

        uuids.add(json_data['uuid'])

num_commands = i + 1 # enumerate starts from 0.
sys.stdout.write("Validated {} files(s).\n".format(num_commands))
