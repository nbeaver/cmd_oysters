#! /usr/bin/env python3

import unittest
import cmdoysters
import logging

class CmdOysterTest(unittest.TestCase):

    def test_tokenize_1(self):
        example_sentence = "This is an example sentence; it has punctuation."
        tokens = cmdoysters.tokenize(example_sentence)
        assert tokens == ["This", "is", "an", "example", "sentence", "it", "has", "punctuation"]

    def test_lowercase_subset(self):
        l1 = ["a"]
        l2 = ["a", "b"]
        l3 = ["a", "b", "c"]
        x = ["x"]
        L1 = ["a"]
        L2 = ["a", "b"]
        L3 = ["a", "b", "c"]
        X = ["x"]
        assert cmdoysters.lowercase_subset(l1, l1) == True
        assert cmdoysters.lowercase_subset(l1, l2) == True
        assert cmdoysters.lowercase_subset(l2, l3) == True
        assert cmdoysters.lowercase_subset(l1, l3) == True
        assert cmdoysters.lowercase_subset(L1, l1) == True
        assert cmdoysters.lowercase_subset(l1, l1) == True
        assert cmdoysters.lowercase_subset(L1, l2) == True
        assert cmdoysters.lowercase_subset(L2, l3) == True
        assert cmdoysters.lowercase_subset(L1, l3) == True
        assert cmdoysters.lowercase_subset(x, l1) == False
        assert cmdoysters.lowercase_subset(l3, l2) == False
        assert cmdoysters.lowercase_subset(l3, l1) == False

    def test_no_invocation_string(self):
        query = cmdoysters.QueryInfo()
        query.commands = ['ls']
        query.substring = None
        query.tokens = None
        query.description = None
        query.description_tokens = None

        invocation = {
            "comment": "example comment"
        }

        logging.disable(logging.ERROR)
        with self.assertRaises(KeyError) as e:
            cmdoysters.invocation_matches(invocation, query)
        logging.disable(logging.NOTSET)

    def test_invocation_substring(self):
        query = cmdoysters.QueryInfo()
        query.commands = None
        query.substring = "ls"
        query.tokens = None
        query.description = None
        query.description_tokens = None

        invocation_1 = {
            "invocation-string": "ls"
        }
        assert cmdoysters.invocation_matches(invocation_1, query) == True
        invocation_2 = {
            "invocation-string": "lsmod"
        }
        assert cmdoysters.invocation_matches(invocation_2, query) == True
        invocation_3 = {
            "invocation-string": "ld"
        }
        assert cmdoysters.invocation_matches(invocation_3, query) == False
        invocation_4 = {
            "invocation-string": "l s"
        }
        assert cmdoysters.invocation_matches(invocation_4, query) == False


    def test_oyster_match_component_command_single(self):
        query = cmdoysters.QueryInfo()
        query.commands = ['ls']
        query.substring = None
        query.tokens = None
        query.description = None
        query.description_tokens = None

        oyster_1 = {
            "component-commands": [
                "ls"
            ],
            "description": {
                "verbose-description": "List contents of a directory."
            },
        }
        assert cmdoysters.oyster_matches(oyster_1, query) == True

        oyster_2 = {
            "component-commands": [
                "date"
            ],
            "description": {
                "verbose-description": "Show the current date and time."
            },
        }
        assert cmdoysters.oyster_matches(oyster_2, query) == False

        oyster_3 = {
            "component-commands": [
                "ls",
                "grep"
            ],
            "description": {
                "verbose-description": "Filter the output of ls."
            },
        }
        assert cmdoysters.oyster_matches(oyster_3, query) == True

        oyster_4 = {
            "component-commands": [
                "lsmod"
            ],
            "description": {
                "verbose-description": "List kernel modules."
            },
        }
        assert cmdoysters.oyster_matches(oyster_4, query) == False


    def test_oyster_match_component_commands_double(self):
        query = cmdoysters.QueryInfo()
        query.commands = ['awk', 'grep']
        query.substring = None
        query.tokens = None
        query.description = None
        query.description_tokens = None

        oyster_1 = {
            "component-commands": [
                "awk"
            ],
            "description": {
                "verbose-description": "Example"
            },
        }
        assert cmdoysters.oyster_matches(oyster_1, query) == False

        oyster_2 = {
            "component-commands": [
                "grep"
            ],
            "description": {
                "verbose-description": "Example"
            },
        }
        assert cmdoysters.oyster_matches(oyster_2, query) == False

        oyster_3 = {
            "component-commands": [
                "awk",
                "grep"
            ],
            "description": {
                "verbose-description": "Example"
            },
        }
        assert cmdoysters.oyster_matches(oyster_3, query) == True

        oyster_4 = {
            "component-commands": [
                "lscpu",
                "awk",
                "grep"
            ],
            "description": {
                "verbose-description": "Example"
            },
        }
        assert cmdoysters.oyster_matches(oyster_4, query) == True

        oyster_5 = {
            "component-commands": [
                "awk",
                "example",
                "grep"
            ],
            "description": {
                "verbose-description": "Example"
            },
        }
        assert cmdoysters.oyster_matches(oyster_5, query) == True

        oyster_6 = {
            "component-commands": [
                "grep",
                "example",
                "awk"
            ],
            "description": {
                "verbose-description": "Example"
            },
        }
        assert cmdoysters.oyster_matches(oyster_6, query) == True

        oyster_7 = {
            "component-commands": [
                "awk"
                "ugrep",
            ],
            "description": {
                "verbose-description": "Example"
            },
        }
        assert cmdoysters.oyster_matches(oyster_7, query) == False

        oyster_8 = {
            "component-commands": [
                "gawk"
                "grep",
            ],
            "description": {
                "verbose-description": "Example"
            },
        }
        assert cmdoysters.oyster_matches(oyster_8, query) == False

        oyster_9 = {
            "component-commands": [
                "gawk"
                "ugrep",
            ],
            "description": {
                "verbose-description": "Example"
            },
        }
        assert cmdoysters.oyster_matches(oyster_9, query) == False

    def test_oyster_match_description(self):
        query = cmdoysters.QueryInfo()
        query.commands = None
        query.substring = None
        query.tokens = None
        query.description = "list"
        query.description_tokens = None

        oyster_1 = {
            "component-commands": [
                "ls"
            ],
            "description": {
                "verbose-description": "List directory contents."
            },
        }
        assert cmdoysters.oyster_matches(oyster_1, query) == True

        oyster_2 = {
            "component-commands": [
                "date"
            ],
            "description": {
                "verbose-description": "Show the current date and time."
            },
        }
        assert cmdoysters.oyster_matches(oyster_2, query) == False

        oyster_3 = {
            "component-commands": [
                "lsof"
            ],
            "description": {
                "verbose-description": "Show a list of open files."
            },
        }
        assert cmdoysters.oyster_matches(oyster_3, query) == True

    def test_oyster_match_description_tokens(self):
        query = cmdoysters.QueryInfo()
        query.commands = None
        query.substring = None
        query.tokens = None
        query.description = None
        query.description_tokens = ["contents", "directory"]

        oyster_1 = {
            "component-commands": [
                "ls"
            ],
            "description": {
                "verbose-description": "List directory contents."
            },
        }
        assert cmdoysters.oyster_matches(oyster_1, query) == True

    def test_display_invocation_minimal(self):
        invocation = {"invocation-string": "ls"}
        lines = []
        for line in cmdoysters.display_invocation(invocation):
            lines.append(line)
        assert lines == ["ls"]

    def test_display_invocation_with_comment(self):
        invocation = {
            "invocation-string": "ls",
            "comment": "List files"
        }
        lines = []
        for line in cmdoysters.display_invocation(invocation):
            lines.append(line)
        assert lines == ["# List files", "ls"]

    def test_display_invocation_with_example_output(self):
        invocation = {
            "invocation-string": "ls",
            "example-outputs": [
                "file1.txt file2.txt"
            ]
        }
        lines = []
        for line in cmdoysters.display_invocation(invocation):
            lines.append(line)
        assert lines == ["ls", "# Example output:", invocation["example-outputs"][0]]


if __name__ == '__main__':
    unittest.main()
