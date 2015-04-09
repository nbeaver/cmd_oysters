#! /usr/bin/env python
import json
import nilsimsa

commands = json.load(open("command-database.json"))

for command in commands:
    command['description']['nilsimsa-hex'] = nilsimsa.Nilsimsa(command['description']['string']).hexdigest()
    for invocation, invocation_dict in command['invocations'].iteritems():
        invocation_dict['nilsimsa-hex'] = nilsimsa.Nilsimsa(invocation_dict['string']).hexdigest()

json.dump(commands, open("nilsimsa.json", 'w'), indent=4, sort_keys=True)
