.. -*- coding: utf-8 -*-

=========================================
CmdOysters: shell commands with metadata.
=========================================

:Author: Nathaniel Beaver
:Date: $Date: 2016-02-10 (Wednesday, 10 February 2016) $
:Copyright: This document is licensed under a Creative Commons Attribution 4.0 International license.

See also `<todo.md>`_.

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
            "verbose-description": "List contents of a directory."
        },
        "invocations": {
            {
                "invocation-string": "ls"
            }
        },
        "uuid": "535f7bb6-09ae-4105-a69c-e576ece9b113"
    }

Here are some less trivial examples:

- `Highlight the non-ASCII characters in a text file <cmdoysters/7b93628a-938d-4227-a88c-9d697f55fac4.json>`_.

- `Safely list hidden files <cmdoysters/924d5f3a-512b-4c0e-8219-6a47002d9014.json>`_.

- `Change the current user's default shell <cmdoysters/7a49c243-47f7-4a5a-a42a-87357d134b0d.json>`_.

- `Extract images from multiple PDFs <cmdoysters/6c0081a3-5c10-4cdf-826b-1bd778ae8ef0.json>`_.

- `Display the machine's CPU architecture <cmdoysters/f69252a3-a58b-48bc-9fd2-89e9e5d29f94.json>`_.

----------
Quickstart
----------

#. ``git clone https://github.com/nbeaver/cmd-oysters``

#. ``cd cmd-oysters/``

#. ``python2 find_command.py --substring "ping -i"``

More examples:

#. ``python2 find_command.py --commands awk grep``

#. ``python2 find_command.py --tokens '|' '~'``
   
#. ``python2 find_command.py --description-tokens architecture CPU``

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

- Are straightforward to query because of robust metadata
  instead of more fragile search methods such as regular expressions.

- Link to URIs of sources and relevant documentation.

Example scenarios this is intended to be useful for:

- Restarting a WiFi card without a working internet connection
  to look up the required commands.

- Building up a complex ``find`` command by combining simpler examples.

- Leveraging well-known commands without the hazards of
  `copying and pasting them from online forums into a terminal`_.

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

~~~~~~~~~~~~~~~~~~~~~~~
Avoidance of metasyntax
~~~~~~~~~~~~~~~~~~~~~~~

An example command invocation in a CmdOyster
should resemble real usage as much as possible,
and ideally should be runnable as-is on an actual system.

For example::

    grep -nP '[^[:ascii:]]' --color=always /usr/share/dict/words | less -R

is a better example than::

    grep -nP '[^[:ascii:]]' --color=always /path/to/file.txt | less -R

which is better than::

    grep -nP '[^[:ascii:]]' --color=always foo | less -R

which is better than::

    grep -nP '[^[:ascii:]]' foo

which is better than::

    grep -nP '[^[:ascii:]]' [FILE...]

even though the last example is the most abstract, general case.

For the purposed of the CmdOysters,
the "best" example is not the most general,
it is the one that is closest to an example that can be run without modification.

Thus, metasyntax designed to show all the possible uses of a command,
or make the example more abstract,
such as the man-page convention ``[FILE...]``,
or `metasyntactic variables`_ like ``foo`` and ``bar``,
are not good examples for a CmdOyster.

.. _metasyntactic variables: https://en.wikipedia.org/wiki/Metasyntactic_variable

~~~~~~~~~~~~~~~~~~~~~
Simple textual format
~~~~~~~~~~~~~~~~~~~~~

CmdOysters are text files in the JSON data serialization format.

Of textual data serialization formats,
JSON and YAML are the simplest and most widespread standardized formats.

Well-maintained JSON parsing and schema libraries
are readily available for most programming languages,
but the same is unfortunately not true for YAML.

A directory of JSON files
makes code work cross-platform and cross-language easily.

In addition, JSON permits Unicode
and only requires escaping double quotes and backslashes,
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
but version number is not always a reliable indication
of command compatibility.

For example, the maximum integer that the ``factor`` command will accept
depends on whether it was compiled with ``bignum`` support.
This does not change the version information,
but it does change the SHA-1 checksum of the binary.

To be sure, posessing the same SHA-1 checksum for the binary
does not guarantee the same result
because of e.g. differing config files.
However, if the SHA-1 is identical,
it is easier to eliminate cause of the misbehavior.

~~~~~~~~~~~~~
Extensibility
~~~~~~~~~~~~~

Frequently, new fields can be added to JSON documents
without breaking existing code.

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
and that updating one CmdOyster's description
requires updating all the CmdOysters that point to it,
but it evades some of the problems that URIs and file paths have,
such as maintaining hierarchies and using arbitrary identifiers.

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
#. Unique (SHA-1) hashes of command invocations.
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

This is intended to protect both those who make their own CmdOysters
and those who use them.

It may seem strange to have a license for what amounts to one line of code,
but the command invocation is just one part
of a JSON document that could be construed as a creative work,
so an explicit grant of copyright is always better than an ambiguous one.

The `extent to which metadata is copyrightable`_
varies by country and is still somewhat controversial,
so while the license field is not strictly required for a valid CmdOyster,
it is strongly encouraged to ensure others may copy and modify the CmdOysters
without fear of infringement or litigation.

.. _extent to which metadata is copyrightable: http://lj.libraryjournal.com/2013/02/opinion/peer-to-peer-review/metadata-and-copyright-peer-to-peer-review/

---------------------------------
Example of making a new CmdOyster
---------------------------------

Python has had a built-in JSON library since version 2.6.

Run ``python generate_oyster.py`` to generate a new CmdOyster::

    $ python generate_oyster.py 
    Created new CmdOyster:
    /path/to/cmd-oysters/cmdoysters/6720d31b-511c-4b48-bf0e-073ec72c9234.json

This will create a minimal CmdOyster and a new UUID;
6720d31b-511c-4b48-bf0e-073ec72c9234 in this case.
Inspect the JSON with your favorite editor.

You will probably want to copy over some of the fields from other entries
or from `<templates/full-command-template.json>`_.

Run ``python cmdoysters/6720d31b-511c-4b48-bf0e-073ec72c9234.json schemas/full-schema.json``
or simply::

    cd cmdoysters/
    make

to ensure the JSON is valid.

Continue adding metadata and invocations until satisfied.

--------------------------------------------
How to add new metadata fields to the schema
--------------------------------------------

Add the field to `<schemas/full-schema.json>`_.

Resources on writing JSON schemas:

- http://json-schema.org/documentation.html
- https://spacetelescope.github.io/understanding-json-schema/

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

See `<todo.md>`_.

Here are some highlights, in no particular order:

- Incremental search interface.

- Generate list of required packages that need to be installed to use a given command, depending on OS.

- Spawn a shell with the command automatically filled in and ready to edit or press enter.

- Extend CmdOysters to interactive textual commands in general,
  such as ``gnuplot``, ``ipython``, ``irb``, ``maxima``, and so on.
