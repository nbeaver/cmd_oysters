Tailor invocation according to host OS,
or at least add a shell options or config file for preferred shell.

Add information about how to exit an interactive command, e.g.:

- root -l:  Ctrl-D and Ctrl-C don't work, must use exit().
- cat: Ctrl-C, Ctrl-D, Ctrl-\
- ssh: Have to use <Enter>~. when a connection hangs.
- pacmd: Don't use exit, use Ctrl-D, or you'll kill the daemon.
- ed: use q, not anything else.

How to include version numbers in "commands this shell works with/doesn't work with"?

How to extend this to work for other programming languages.

Verify that all the pseudo-schema fields are in command-template.json.

Verify temp.json when make is run.

Sometimes changeable arguments are repeated -- should slice be a list of slices?

Omit requirements for shell keywords, since they don't do anything on their own? Or use null?

Required packages for shell keywords and builtins -- just omit them, since it depends on the shell anyway?

Requirements are vague, e.g. using ``ls`` in an sshfs does require an internet connection, but only indirectly.

Should the requirements refer to the command as used, or to any potential use of the command?

Decide which fields are required and which are optional (JSON schema?).

Decide if all command information should be at the same nesting level or not.

Add to find-command.py: Add a --shell -x flag to spawn a prompt for the user with the command already filled in (use pexpect).

Re-order command info so there is a platform-independent, then ones for Debian, etc.

How to express the various options for debian packages, e.g. various shells or awks.

Nilsimsa is not good for short strings. Better locality-sensitive hash for short strings?
