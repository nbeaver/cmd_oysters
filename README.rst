.. -*- coding: utf-8 -*-

=========================================
CmdOysters: shell commands with metadata.
=========================================

:Author: Nathaniel Beaver
:Date: $Date: 2015-04-17 (Friday, 17 April 2015) $
:Copyright: This document is licensed under a Creative Commons Attribution 4.0 International license.

See also `<pseudo-schema-notes.markdown>`_ and `<TODO.rst>`_.

.. contents::

---------------
Minimal example
---------------

This is a an example of a minimal but valid CmdOyster JSON file::

    {
        "component-commands": [
            "ls"
        ],
        "description": {
            "sha1hex": "62f6a0e19cae58eefb0e39bc09aaf7b9469202e5",
            "string": "List contents of a directory."
        },
        "invocations": {
            "POSIX" : {
                "sha1hex": "ebfdec641529d4b59a54e18f8b0e9730f85939fb",
                "string": "ls"
            }
        }
    }

Here are some less trivial examples:

- `Highlight the non-ASCII characters in a text file <CmdOysters/118f2d8f8666f09b5d9c9db536d645be5f923f6c.json>`_.

- `Change the current user's default shell <CmdOysters/f3951f67052d0a0ea66062977ab7074c88bf9708.json>`_.

- `Extract images from multiple PDFs <CmdOysters/040662df76d8e74369a2b56c10764ba16b44d2a7.json>`_.

- `Exhaustive reference template showing every possible field in a CmdOyster <templates/full-command-template.json>`_.

----------
Quickstart
----------

#. ``git clone https://github.com/nbeaver/command-oysters``

#. ``cd command-oysters/``

#. ``python2 find-command.py --substring "ping -i"``

More examples:

#. ``python2 find-command.py --commands awk grep``

#. ``python2 find-command.py --tokens '|' '~'``
   
#. ``python2 find-command.py --description-tokens architecture bit``

----------
Motivation
----------

Ever filed away a useful shell command and been unable to find it later?

Ever been stymied by a `man page without examples <https://wiki.freebsd.org/ManPagesWithoutExamples>`_?

This is intended to provide a repository of shell commands that:

- Have explicit metadata explaining their use, such as:

  - which shells they work with, and `which ones they don't <http://tldp.org/LDP/abs/html/portabilityissues.html>`_;

  - their dependencies and versions;

  - which arguments can be modified;

  - which parts require a working internet connection;

  - and which parts require root privileges.

- Are straightforward to query because of robust metadata instead of more fragile search methods such as regular expressions.

- Link to URIs of sources and relevant documentation.

Example scenarios this is intended to be useful for:

- Debugging a wifi card without a working internet connection.

- Building up a complex ``find`` command by combining simpler examples.

- Leveraging well-known commands without copying and pasting them from online forums.

- Quick lookup of commands for doing familiar tasks on an unfamiliar system.

More generally, this is intended to be make the use of shell commands
less surprising, more portable, and more robust.

It's also intended to make sharing the knowledge
of how to use a shell command for a particular purpose
as simple as sending a text file.

------------
Design goals
------------

~~~~~~~~~~~~~~~~~~~~~
Simple textual format
~~~~~~~~~~~~~~~~~~~~~

CmdOysters are text files in the JSON data serialization format.

Of textual data serialization formats,
JSON and YAML are the simplest and most widespread standardized formats.

Well-maintained JSON libraries are readily available for most programming languages,
but the same is unfortunately not true for YAML.

A directory of JSON files makes code work cross-platform and cross-language easily.

In addition, JSON permits Unicode and only requires escaping double quotes and backslashes,
so most commands do not require many changes to store as JSON.

~~~~~~~~~~~~
Mergeability
~~~~~~~~~~~~

The JSON fields in a CmdOyster should appear in alphanumeric order.
This way, diffing and merging becomes easier.

CmdOysters are not assigned arbitrary primary keys,
since two different databases could have clashing primary keys.

