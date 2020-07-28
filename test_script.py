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


    def test_invalid_oyster_no_invocation_string(self):
        query = cmdoysters.QueryInfo()
        query.commands = ['ls']
        query.substring = None
        query.tokens = None
        query.description = None
        query.description_tokens = None

        filepath = "dummy_filepath"

        oyster = {
            "component-commands": [
                "ls"
            ],
            "description": {
                "verbose-description": "List contents of a directory."
            },
            "invocations": [
                {
                    "comment": "example comment"
                }
            ],
            "uuid": "27885a94-c25f-4fb6-b6ac-c381869c87ce"
        }

        logging.disable(logging.ERROR)
        with self.assertRaises(KeyError) as e:
            cmdoysters.get_matching_invocations(oyster, query, filepath)
        logging.disable(logging.NOTSET)

    def test_oyster_match_component_command(self):
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
