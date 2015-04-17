.. -*- coding: utf-8 -*-

=================================================
CmdOyster: a command repository and metadatabase.
=================================================

----------
Quickstart
----------

#. ``git clone https://github.com/nbeaver/cmd-oyster``

#. ``cd cmd-oyster/``

#. ``python2 ./find-command.py --substring ping``

----------
Motivation
----------

Ever filed away a useful shell command and been unable to find it later?

Ever been stymied by a `man page without examples <https://wiki.freebsd.org/ManPagesWithoutExamples>`_?

This is intended to provide a repository of shell commands that:

- Explicitly state which shells they work with, and `which ones they don't <http://tldp.org/LDP/abs/html/portabilityissues.html>`_.

- Explicitly state which packages they require for multiple platforms.

- Explicitly state which version the software requires for the command to work properly.

- Explicitly state which arguments can be modified.

- Explicitly state when they require a working internet connection.

- Explicitly state when they require root privileges.

- Are straightforward to query because of robust metadata instead of fragile regular expression searches.

- Link to sources and relevant documentation.

Example scenarios this is intended to be useful for:

- Debugging a wifi card without a working internet connection.

- Building up a complex ``find`` command by combining simpler examples.

- Leveraging well-known commands without copying and pasting them from online forums.

- Quick lookup of commands for doing familiar tasks on an unfamiliar system.

More generally, this is intended to be extendible to interactive textual commands in general,
such as ``gnuplot``, ``ipython``, ``irb``, ``maxima``, and so on.

.. Composite commands versus component commands.

.. Order of arguments.

.. Requirements: if the command fails, why? Is it an installation problem? Is the command not in my $PATH? Is it a permissions problem? Is it a network problem?

------------
Design goals
------------

~~~~~~~~~~~~~~~~~~~~~
Simple textual format
~~~~~~~~~~~~~~~~~~~~~

Well-maintained JSON libraries are readily available for almost all programming languages,
but the same is unfortunately not true for YAML.

The data are not complex enough to require XML.

A directory of JSON files makes code work cross-platform and cross-language easily.

~~~~~~~~~~~~
Mergeability
~~~~~~~~~~~~

The JSON fields should appear in alphanumeric order.
This way, diffing and merging becomes much less problematic.

Also, commands are not assigned arbitrary primary keys,
since two different databases could have keys that clash.

Instead, commands can reference related commands
by the SHA-1 hash of the description text or invocation string
(see `Cross-referencing`_).

This means that two different commands must not have the same description text.

~~~~~~~~~~~~~~~~~~~~~~
Compatibility metadata
~~~~~~~~~~~~~~~~~~~~~~

The metadata about the commands should indicate which shells they are compatible with,
and what their dependencies are (e.g. a list of Debian package names).

Also, if an invocation only works for a particular shell,
an alternative invocation using the same commands can be added
while retaining the context and connection to the other command.

This way, if a command fails or does not behave as expected,
it is easier to debug.

~~~~~~~~~~~~~
Extensibility
~~~~~~~~~~~~~

New fields can be added to the JSON objects without breaking existing code.

Fields can be omitted and added later

~~~~~~~~~~~~~~~~~
Cross-referencing
~~~~~~~~~~~~~~~~~

Commands can "link" to related commands via their SHA-1 hash hex digests.

This also makes finding commands indexed by search engines much easier,
since most search engines do not match special characters,
but a SHA-1 hash is a unique alphanumeric identifier.

~~~~~~~~~~~~~~~~~~~~
Similarity detection
~~~~~~~~~~~~~~~~~~~~

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

#. Metadata and search based on metadata.
#. Cross-referencing.
#. Unique (SHA-1) and string similarity (Nilsimsa) hashes of commands.

In addition, the focus of commandlinefu is in providing a platform for commenting and upvoting,
which is different from the focus of a customized repository of commands,
many of which may only be useful to their creator.

.. _commandlinefu: http://www.commandlinefu.com/

- Why not just make an alias or shell function and add it to your ``bashrc``?

It's not always easy to find a short, memorable name for an alias that doesn't conflict with existing commands,
and a multitude of aliases tend to make autocompletion more unwieldy and less predictable.

Aliases and shell functions are great for commonly used commands with a particular shell,
but not so great for remembering how to use a command from several months ago,
or for keeping track of how to do the same thing with a variety of different shells.

- What does the term ``component command`` refer to?

One of the greatest strength of shell commands is that they can be piped together,
evaluated to supply arguments to other commands,
or even taken directly as arguments to other commands.

These composite commands consist of more than one component command,
which may be executable in the filesystem or shell builtins.

- What's the difference between commands and invocations?

Often times, there are multiple ways to write the same command,
such as long flag/short flag versions,
a different order of arguments,
or just a different method,
e.g. removing a file in the current directory named ``-``
using either ``rm ./-`` or ``rm -- -``.

Since these use the same component commands,
it makes sense to group them together
than list them redundantly as separate commands.
These are said to be equivalent invocations of the same command.

If there is a similar command that uses different component commands,
it must be listed as a different command,
not an equivalent invocation:
e.g. ``unlink -`` will accomplish the same thing as ``rm ./-``,
but it must be listed as a different command.
However, they can be `cross-referenced`_.

.. _cross-referenced: `Cross-referencing`_

- Is it ok for command invocations to span multiple lines?

Yes, but one-liners are the focus for now.

This is meant to aid interactive use of commandline programs,
such as core building blocks of shell scripts,
not a library of robust and well-commented shell scripts.

- Why use ``python2`` as the implementation?

The main focus for this project is the database of commands (expressed as JSON files),
not the search application or validation programs as such.

However, Python is widespread and cross-platform,
and ``python2`` has a ``nilsimsa`` hash library.

-----------------------------------------------
Example of adding a new command to the database
-----------------------------------------------

Install `tree`_, `markdown`_, and `docutils`_ for generating documentation.

On Debian, this is accomplished with::

    apt-get install tree markdown python-docutils

and the optional `nilsimsa library`_ can be installed with:: 

    pip install nilsimsa

which appears to currently be Python 2 only.

.. _tree: http://mama.indstate.edu/users/ice/tree/
.. _markdown: http://daringfireball.net/projects/markdown/
.. _docutils: http://docutils.sourceforge.net/
.. _nilsimsa library: https://pypi.python.org/pypi/nilsimsa/0.3.2

Copy `<command-templates/minimal-template.json>`_ to ``command-templates/temp.json``.

Change the ``description`` and ``invocation`` strings.

Run `<validate-database.py>`_ to supply the SHA-1 and Nilsimsa hashes.

Copy over some of the fields from other entries or from `<command-templates/full-command-template.json>`_.

Run ``make`` to ensure the JSON is valid.

Continue adding metadata and invocations until satisfied.

Rename file to the SHA-1 hash of its description,
appended with ``.json``.

Move the JSON file into `<commands/>`_.

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

Copy over the new field to `<pseudo-schema-notes.markdown>`_
and add a description.

-------------------
Future improvements
-------------------

See `<TODO.rst>`_.

Here are some highlights:

- Incremental search interface.

- Generate list of required packages for a given command, depending on OS.

- Spawn a shell with the command automatically filled in and ready to edit or press enter.
