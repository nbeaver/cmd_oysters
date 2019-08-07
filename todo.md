TODO
====

Specific items by file, in no particular order
----------------------------------------------

-   [x] Make a minimal template with only required fields ([templates/simple-template.json](templates/simple-template.json)).

### [schemas/full-schema.json](schemas/full-schema.json)

-   [ ] Add a field for explaining the meaning of flags even if they don't take an argument.

-   [ ] Add field for specifying dependency on environment variables like `$HOME`, `$LANG`, `$TERM`, and `$DISPLAY`,
        as well as locale (e.g. `sort` is affected by `LC_COLLATE`)

    - Useful for e.g. commands that require an X11 server, so won't work in a TTY or on Cygwin.

-   [ ] Use a copyright fields like Debian's: <https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/>

-   [x] Specify required commands.

-   [x] Check that `bash-type` is one of `keyword`, `builtin`, or `file`.

-   [x] Split command database into individual JSON files.

-   [x] Include version numbers in "commands this shell works with/doesn't work with".

-   [x] Change field name from `compatible-shells` to `compatible-with` so it's more generic.

-   [x] Split requirements into `requirements-in-general` and `requirements-as-invoked`.

-   [ ] Indicate XORs in dependencies for Debian packages, e.g.  `gawk | mawk`.

-   [ ] Use `null` for `executable-path` of shell builtins and keywords.
    - Abandoned since `null`s in JSON tend to cause problems.

-   [x] Combine debian-paths and debian-packages into single debian tree.

-   [x] Combine `component-command-*` into `component-command-info/*`.

-   [x] Change `related-commands` to a list of objects, not SHA-1 hashes, so that e.g. broken links to similar commands can be found by Nilsima hash.

-   [x] Change `related-invocations` to a list of objects, not SHA-1 hashes, so that e.g. broken links to similar invocations can be found by Nilsima hash.

-   [x] Change `relevant-urls` to a list of objects, not strings, so that e.g.  additional information about the URL can be added.

-   [x] A "copying" object field.
    -   [x] A "license" field.
    -   [x] An "author" or "acknowledgements" field.
    -   [x] A year field.

-   [ ] Field that indicates if the invocation is a pipeline, since the presence of a pipe character is not a reliable indication.

-   [x] Field for example output of command (only some of them, obviously).
    -   [ ] Include output of `locale` command for these.

-   [x] Change `shell` compatibility to a list of objects.

-   [x] Enumerate fields with `yes|no|maybe` and `never|sometimes|always`.

-   [ ] Split it into smaller sub-schemas to avoid duplication.

-   [x] Take descriptions from old pseudo-schema.

-   [ ] Be more specific about required OS.

-   [ ] Be more specific about other non-command dependencies.
    -   For example, `xev` requires an X server, and `ssh -X` doesn't make much sense without an X server.

-   [x] Change `string` to `invocation-string` and `description-string`.  This makes ad-hoc grepping easier.

-   [ ] Key invocations by invocation string instead of using a separate "string" field.
    -   Advantage: more elegant structure.
    -   Disadvantage: Would be a breaking change.
    -   Disadvantage: Would not prevent duplicate invocations: <https://stackoverflow.com/questions/17063257/necessity-for-duplicate-keys-in-json-object>
    -   Disadvantage: Would make ad-hoc grepping even harder.

-   [x] Change structure of invocations to a list of objects, so that they do not require a shell name.

-   [x] Add a `comment` field to each invocation.

-   [x] Change `url-string` to just `string` for consistency.

-   [x] Add a `compatible-sha1-hashes` field for shells.

-   [x] Add a `compatible-sha1-hashes` field for component commands.
    -   Also check BuildID?

-   [x] Use a UUID instead of SHA1/nilsimsa.
    -   Advantage: would prevent forced updates whenever the description changes, while still keeping the option for finding similar descriptions via Nilsimsa.

-   [ ] Add a `depends-on-working-directory` field to invocations.

-   [ ] Add an `idempotent` field to invocations.
    -   This is helpful in case it unclear if the command has already been run before.

-   [x] Add a `depends-on-locale` field to invocations.
    -   Decided this was too general, but locale information should be part of example outputs.

-   [x] Add a `shibboleth` field to invocations, e.g. `ls --version` will return 0 for the GNU version of `ls` but 1 for the BSD version of `ls`.

    -   Could also do something more elaborate like `ls --version | head -n 1 | cut -d ' ' -f 4` to get version number, but this is too brittle and complicated.

    -   Two kinds of shibboleths: "likely to work" and "likely to fail", with corresponding output and return codes.

-   [ ] Add a `warning` or `caution` field.

-   [ ] Indicate if the command is POSIX-standard, and if so, which version of POSIX.

-   [ ] Link to commands to try if it fails based on error number.

-   [ ] Two different descriptions, one terse (80 characters or less), and one verbose.

### [cmdoysters.py](cmdoysters.py)

-   [ ] Add a `--shell` flag (short flag `-x`) to spawn a prompt for the user with the command already filled in (use `pexpect`).
    -   [ ] Tailor invocation according to host OS and environment.
    -   [ ] Add a config file for e.g. preferred shell.
    -   [ ] Check if dependencies are installed, and generate OS-specific command (e.g. `apt-get`) to install the necessary packages.

-   [ ] Syntax highlighting of output. (This will complicate things because terminal might have a light or dark background.)

-   [x] Take `--commands` argument and search in component commands.

-   [ ] Take multiple arguments to `--substring` so it's effectively a regex search for `arg1.*arg2.*arg3`.

-   [ ] Add a flag for excluding patterns.

-   [ ] Add a flag for excluding commands.

