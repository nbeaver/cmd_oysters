.. -*- coding: utf-8 -*-

==========================================
Shell command repository and metadatabase.
==========================================

----------
Quickstart
----------

.. TODO: Add URL here.

#. ``git clone https://github.com/``

.. TODO: Add directory name here.

#. ``cd name-of-directory/``

#. ``python2 find-command.py --substring 'ping'``

.. Required packages: python
.. Recommended packages: tree (for pseudoschema), yajl (for verification), markdown and rst (for documentation)

----------
Motivation
----------

Ever tried to debug your wifi card without a working internet connection?

Ever tried to run a complex shell command and had a hard time figuring out which part of the command was misbehaving?

Ever been frustrated by a shell command that relied on `unportable shell extensions <http://tldp.org/LDP/abs/html/portabilityissues.html>`_ to work correctly?

Ever tried to use a command and find out that the version you're using is too old?

Ever filed away a useful command snippet and been unable to find it later?

Ever been stymied by a `man page without examples <https://wiki.freebsd.org/ManPagesWithoutExamples>`_?

.. Restarting daemons, changing permissions, shell incompatibility.

.. Security of shell commands, looking online ones.

.. Composite commands versus component commands.

.. Order of arguments.

.. Requirements: if the command fails, why? Is it an installation problem? Is the command not in my $PATH? Is it a permissions problem? Is it a network problem?

------------
Design goals
------------

- Simple textual format (JSON).

Well-maintained JSON libraries are readily available for almost all programming languages,
but the same is unfortunately not true for YAML.

The data are not complex enough to require XML.

A single JSON file makes code work cross-platform and cross-language easily.

- Mergeability.

The JSON fields must appear in alphanumeric order.
This way, diffing and merging becomes much less problematic.

Also, commands are not assigned arbitrary primary keys,
since two different databases could have keys that clash.

Instead, commands can reference related commands by the SHA1 hash of the description text.

This means that two different commands must not have the same description text.

- Explicity requirements and portability metadata.

The metadata about the commands should indicate which shells they are compatible with,
and what their dependencies are.

Also, if an invocation only works for a particular shell,
an alternative invocation using the same commands can be added
while retaining the context and connection to the other command.

This way, if a command fails or does not behave as expected,
it is easier to debug.

- Extensbility.

New fields can be added to the JSON objects without breaking existing code.

- Cross-referencing.

Commands can "link" to related commands via their SHA1 hash hex digests.

- Similarity detection.

Similar commands can be found by comparing their Nilsimsa hash hex digests.

`Nilsimsa`_ is a `locality-sensitive`_ hashing algorithm originally developed for spam detection.

.. _Nilsimsa: http://en.wikipedia.org/wiki/Nilsimsa_Hash
.. _locality-sensitive: http://en.wikipedia.org/wiki/Locality-sensitive_hashing

---------
Questions
---------

- Why not just make an alias or shell function and add it to your ``bashrc``?

It's not always easy to find a short, memorable name for an alias that doesn't conflict with existing commands,
and a multitude of aliases tend to make autocompletion more unwieldy and less predictable.

Aliases and shell functions are great for commonly used commands with a particular shell,
but not so great for remembering how to use a command from several months ago,
or for keeping track of how to do the same thing with a variety of different shells.

- What does the term ``component command`` refer to?

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
but it must be listed as a different command.

- Is it ok for command invocations to span multiple lines?

Yes, but one-liners are the focus for now.

This is mean for helping with interactive uses of a shell,
or core building blocks of shell scripts,
not a collection of well-designed and documented multiline shell scripts.

- Why use ``python2`` as the implementation?

The main focus for this project is the command metadatabase (expressed as a JSON file),
not the search application or validation programs as such.

However, Python is widespread and cross-platform,
and ``python2`` has a ``nilsimsa`` hash library.

---------------------------------------
How to add new commands to the database
---------------------------------------

Copy `<simple-template.json>`_ to ``temp.json``.

Change the description and invocation strings.

Run `<validate-database.py>`_ to supply the SHA1 and Nilsimsa hashes.

Copy over some of the fields from previous entries or from `<full-command-template.json>`_.

Run ``make`` to ensure the JSON is valid.

Continue adding metdata and invocations until satisfied.

Copy into `<command-database.json>`_.

-------------------------------------
How to add new fields to the database
-------------------------------------

Navigate to the relevant directory in `<pseudo-schema/>`_.

If the new field is an object, make a new directory.
Otherwise, make an empty file.

If the field is a wildcard and permits any name,
start it with a ``$`` (dollar sign) and use all caps,
e.g ``$COMMAND`` or ``$ARG``.
(The dollar sign is required, but the caps are optional).

Run ``make`` to update `<pseudo-schema-tree.txt>`_.
Copy over the field to `<pseudo-schema-notes.markdown>`_
and add a description.

-------------------
Future improvements
-------------------

.. Incremental search mode.

.. Make it spit out the required packages for a given command, depending on OS.

.. Semantics of command requirements: is it only as the command is used in the invocation, or anytime the command is used?

.. The "always, sometimes, never" is a useful distinction, but what about "depends on flags" or "dependson on arguments" or "depends on configuration" or "depends on shell"?
