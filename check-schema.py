#! /usr/bin/env python
import json
import jsonschema
data = json.load(open("templates/simple-template.json"))
schema = json.load(open("schemas/simple-schema.json"))

jsonschema.validate(data, schema)