-   [x] Add a `--description` search.
    -   [ ] Make the description search case-insensitive.
    -   [ ] Make the description search into a full regex search.

-   [ ] Do some unit tests instead of the hacky makefile tests (use `unittest` module).

-   [x] Add a description token search, stripping out punctuation.
    -   [ ] Add [stemming](https://pythonhosted.org/Whoosh/stemming.html) or [lemmatising](http://marcobonzanini.com/2015/01/26/stemming-lemmatisation-and-pos-tagging-with-python-and-nltk/).

-   [ ] Incremental search for all search modes, possibly using `ncurses`.

-   [ ] Add an `--edit` command to open the json file in the user's `$EDITOR`.

-   [ ] Add a `--case-sensitive` flag for searching, since case-insensitive is a convenient default, but sometimes case-sensitivity can make a big difference in matching results.

-   [ ] More options for output formatting.
    -   [ ] Use short descriptions instead of long descriptions.
    -   [ ] Terse output (commands only, no comments). Or should this be by default?
    -   [ ] Show explanations of flags and changeable arguments.
    -   [ ] Show relevant URLs.


### [validate_database.py](validate_database.py)

-   [x] Check that no two commands have the same UUIDs.

-   [ ] Check for likely duplicates based on Nilsimsa hashes of both commands and descriptions (use `nilsimsa.compare_digests`).


### [validate_oyster.py](validate_oyster.py)

-   [x] Check all the commands in component commands are substrings of the main command.

-   [ ] Check that the commands in `component-command-info` are a subset of `component-commands`.

-   [ ] Check `debian-path` is correct using `which`.

-   [x] Make a JSON schema to do at least part of this more systematically.

-   [x] Check that the filename is the same as the UUID, plus `.json`.

-   [ ] Check that the fields are in alphanumeric order.

-   [x] Check that `component-command-flag` is a substring of `invocation-string`.


### [templates/full-command-template.json](templates/full-command-template.json)

-   [ ] Ensure that every field in the schema is in this template.

### [cmdoysters/Makefile](cmdoysters/Makefile)

-   [x] Figure out some way to do fine-grained validation, so once a CmdOyster has been checked, it won't be checked again until it changes.
-   [x] Don't check all CmdOysters by default (make it a separate target).


Non-specific notes and observations
-----------------------------------

-   Add information about how to exit an interactive command, e.g.:

    -   root -l: `exit()<Enter>` (Ctrl-D and Ctrl-C don't work)
    -   ssh: Have to use `<Enter>~.` when a connection hangs.
    -   pacmd: `Ctrl-D` (don't use `exit` or you'll kill the daemon.
    -   ed: use `q<Enter>` (and nothing else)
    -   vim: `:quit!<Enter>` or `ZQ`
    -   emacs: `Ctrl-X Ctrl-C`
    -   nano: `Ctrl-X`
    -   wine cmd: `exit`, not `quit` or `Ctrl-D`.
    -   maxima: `Ctrl-D` or `quit();<Enter>`
    -   irb: `quit<Enter>` or `Ctrl-D`
    -   gnuplot: `quit<Enter>`, `exit<Enter>`, or `Ctrl-D`.

    Or should this be a separate project?

-   Would be good to extend this to work for any programming language,
    not just shells.
-   Sometimes changeable arguments show up more than once --
    should slice be a list of slices?
-   Omit requirements for shell keywords,
    since they don't do anything on their own?
    Or use `null`?
-   Required packages for shell keywords and builtins --
    just omit them, since it depends on the shell anyway?
    Or use `null`?
-   Requirements are too vague, e.g.
    using `ls` in an `sshfs` does require an internet connection,
    but only indirectly.
-   The "always, sometimes, never" is a useful distinction,
    but what about "depends on flags"
    or "depends on the arguments"
    or "depends on configuration"
    or "depends on shell"?
-   Decide which fields are required and which are optional (JSON schema?).
-   Note: don't use Nilsimsa for one-letter or two-letter commands;
    Nilsimsa of "ls", "rm", "cd", "cp", "bc", "du", "df", "ln", and "bg"
    is the same:
    '0000000000000000000000000000000000000000000000000000000000000000'
-   From `xclip` man page: "I hate man pages without examples!"
-   What is the best way to handle commands that are the same
    but have different executable names due to forking,
    e.g. `avconv` and `ffmpeg`?
-   Would be good to differentiate commands that can be run as-is
    and commands that need different arguments.
- Add UUID per invocation.

Getting shell versions
----------------------

-   bsh: `echo 'printBanner();' | bsh`
-   bash: `bash --version`
-   csh: `dpkg -s csh | grep Version | cut -d ' ' -f 2`
    -   <https://stackoverflow.com/questions/14259723/how-can-i-determine-my-csh-version>
-   dash: `dpkg -s dash | grep Version | cut -d ' ' -f 2`
    -   <https://askubuntu.com/questions/283134/how-to-find-the-version-of-the-dash-shell-on-ubuntu-bin>
-   fish: `fish --version`
-   ksh: `ksh --version`
-   lshell: `lshell --version`
-   lush: `dpkg -s lush | grep Version | cut -d ' ' -f 2`
-   mksh: `mksh -c 'echo \$KSH\_VERSION'`
-   posh: `posh -c 'echo \$POSH\_VERSION'`
-   rc: `rc -c 'echo \$version'`
-   sash: `dpkg -s sash | grep Version: | cut -d ' ' -f 2`
-   tcsh: `tcsh --version`
-   yash: `yash --version`
-   zsh: `zsh --version`

"bsh", "bash", "csh", "dash", "fish", "ksh", "mksh", "posh", "tcsh", "zsh",
