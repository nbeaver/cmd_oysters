====
TODO
====

----------------------------------------------
Specific items by file, in no particular order
----------------------------------------------

- ``[*]`` Make a minimal template with only required fields (`<command-templates/minimal-template.json>`_).

~~~~~~~~~~~~~~~~~~~~~~~~~~~
`<check-full-template.py>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``[*]`` Verify that all the pseudo-schema fields are in `<command-templates/full-command-template.json>`_.

~~~~~~~~~~~~~~~
`<CmdOysters>`_
~~~~~~~~~~~~~~~

- ``[*]`` Split `<command-database.json>`_ into individual JSON files.

- ``[ ]`` Include version numbers in "commands this shell works with/doesn't work with".

- ``[*]`` Change field name from ``compatible-shells`` to ``compatible-with`` so it's more generic.

- ``[*]`` Split requirements into ``requirements-in-general`` and ``requirements-as-invoked``.

- ``[ ]`` Indicate XORs in dependencies for Debian packages, e.g. ``gawk | mawk``.

- ``[*]`` Use ``null`` for ``executable-path`` of shell builtins and keywords.

- ``[*]`` Combine debian-paths and debian-packages into single debian tree.

- ``[*]`` Combine ``component-command-*`` into ``component-command-info/*``.

- ``[ ]`` Change ``related-commands`` to a list of objects, not SHA-1 hashes, so that e.g. broken links to similar commands can be found by Nilsima hash.

- ``[ ]`` Change ``related-invocations`` to a list of objects, not SHA-1 hashes, so that e.g. broken links to similar invocations can be found by Nilsima hash.

- ``[ ]`` Change ``relevant-urls`` to a list of objects, not SHA-1 hashes, so that e.g. additional information about the URL can be added.

- ``[ ]`` A "copying" object field.

  - ``[ ]`` A "license" field.
  - ``[ ]`` An "author" or "acknowledgements" field.
  - ``[ ]`` A date field.

- ``[ ]`` Field that indicates if the invocation is a pipeline, since the presence of a pipe character is not a reliable indication.


~~~~~~~~~~~~~~~~~~~~
`<find-command.py>`_
~~~~~~~~~~~~~~~~~~~~

- ``[ ]`` Add a ``--shell`` flag (short flag ``-x``) to spawn a prompt for the user with the command already filled in (use ``pexpect``).

  - ``[ ]`` Tailor invocation according to host OS and environment.
  - ``[ ]`` Add a config file for e.g. preferred shell.
  - ``[ ]`` Check if dependencies are installed, and generate OS-specific command (e.g. ``apt-get``) to install the necessary packages.

- ``[ ]`` Syntax highlighting of output.

- ``[*]`` Take ``--commands`` argument and search in component commands.

- ``[ ]`` Take multiple arguments to ``--substring`` so it's effectively a regex search for ``arg1.*arg2.*arg3``.

- ``[ ]`` Add a flags for excluding patterns and commands.

- ``[*]`` Add a ``--description`` search.

  - ``[ ]`` Make the description search case-insensitive.
  - ``[ ]`` Make the description search into a full regex search.

- ``[ ]`` Do some unit tests instead of the hacky makefile tests.

- ``[*]`` Add a description token search, stripping out punctuation.

  - ``[ ]`` Add `stemming`_ or `lemmatising`_.

- ``[ ]`` Incremental search for all search modes, possibly using ``ncurses``.

.. _stemming: https://pythonhosted.org/Whoosh/stemming.html
.. _lemmatising: http://marcobonzanini.com/2015/01/26/stemming-lemmatisation-and-pos-tagging-with-python-and-nltk/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`<pseudo-schema-notes.markdown>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``[*]`` Specify which fields are required.

~~~~~~~~~~~~~~~~~~~~~~~~~
`<validate-database.py>`_
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``[*]`` Check all the commands in component commands are substrings of the main command.
- ``[ ]`` Check that ``bash-type`` is one of ``keyword``, ``builtin``, or ``file``.
- ``[ ]`` Check that the commands in ``component-command-info`` are a subset of ``component-commands``.
- ``[ ]`` Check ``debian-path`` is correct using ``which``.
- ``[*]`` Check that no two commands have the same SHA1s of description text.
- ``[ ]`` Make a JSON schema to do at least part of this more systematically.

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
