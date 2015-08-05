.. -*- coding: utf-8 -*-

=========================================
CmdOysters: shell commands with metadata.
=========================================

:Author: Nathaniel Beaver
:Date: $Date: 2015-05-12 (Tuesday, 12 May 2015) $
:Copyright: This document is licensed under a Creative Commons Attribution 4.0 International license.

See also `<TODO.rst>`_.

.. contents::

---------------
Minimal example
---------------

This is an example of the contents of a minimal but valid CmdOyster JSON file::

    {
        "component-commands": [
            "ls"
        ],
        "description": {
            "sha1-hex": "62f6a0e19cae58eefb0e39bc09aaf7b9469202e5",
            "string": "List contents of a directory."
        },
        "invocations": {
            {
                "sha1-hex": "ebfdec641529d4b59a54e18f8b0e9730f85939fb",
                "string": "ls"
            }
        }
    }

Here are some less trivial examples:

- `Highlight the non-ASCII characters in a text file <cmdoysters/118f2d8f8666f09b5d9c9db536d645be5f923f6c.json>`_.

- `Safely list hidden files <cmdoysters/2d0b6b2b90eeb1efbd9591dbfa593766f6cf540a.json>`_.

- `Change the current user's default shell <cmdoysters/f3951f67052d0a0ea66062977ab7074c88bf9708.json>`_.

- `Extract images from multiple PDFs <cmdoysters/040662df76d8e74369a2b56c10764ba16b44d2a7.json>`_.

- `Display the machine's CPU architecture <cmdoysters/9f2fdee93e84817e73dcbe46d01e28af001fbe1e.json>`_.

----------
Quickstart
----------

#. ``git clone https://github.com/nbeaver/cmd-oysters``

#. ``cd cmd-oysters/``

#. ``python2 find-command.py --substring "ping -i"``

More examples:

#. ``python2 find-command.py --commands awk grep``

#. ``python2 find-command.py --tokens '|' '~'``
   
#. ``python2 find-command.py --description-tokens architecture CPU``

----------
Motivation
----------

Ever bookmarked a useful shell one-liner and had trouble finding it later?

Ever been stymied by a `man page without examples`_?

This is intended to provide a repository of shell commands that:

- Have explicit metadata explaining their use, such as:

  - which shells they work with, and `which ones they don't`_;

  - dependencies for running the necessary commands on multiple platforms;

  - required version numbers for the command to function as expected;

  - which arguments can be modified;

  - which commands require a working internet connection;

  - and which parts of the command require root privileges.

- Are straightforward to query because of robust metadata instead of more fragile search methods such as regular expressions.

- Link to URIs of sources and relevant documentation.

Example scenarios this is intended to be useful for:

- Restarting a WiFi card without a working internet connection to look up the required commands.

- Building up a complex ``find`` command by combining simpler examples.

- Leveraging well-known commands without the hazards of `copying and pasting them from online forums into a terminal`_.

- Quick lookup of commands for doing familiar tasks on an unfamiliar system.

More generally, this is intended to be make the use of shell commands
less surprising, more portable, and more robust.

It's also intended to make sharing the knowledge
of how to use a shell command for a particular purpose
as simple as sending a text file.

.. _man page without examples: https://wiki.freebsd.org/ManPagesWithoutExamples
.. _which ones they don't: http://tldp.org/LDP/abs/html/portabilityissues.html
.. _copying and pasting them from online forums into a terminal: http://thejh.net/misc/website-terminal-copy-paste

------------
Design goals
------------

~~~~~~~~~~~~~~~~~~~~~
Simple textual format
~~~~~~~~~~~~~~~~~~~~~

CmdOysters are text files in the JSON data serialization format.

Of textual data serialization formats,
JSON and YAML are the simplest and most widespread standardized formats.

Well-maintained JSON parsing and schema libraries are readily available for most programming languages,
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

CmdOysters permit multiple invocations.

If one version of a command uses ``bash``-only extensions,
another version only works with ``zsh``,
and another works with any POSIX-conformant shell,
all three versions can still be stored in the same CmdOyster,
provided each invocation uses the same `component commands`_.

.. _component commands: `What does the term "component command" refer to?`_