Instead, CmdOysters can reference related commands or invocations
by the SHA-1 hash of the description text or invocation string
(see `Cross-referencing`_).

~~~~~~~~~~~~~~~~~~~~~~
Compatibility metadata
~~~~~~~~~~~~~~~~~~~~~~

The metadata about the commands should indicate which shells they are compatible with,
and what their dependencies are (e.g. a list of Debian package names).

CmdOysters can have multiple invocations,
so if one invocation only works in ``bash``,
an alternative invocation for ``csh`` can be stored in the same CmdOyster,
provided it uses the same component commands.

This encourages non-standard but feature-rich shells
to coexist with portable and standardized commands,
since the CmdOyster can provide either option as necessary.

~~~~~~~~~~~~~
Extensibility
~~~~~~~~~~~~~

Frequently, new fields can be added to JSON documents without breaking existing code.

However, since CmdOysters are still under active development,
there may be breaking changes in future versions.
Once the project has matured, this will not be a problem.

~~~~~~~~~~~~~~~~~
Cross-referencing
~~~~~~~~~~~~~~~~~

CmdOysters can "link" to related descriptions or invocations via their SHA-1 hash hex digests.

This also makes finding CmdOysters indexed by search engines much easier,
since most search engines do not match special characters,
but a SHA-1 hash is a unique alphanumeric identifier.

This has a cost;
it means that two different CmdOysters must not have the same description text,
and that updating one CmdOyster's description requires updating all the CmdOysters that point to it,
but it evades some of the problems that URLs and file paths have,
such as maintaining hierarchies and using arbitrary identifiers.

~~~~~~~~~~~~~~~~~~~~
Similarity detection
~~~~~~~~~~~~~~~~~~~~

Similar invocations or descriptions can be found by comparing their Nilsimsa hash hex digests.

`Nilsimsa`_ is a `locality-sensitive`_ hashing algorithm originally developed for spam detection.

.. _Nilsimsa: http://en.wikipedia.org/wiki/Nilsimsa_Hash
.. _locality-sensitive: http://en.wikipedia.org/wiki/Locality-sensitive_hashing

---------------------
Questions and answers
---------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
How is this different from, say, an offline cache of `commandlinefu`_?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Commandlinefu is a remarkable and dedicated online community,
but there are some things it lacks or was never designed to have, such as:

#. Metadata and search based on metadata.
#. Cross-referencing.
#. Unique (SHA-1) and string similarity (Nilsimsa) hashes of command invocations.

In addition, the focus of commandlinefu is in providing a platform for commenting and upvoting,
which is different from the focus of a customized repository of specialized shell commands,
many of which may only be useful to their creator.

.. _commandlinefu: http://www.commandlinefu.com/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Why not just make an alias or shell function and add it to your ``bashrc``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's not always easy to find a short, memorable name for an alias that doesn't conflict with existing commands,
and a multitude of aliases tend to make autocompletion more unwieldy and less predictable.

Aliases and shell functions are great for commonly used commands with a particular shell,
but not so great for remembering how to use a command from several months ago,
or for keeping track of how to do the same thing with a variety of different shells.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
What does the term "component command" refer to?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the greatest strengths of UNIX shell commands
is that they can be composed in many ways.

They can be
used in sequence (e.g. ``./configure && make``),
piped together (e.g. ``du | sort -nr``),
evaluated to supply arguments to other commands (e.g. ``find | grep bash``),
or even taken directly as arguments to other commands (e.g. ``find . -exec file '{}' +``).

These composite commands consist of more than one component command,
which may be executable in the filesystem or shell builtins.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
What's the difference between commands and invocations?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

However, these command can (and should) be `cross-referenced`_.

.. _cross-referenced: `Cross-referencing`_

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Why aren't there many commands yet?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quality over quantity;
this project is new and under active development,
and it is helpful to start with some good examples.

Furthermore, changes to the JSON schema will be necessary,
and if they are breaking changes
it is usually easier to fix a smaller number of CmdOysters.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Is it ok for command invocations to span multiple lines?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, but one-liners are the focus for now.

