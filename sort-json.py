#! /usr/bin/env python2
import json

json.dump(json.load(open("command-database.json")), open("sorted.json", 'w'), indent=4, sort_keys=True)
