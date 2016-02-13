#! /usr/bin/env python

import sys
import json

for filepath in sys.argv[1:]:
    with open(filepath) as f:
        try:
            oyster = json.load(f)
        except ValueError:
            sys.stderr.write("In file: {}\n".format(filepath))
            raise
    with open(filepath, 'w') as f:
        json.dump(oyster, f, indent=4, separators=(',', ': '), sort_keys=True)
        f.write('\n') # add a trailing newline.
