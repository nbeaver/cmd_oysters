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

#. ``python2 find-command.py --substring ping``

.. Required packages: python
.. Recommended packages: tree (for pseudoschema), yajl (for verification), markdown and rst (for documentation)

----------
Motivation
----------

Ever filed away a useful shell command and been unable to find it later?

Ever been stymied by a `man page without examples <https://wiki.freebsd.org/ManPagesWithoutExamples>`_?

This is intended to provide a repository of shell commands that:

- Explicitly state which shells they work with, and `which ones they don't <http://tldp.org/LDP/abs/html/portabilityissues.html>`_.

- Explicitly state which version the software requires for the command to work properly.

- Explicitly state which arguments can be modified.

- Explicitly state when they require a working internet connection.

- Explicitly state when they require root privileges.

- Are straightforward to query because of robust metadata instead of fragile regular expression searches.

- Link to sources and relevant documentation.

Example scenarios this is intended to be useful for:

- Debugging a wifi card without a working internet connection.

- Building up a complex ``find`` command by combining simpler examples.

- Leveraging existing commands without copying and pasting them from online forums.

- Rapidly finding commands for administering an unfamiliar system.

More generally, this is intended to be extendable to interactive textual commands in general,
such as ``gnuplot``, ``ipython``, ``irb``,

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

Similar commands or command descriptions can be found by comparing their Nilsimsa hash hex digests.

`Nilsimsa`_ is a `locality-sensitive`_ hashing algorithm originally developed for spam detection.

.. _Nilsimsa: http://en.wikipedia.org/wiki/Nilsimsa_Hash
.. _locality-sensitive: http://en.wikipedia.org/wiki/Locality-sensitive_hashing

---------------------
Questions and answers
---------------------

- How is this different from, say, an offline cache of `commandlinefu`_?

  Commandlinefu is a remarkable and dedicated online community,
  but there are some things it lacks or was never designed to have, such as:

  #. Thorough metadata.
  #. Mergeable invocations instead of alternatives.
  #. Independent search options.
  #. Cross-referencing.
  #. Unique (SHA-1) and locality-sensitive (Nilsimsa) hashes of commands.
  
  In addition, the focus of commandlinefu is in providing a platform for commenting and upvoting,
  which is not the same as a customized repository of commands which may only be useful to their creator.

.. commandlinefu: http://www.commandlinefu.com/

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
