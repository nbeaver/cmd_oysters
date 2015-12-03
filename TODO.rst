====
TODO
====

----------------------------------------------
Specific items by file, in no particular order
----------------------------------------------

- ``[*]`` Make a minimal template with only required fields (`<templates/minimal-template.json>`_).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`<schemas/full-schema.json>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``[ ]`` Use a copyright fields like Debian's: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/

- ``[*]`` Specify required commands.

- ``[x]`` Make sha1-hash of related urls a required field. (Abandoned because these are not intended to be unique.)

- ``[*]`` Check that ``bash-type`` is one of ``keyword``, ``builtin``, or ``file``.

- ``[*]`` Split command database into individual JSON files.

- ``[*]`` Include version numbers in "commands this shell works with/doesn't work with".

- ``[*]`` Change field name from ``compatible-shells`` to ``compatible-with`` so it's more generic.

- ``[*]`` Split requirements into ``requirements-in-general`` and ``requirements-as-invoked``.

- ``[ ]`` Indicate XORs in dependencies for Debian packages, e.g. ``gawk | mawk``.

- ``[x]`` Use ``null`` for ``executable-path`` of shell builtins and keywords. (Abandoned since nulls tend to cause problems.)

- ``[*]`` Combine debian-paths and debian-packages into single debian tree.

- ``[*]`` Combine ``component-command-*`` into ``component-command-info/*``.

- ``[*]`` Change ``related-commands`` to a list of objects, not SHA-1 hashes, so that e.g. broken links to similar commands can be found by Nilsima hash.

- ``[*]`` Change ``related-invocations`` to a list of objects, not SHA-1 hashes, so that e.g. broken links to similar invocations can be found by Nilsima hash.

- ``[*]`` Change ``relevant-urls`` to a list of objects, not strings, so that e.g. additional information about the URL can be added.

- ``[*]`` A "copying" object field.

  - ``[*]`` A "license" field.
  - ``[*]`` An "author" or "acknowledgements" field.
  - ``[*]`` A year field.

- ``[ ]`` Field that indicates if the invocation is a pipeline, since the presence of a pipe character is not a reliable indication.

- ``[*]`` Field for example output of command (only some of them, obviously).
  - ``[ ]`` Include output of ``locale`` command for these.

- ``[*]`` Change ``shell`` compatibility to a list of objects.

- ``[*]`` Enumerate fields with ``yes|no|maybe`` and ``never|sometimes|always`` options.

- ``[ ]`` Split it into smaller sub-schemas to avoid duplication.

- ``[*]`` Take descriptions from old pseudo-schema.

- ``[ ]`` Be more specific about required OS.

- ``[ ]`` Be more specific about other non-command dependencies, e.g. which commands require an X server.

- ``[x]`` Change ``string`` to ``invocation-string`` and ``description-string``. This makes ad-hoc grepping easier.
  - Disadvantage: Makes validation code messier.

- ``[x]`` Key invocations by invocation string instead of using a separate "string" field.
  - Disadvantage: Would be a breaking change.
  - Disadvantage: Would not prevent duplicate invocations: https://stackoverflow.com/questions/17063257/necessity-for-duplicate-keys-in-json-object
  - Disadvantage: Would make ad-hoc grepping even harder.

- ``[*]`` Change structure of invocations to a list of objects, so that they do not require a shell name.

- ``[*]`` Add a ``comment`` field to each invocation.

- ``[*]`` Change ``url-string`` to just ``string`` for consistency.

- ``[*]`` Change ``url-sha1-hash`` to just ``sha1-hash`` for consistency.

- ``[*]`` Change ``url-nilsimsa-hash`` to just ``nilsimsa-hash`` for consistency.

- ``[*]`` Add a ``compatible-sha1-hashes`` field for shells.

- ``[*]`` Add a ``compatible-sha1-hashes`` field for component commands.

  - Also check BuildID?

- ``[ ]`` Use a UUID instead of SHA1/nilsimsa of description string.
  - Advantage: would prevent forced updates whenever the description changes,
    while still keeping the option for finding similar descriptions via Nilsimsa.

- ``[ ]`` Add a ``depends-on-working-directory`` field to invocations.

- ``[ ]`` Add an ``idempotent`` field to invocations.
  - This is helpful in case it unclear if the command has already been run before.

- ``[x]`` Add a ``depends-on-locale`` field to invocations.
  - Decided this was too general, but local information should be part of example outputs.

- ``[ ]`` Add a ``shibboleth-command`` field to invocations,
  e.g. ``ls --version`` will return 0 for the GNU version of ``ls``
  but 1 for the BSD version of ``ls``.

- ``[ ]`` Add a ``warning`` or ``caution`` field.

- ``[ ]`` Indicate if the command is POSIX-standard,
  and if so, which version of POSIX.

~~~~~~~~~~~~~~~~~~~~
`<find-command.py>`_
~~~~~~~~~~~~~~~~~~~~

- ``[ ]`` Add a ``--shell`` flag (short flag ``-x``) to spawn a prompt for the user with the command already filled in (use ``pexpect``).

  - ``[ ]`` Tailor invocation according to host OS and environment.
  - ``[ ]`` Add a config file for e.g. preferred shell.
  - ``[ ]`` Check if dependencies are installed, and generate OS-specific command (e.g. ``apt-get``) to install the necessary packages.

- ``[ ]`` Syntax highlighting of output. (This will complicate things because terminal might have a light or dark background.)

- ``[*]`` Take ``--commands`` argument and search in component commands.

- ``[ ]`` Take multiple arguments to ``--substring`` so it's effectively a regex search for ``arg1.*arg2.*arg3``.

- ``[ ]`` Add a flag for excluding patterns.

- ``[ ]`` Add a flag for excluding commands.

- ``[*]`` Add a ``--description`` search.

  - ``[ ]`` Make the description search case-insensitive.
  - ``[ ]`` Make the description search into a full regex search.

- ``[ ]`` Do some unit tests instead of the hacky makefile tests.

- ``[*]`` Add a description token search, stripping out punctuation.

  - ``[ ]`` Add `stemming`_ or `lemmatising`_.

- ``[ ]`` Incremental search for all search modes, possibly using ``ncurses``.

- ``[ ]`` Add an ``--edit`` command to open the json file in the user's ``$EDITOR``.

- ``[ ]`` Add a ``--case-sensitive`` flag for searching, since case-insensitive is a convenient default,
  but sometimes case-sensitivity can make a big difference in matching results.

.. _stemming: https://pythonhosted.org/Whoosh/stemming.html
.. _lemmatising: http://marcobonzanini.com/2015/01/26/stemming-lemmatisation-and-pos-tagging-with-python-and-nltk/

~~~~~~~~~~~~~~~~~~~~~~~~~
`<validate-database.py>`_
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``[*]`` Check all the commands in component commands are substrings of the main command.

- ``[ ]`` Check that the commands in ``component-command-info`` are a subset of ``component-commands``.

- ``[ ]`` Check ``debian-path`` is correct using ``which``.

- ``[*]`` Check that no two commands have the same SHA1s of description text.

- ``[ ]`` Check for likely duplicates based on Nilsimsa hashes of both commands and descriptions (use nilsimsa.compare_digests).

- ``[*]`` Make a JSON schema to do at least part of this more systematically.

- ``[*]`` Check that the filename is the same as the SHA1 of the description, plus ``.json``.

- ``[ ]`` Check that the fields are in alphanumeric order.

- ``[*]`` Correct the SHA1 and Nilsimsa values automatically, prompting before writing them out to file.

- ``[ ]`` Figure out some way to do fine-grained validation, so once a CmdOyster has been checked, it won't be checked again until it changes.

- ``[ ]`` Check that all the SHA1s of related commands are actually in the database (will require a dict associating the link to the file, so we know later which one the link was in).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`<templates/full-command-template.json>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``[ ]`` Ensure that every field in the schema is in this template.

