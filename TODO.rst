====
TODO
====

---------------------------------------
Specific items (in no particular order)
---------------------------------------

- ``[ ]`` Split `<command-database.json>`_ into individual JSON documents.

- ``[ ]`` Tailor invocation according to host OS and environment.

- ``[ ]`` Add a config file for e.g. preferred shell.

- ``[ ]`` Include version numbers in "commands this shell works with/doesn't work with".

- ``[ ]`` Change field name from ``compatible-shells`` to ``compatible-with`` so it works

- ``[*]`` `<validate-database.py>`_: Verify that all the pseudo-schema fields are in `<command-template.json>`_.

- ``[ ]`` `<find-command.py>`_: Add a --shell -x flag to spawn a prompt for the user with the command already filled in (use pexpect).

- ``[*]`` Split requirements into ``requirements-in-general`` and ``requirements-as-invoked``.

- ``[ ]`` Indicate options for alternatives in Debian packages, e.g. ``mawk`` or ``gawk``, but not both.

- ``[ ]`` Use ``null`` for ``executable-path`` of shell builtins and keywords.

- ``[ ]`` `<find-command.py>`_: Syntax highlighting of output.

- ``[*]`` Say which fields are required in `<pseudo-schema-notes.markdown>`_.

- ``[*]`` Make a minimal template with only required field (`<minimal-template.json>`_).

- ``[ ]`` Make a JSON schema.

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
  - maxima: ``Ctrl-D`` or ``quit();``

  Or should this be a separate project?

- Would be good to extend this to work for any programming language, not just shells.

- Sometimes changeable arguments are repeated -- should slice be a list of slices?

- Omit requirements for shell keywords, since they don't do anything on their own? Or use null?

- Required packages for shell keywords and builtins -- just omit them, since it depends on the shell anyway? Or use null?

- Requirements are vague, e.g. using ``ls`` in an sshfs does require an internet connection, but only indirectly.

- Decide which fields are required and which are optional (JSON schema?).

- Note: don't use Nilsimsa for one-letter or two-letter commands;
  Nilsimsa of "ls", "rm", "cd", "cp", "bc", "du", "df", "ln", and "bg" is the same:
  '0000000000000000000000000000000000000000000000000000000000000000'

- ``man xclip``: "I hate man pages without examples!"

