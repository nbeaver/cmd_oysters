.. -*- coding: utf-8 -*-

==========================================
Shell command repository and metadatabase.
==========================================

----------
Quickstart
----------

.. Required packages: python
.. Recommended packages: tree (for pseudoschema), yajl (for verification)

----------
Motivation
----------

.. Ever tried to debug your laptop without an internet connection and not had the commands?

.. Ever stored a useful command for later in a text file and been unable to find it later?

.. Restarting daemons, changing permissions, shell incompatibility.

.. Security of shell commands, looking online ones.

.. Composite commands versus component commands.

.. Order of arguments.

--------
Examples
--------

------------
Design goals
------------

- Simple textual format.

Well-maintained JSON libraries are readily available for almost all programming languages,
but the same is unfortunately not true for YAML.

The data are not complex enough to require XML.

A single JSON file makes code work cross-platform easily.

- Mergeability.

The commands do not have arbitarily designated primary keys,
since two different databases could have keys that clash.

Instead, commands can reference related commands by the SHA1 hash of the description text.

This means that two different commands must not have the same description text.

.. Mergeability (use hashes of descriptions and commands, not arbitrary primary keys).

.. One-liners vs longer scripts.

.. Extensibility of JSON fields without breaking.

.. Why different invocations? Same component commands, different forms.

.. Requirements: if the command fails, why? Is it an installation problem? Is the command not in my $PATH? Is it a permissions problem? Is it a network problem?

---------
Questions
---------

- What are component commands?

- What's the difference between commands and invocations?

Often times, there are multiple ways to write the same command,
such as long flag/short flag versions,
or a different order of arguments,
or just a different method,
e.g. removing a file in the current directory named ``-``
using either ``rm ./-`` or ``rm -- -``.

Rather than list these as separate commands,
they are grouped together as equivalent invocations of the same command.

If there is a similar command that uses different component commands,
it must be listed as a different command,
not an equivalent invocation:
e.g. ``unlink -`` will accomplish the same thing,
but is considered a different command.

- Is it ok for command invocations to span multiple lines?

Yes, but one-liners have been the focus for now.

----------------------------------
Process for adding to the database
----------------------------------

-------------------
Future improvements
-------------------

.. Make it spit out the required packages for a given command, depending on OS.

.. Semantics of command requirements: is it only as the command is used in the invocation, or anytime the command is used?

.. The "always, sometimes, never" is a useful distinction, but what about "depends on flags" or "dependson on arguments" or "depends on configuration" or "depends on shell"?