~~~~~~~~~~~~~
`<Makefile>`_
~~~~~~~~~~~~~

- ``[*]`` Don't check all CmdOysters by default (make it a separate target).

-----------------------------------
Non-specific notes and observations
-----------------------------------

- Add information about how to exit an interactive command, e.g.:

  - root -l: ``exit()<Enter>`` (Ctrl-D and Ctrl-C don't work)
  - ssh: Have to use ``<Enter>~.`` when a connection hangs.
  - pacmd: ``Ctrl-D`` (don't use ``exit`` or you'll kill the daemon.
  - ed: use ``q<Enter>`` (and nothing else)
  - vim: ``:quit!<Enter>`` or ``ZQ``
  - emacs: ``Ctrl-X Ctrl-C``
  - nano: ``Ctrl-X``
  - wine cmd: ``exit``, not ``quit`` or ``Ctrl-D``.
  - maxima: ``Ctrl-D`` or ``quit();<Enter>``
  - irb: ``quit<Enter>`` or ``Ctrl-D``
  - gnuplot: ``quit<Enter>``, ``exit<Enter>``, or ``Ctrl-D``.

  Or should this be a separate project?

- Would be good to extend this to work for any programming language, not just shells.

- Sometimes changeable arguments show up more than once -- should slice be a list of slices?

- Omit requirements for shell keywords, since they don't do anything on their own? Or use ``null``?

- Required packages for shell keywords and builtins -- just omit them, since it depends on the shell anyway? Or use ``null``?

- Requirements are vague, e.g. using ``ls`` in an ``sshfs`` does require an internet connection, but only indirectly.

- The "always, sometimes, never" is a useful distinction, but what about "depends on flags" or "depends on the arguments" or "depends on configuration" or "depends on shell"?

- Decide which fields are required and which are optional (JSON schema?).

- Note: don't use Nilsimsa for one-letter or two-letter commands;
  Nilsimsa of "ls", "rm", "cd", "cp", "bc", "du", "df", "ln", and "bg" is the same:
  '0000000000000000000000000000000000000000000000000000000000000000'

- ``man xclip``: "I hate man pages without examples!"

- It's kind of a hassle to have to change all the SHA-1 links and filename every time the description changes,
  but the Nilsimsa hash helps.

- What is the best way to handle commands that are the same but have different executable names due to forking, e.g. ``avconv`` and ``ffmpeg``?

- Would be good to differentiate commands that can be run as-is, and commands that need different arguments.

----------------------
Getting shell versions
----------------------

- bsh: echo 'printBanner();' | bsh
- bash: bash --version
- csh:  dpkg -s csh | grep Version | cut -d ' ' -f 2 # https://stackoverflow.com/questions/14259723/how-can-i-determine-my-csh-version
- dash: dpkg -s dash | grep Version | cut -d ' ' -f 2 # https://askubuntu.com/questions/283134/how-to-find-the-version-of-the-dash-shell-on-ubuntu-bin
- fish: fish --version
- ksh: ksh --version
- lshell: lshell --version
- lush: dpkg -s lush | grep Version | cut -d ' ' -f 2
- mksh: mksh -c 'echo $KSH_VERSION'
- posh: posh -c 'echo $POSH_VERSION'
- rc: rc -c 'echo $version'
- sash: dpkg -s sash | grep Version: | cut -d ' ' -f 2
- tcsh: tcsh --version
- yash: yash --version
- zsh: zsh --version

"bsh", "bash", "csh", "dash", "fish", "ksh", "mksh", "posh", "tcsh", "zsh",
