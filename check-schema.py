#! /usr/bin/env python
import json
import jsonschema
import os

def validate_in_directory(directory, schema):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                data = json.load(open(filepath))
                try:
                    jsonschema.validate(data, schema)
                except jsonschema.exceptions.ValidationError:
                    print filepath
                    raise

full_schema = json.load(open("schemas/full-schema.json"))
validate_in_directory("templates", full_schema)
validate_in_directory("CmdOysters", full_schema)