The metadata about the commands indicate which shells they are compatible with,
and what their dependencies are (i.e. a list of component commands).

Currently there is also an optional field for a list of required Debian packages.
In the future, this should be expanded to other package managers.

Per-shell and per-invocation compatibility metadata is provided in several ways:

- A human-readable version specifier string, e.g. ``version 1.3 or higher``
- A list of versions known to be compatible.
- A list of versions known to be incompatible.
- A list of SHA1s known to be compatible.
- A list of SHA1s known to be incompatible.

This may seem excessive,
but version number is not always a reliable indication of command compatibility.

For example, the maximum integer that the ``factor`` command will accept
depends on whether it was compiled with ``bignum`` support.
This does not change the version information,
but it does change the SHA-1 checksum of the binary.

While having the same SHA-1 checksum for the binary does not guarantee the same result,
because of e.g. differing config files,
it still aids in reproducing the expected result,
and is better than relying on version number alone.

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

CmdOysters can "link" to related descriptions or invocations
via their SHA-1 hash hex digests.

This also makes finding CmdOysters indexed by search engines much easier,
since most search engines do not match special characters,
but a SHA-1 hash is a unique alphanumeric identifier.

This has a cost;
it means that two different CmdOysters must not have the same description text,
and that updating one CmdOyster's description requires updating all the CmdOysters that point to it,
but it evades some of the problems that URIs and file paths have,
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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Why not just use the shell history?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shell history searches are useful,
but they behave differently for each shell
and lack metadata and sophisticated search capabilities.

There are tricks to try to get around this deficiency,
such as `using comments as hash tags`_,
but such schemes have `numerous drawbacks`_.

Shells like ``bash`` do not `update the history file`_ until the terminal closes,
so a useful command may `not be available in a new terminal`_.

Most shells limit the `length of the history file`_,
so useful commands may disappear if not used often enough.

Finally, it is inconvenient to synchronize shell histories across multiple machines,
for both technical and security reasons.

(There is a project called `shellsink`_ that `addresses many of these problems`_,
but it is only for ``bash`` and ``zsh`` and its development `appears to be inactive`_ `as of mid 2011`_.)

CmdOysters are individual text files,
so they can be
copied manually,
emailed,
rsynced,
kept in version control,
diffed and merged,
and so on.

