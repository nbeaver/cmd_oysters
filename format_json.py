#! /usr/bin/env python3

import sys
import json
import argparse

def format_json(fp):
    try:
        data = json.load(fp)
    except ValueError:
        sys.stderr.write("In file: {}\n".format(fp.name))
        raise
    # Jump back to the beginning of the file before overwriting it.
    fp.seek(0)
    json.dump(data, fp, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True)
    fp.write('\n') # add a trailing newline.
    fp.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Format JSON files in place.'
    )
    parser.add_argument(
        'files',
        type=argparse.FileType('r+'),
        help='JSON filepaths',
        nargs='+'
    )
    args = parser.parse_args()
    for json_file in args.files:
        format_json(json_file)