This is meant to aid interactive use of commandline programs,
such as core building blocks of shell scripts.

CmdOysters are not intended to be a substitute
for a library of robust and well-commented shell scripts,
as there are already many of these available.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Why use Python 2.7 as the implementation language?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main focus for this project is the database of CmdOysters,
expressed as JSON files,
not the search application or validation programs as such.

However, Python is widespread and cross-platform,
and ``python2`` has a ``nilsimsa`` hash library.

~~~~~~~~~~~~~~~~~~~~~~~~~
Why call them CmdOysters?
~~~~~~~~~~~~~~~~~~~~~~~~~

The oyster is a metaphor for surrounding a compact shell command with contextual metadata;
the shell command is like the small, compact pearl inside,
and the metadata like the protective shell and oyster tissue.

This metaphor is appropriate for shell commands
because JSON's curly bracket pairs are visually similar
to a stylized bivalve mollusk shell: ``{}``

The name is also a nod to the reputation of Perl for cryptic one-liners,
a reputation it shares with the UNIX shells.

~~~~~~~~~~~~~~~~~~~~~
What about licensing?
~~~~~~~~~~~~~~~~~~~~~

CmdOysters have fields for authors and licenses.

This is intended to protect both those who make their own CmdOysters and those who use them.

It may seem strange to have a license for what amounts to one line of code,
but the command invocation is just one part of a JSON document that could be construed as a creative work,
so an explicit grant of copyright is always better than an ambiguous one.


The `extent to which metadata is copyrightable`_ varies by country and is still somewhat controversial,
so while the license field is not strictly required,
it is strongly encouraged to ensure others may use the CmdOyters freely.

.. _extent to which metadata is copyrightable: http://lj.libraryjournal.com/2013/02/opinion/peer-to-peer-review/metadata-and-copyright-peer-to-peer-review/

---------------------------------
Example of making a new CmdOyster
---------------------------------

Python has had a built-in JSON library since version 2.6.
The optional `nilsimsa library`_ can be installed with::

    pip install nilsimsa

which appears to currently be Python 2 only.

.. _nilsimsa library: https://pypi.python.org/pypi/nilsimsa/0.3.2

Copy `<templates/simple-template.json>`_ to ``templates/temp.json``.

Edit ``temp.json``, changing the ``description`` and ``invocation`` strings.

Run `<validate-database.py>`_ to supply the SHA-1 and Nilsimsa hashes.

Copy over some of the fields from other entries
or from `<templates/full-command-template.json>`_
and supply the new values as necessary.

Run ``make`` to ensure the JSON is valid.

Continue adding metadata and invocations until satisfied.

Rename file to the SHA-1 hash of its description,
appended with ``.json``.

Move the JSON file into `<commands/>`_.

------------------------------
How to add new metadata fields
------------------------------

Install `tree`_, `markdown`_, and `docutils`_ for generating documentation.

.. _tree: http://mama.indstate.edu/users/ice/tree/
.. _markdown: http://daringfireball.net/projects/markdown/
.. _docutils: http://docutils.sourceforge.net/

On Debian, this is accomplished with::

    apt-get install tree markdown python-docutils

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

Note that the best metadata to include is information that is:

- not readily available in man pages,

- directly applicable to the specific use of the invocation,

- and easy to verify or falsify.

-------
License
-------

The project is licensed under the MIT (a.k.a Expat) license.

http://opensource.org/licenses/MIT

http://directory.fsf.org/wiki/License:Expat

The CmdOysters are JSON documents containing licenses as part of their metadata.

-------------------
Future improvements
-------------------

See `<TODO.rst>`_.

Here are some highlights:

- More robust validation,
  including a proper JSON schema.

- Incremental search interface.

- Generate list of required packages for a given command, depending on OS.

- Spawn a shell with the command automatically filled in and ready to edit or press enter.

- Extend CmdOysters to interactive textual commands in general,
  such as ``gnuplot``, ``ipython``, ``irb``, ``maxima``, and so on.