.. _using comments as hash tags: http://vignesh.foamsnet.com/2013/06/using-hash-tags-to-organize-bash-history.html
.. _numerous drawbacks: http://www.reddit.com/r/commandline/comments/1hcyb0/using_hash_tags_to_organize_bash_history/
.. _update the history file: http://stackoverflow.com/questions/15075523/how-can-i-make-bash-history-update-more-often
.. _not be available in a new terminal: http://unix.stackexchange.com/questions/1288/preserve-bash-history-in-multiple-terminal-windows
.. _length of the history file: http://stackoverflow.com/questions/9457233/unlimited-bash-history/19533853#19533853
.. _shellsink: http://shell-sink.blogspot.com/
.. _addresses many of these problems: https://www.debian-administration.org/article/625/Making_The_Bash_History_More_Useful
.. _appears to be inactive: https://groups.google.com/forum/#!topic/shell-sink/RxMP6AsT5zw
.. _as of mid 2011: https://github.com/joshuacronemeyer/shellsink

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
How is this different from, say, an offline cache of commandlinefu.com?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Commandlinefu`_ is a remarkable and dedicated online community,
but there are some things it lacks or was never designed to have, such as:

#. Metadata and search based on metadata.
#. Cross-referencing.
#. Unique (SHA-1) and string similarity (Nilsimsa) hashes of command invocations.
#. Explicit open-source licensing.

In addition, the focus of Commandlinefu is in providing a platform for commenting and upvoting,
which is a different focus than a custom repository of specialized shell commands,
many of which may only be useful to their creator.

.. _Commandlinefu: http://www.commandlinefu.com/

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

They can be:

- used in conditional sequence (e.g. ``./configure && make``),
- piped together (e.g. ``du | sort -nr``),
- evaluated to supply arguments to other commands (e.g. ``mkdir $(date -I)``),
- or even taken directly as arguments to other commands (e.g. ``find . -exec file '{}' +``).

These composite commands consist of more than one component command.

Component commands may be
executables in ``$PATH``,
absolute paths to executables,
shell builtins (``cd``),
or shell keywords (``for``, ``do``).

They could in principle be custom shell functions or aliases,
but those are best kept in your favorite ``.shellrc``,
not in a CmdOyster.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
What's the difference between commands and invocations?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is almost always more than one way to write the same command,
such as long flag/short flag versions,
a different order of arguments,
or just a different method,
e.g. removing a file in the current directory named ``-``
using either ``rm ./-`` or ``rm -- -``.

Since these cosmetically different commands use the same component commands,
it makes more sense to group them together
rather than list them redundantly as separate commands.

These are said to be equivalent invocations of the same command.

If there is a similar command that uses different component commands,
it must be listed as a different command,
not an equivalent invocation;
e.g. ``unlink -`` will accomplish the same thing as ``rm ./-``,
but it must be listed as a different command.

However, these related CmdOysters can (and should) be `cross-referenced`_.

The rationale for this is partly the simplicity of implementation
and to prevent a single CmdOyster from storing too much,
but also because different component commands have different behaviors and semantics.

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
Is it OK for command invocations to span multiple lines?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, but one-liners are the focus for now.

CmdOysters are intended to aid interactive use of command-line programs,
such as quick calculations,
interacting with processes,
debugging,
and providing core building blocks of shell scripts.

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
Once the ``nilsimsa`` library is migrated to Python 3,
the scripts can also be migrated.

Please do feel free to write code for working with CmdOysters in your favorite language;
that's why they are JSON data!

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
so while the license field is not strictly required for a valid CmdOyster,
it is strongly encouraged to ensure others may copy and modify the CmdOysters without fear of infringement or litigation.

.. _extent to which metadata is copyrightable: http://lj.libraryjournal.com/2013/02/opinion/peer-to-peer-review/metadata-and-copyright-peer-to-peer-review/

---------------------------------
Example of making a new CmdOyster
---------------------------------

Python has had a built-in JSON library since version 2.6.
The optional `nilsimsa library`_ can be installed with::

    pip install nilsimsa

which appears to currently be Python 2 only.

.. _nilsimsa library: https://pypi.python.org/pypi/nilsimsa/0.3.2

Copy `<testing/62f6a0e19cae58eefb0e39bc09aaf7b9469202e5.json>`_ to ``testing/temp.json``.

Edit ``temp.json``, changing at least the ``description`` and ``invocation`` strings.

Run ``python2 validate-database.py --fix --input testing/``
to supply the SHA-1 and Nilsimsa hashes
(``make cmd_oyster_testing`` does the same thing).

Copy over some of the fields from other entries
or from `<templates/full-command-template.json>`_
and supply the new values as necessary.

Run ``make`` to ensure the JSON is valid.

Continue adding metadata and invocations until satisfied.

Rename file to the SHA-1 hash of its description,
appended with ``.json``.

Move the JSON file into `<CmdOysters/>`_.

--------------------------------------------
How to add new metadata fields to the schema
--------------------------------------------

Add the field to `<schemas/full-schema.json>`_.

See http://json-schema.org/documentation.html
or
https://spacetelescope.github.io/understanding-json-schema/
for help on JSON schemas.

Note that the best command metadata to include in a CmdOyster is information that is:

- not readily available in man pages,

- directly applicable to the specific use of the invocation,

- and easy to verify or falsify.

-------
License
-------

The code for this project is licensed under the `MIT`_ (a.k.a `Expat`_) license.

The individual CmdOysters may have different licenses,
as they are JSON documents containing license information as part of their metadata.

.. _MIT: http://opensource.org/licenses/MIT

.. _Expat: http://directory.fsf.org/wiki/License:Expat

-------------------
Future improvements
-------------------

See `<TODO.rst>`_.

Here are some highlights, in no particular order:

- Incremental search interface.

- Generate list of required packages that need to be installed to use a given command, depending on OS.

- Spawn a shell with the command automatically filled in and ready to edit or press enter.

- Extend CmdOysters to interactive textual commands in general,
  such as ``gnuplot``, ``ipython``, ``irb``, ``maxima``, and so on.
