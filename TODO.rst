Tailor invocation according to host OS,
or at least add a shell options or config file for preferred shell.

Add information about how to exit an interactive command, e.g.:

- root -l:  Ctrl-D and Ctrl-C don't work, must use exit().
- cat: Ctrl-C, Ctrl-D, Ctrl-\
- ssh: Have to use <Enter>~. when a connection hangs.

How to include version numbers in "commands this shell works with/doesn't work with"?

Verify that all the pseudo-schema fields are in command-template.json.

Verify temp.json when make is run.

Sometimes changeable arguments are repeated -- should slice be a list of slices?

Omit requirements for shell keywords, since they don't do anything on their own? Or use null?

Required packages for shell keywords and builtins -- just omit them, since it depends on the shell anyway?

Requirements are vague, e.g. using `ls` in an sshfs does require an internet connection, but only indirectly.
