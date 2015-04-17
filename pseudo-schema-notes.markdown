<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
These are some notes on the structure of the command database.

`pseudo-schema/`  
├── `can-modify`  
│   ├── `filesystem`: Could the command modify the filesystem? Examples: `rm`, `mv`.  
│   └── `other-processes`: Could the command modify other processes? Examples: `kill`, `disown`.  
├── `component-command-info`: Additional metadata for the component commands.  
│   └── `$COMMAND`  
│       ├── `bash-type`: The output of `type -t $COMMAND` in bash; one of `alias`, `keyword`, `function`, `builtin`, or `file`. May be different in other shells, e.g. which is a `builtin` in zsh but a `file` in bash.  
│       ├── `debian`: Information specific to the Debian Linux distribution.  
│       │   ├── `executable-path`: The full path to the binary. Often in e.g. `/bin/` or `/usr/bin/`.  
│       │   └── `required-packages`: the Debian package(s) required to install the relevant command.  
│       └── `requirements-in-general`: Requirements for a command in all possible uses. Useful for figuring out why a command doesn't work as expected.  
│           ├── `authentication`: Will the command require the user to enter their password? Examples: `chsh`, `passwd`.  
│           ├── `internet-connection`: Does the command require an active internet connection? Examples: `wget`, `whois`, `dig`.  
│           └── `sudo`: Does the command require superuser priveleges? Examples: `shutdown`, `rtcwake`.  
├── `component-commands`: List of the individual commands that make up the composite command. Required field.  
├── `description`: Textual description of what the command does. Must be unique, since its SHA1 hash is effectively the primary key. Required field.  
│   ├── `nilsimsa-hex`: A locality-sensitive hash, helping to detect similar descriptions.  
│   ├── `sha1hex`: The SHA1 cryptographic hash of the description string; useful instead of a primary key for linking to related commands. Required field.  
│   └── `string`: The actual text of the description. Don't add hard linebreaks; let the output formatter decide how to do that. Required field.  
├── `invocations`: The actual command that gets run, indexed by shell. All invocations must have the same component commands. Required field.  
│   └── `$INVOCATION`: Name of the shell (e.g. bash) or class of shells (e.g. POSIX) that the command works in. Required field.  
│       ├── `changeable-arguments`: Adjustable parameters of the command or commands; may be nested.  
│       │   └── `$ARG`: The actual text of the argument; a subset of $SHELL/string.  
│       │       ├── `component-command`: The argument is passed to this command.  
│       │       ├── `component-command-flag`: The argument is passed via this flag; may be null.  
│       │       ├── `description-string`: Description of the argument.  
│       │       ├── `invocation-slice`: Position of the argument in $SHELL/string that can be accessed by slice notation.  
│       │       ├── `subtype`: More refined type, e.g. type is string, subtype is absolute path.  
│       │       └── `type`: The base type of the argument e.g. integer, float, string, boolean. Useful since e.g. JSON does not distinguish floats and integers.  
│       ├── `command-requirements-as-invoked`: Requirements for a command as its used in the invocation.  
│       │   └── `$COMMAND`  
│       │       ├── `authentication`: See above.  
│       │       ├── `internet-connection`: See above.  
│       │       └── `sudo`: See above.  
│       ├── `compatible-shells`: List of shells that the command will run correctly on.  
│       ├── `example-outputs`: If the output is short and provides insight into what the command does, it is useful to know.  
│       ├── `incompatible-shells`: Disjoint set of compatible-shells. Options are not explicitly enumerated because there are many, many shells.  
│       ├── `nilsimsa-hex`: A locality-sensitive hash, helping to detect similar commands.  
│       ├── `related-invocations`: SHA1 hashes of invocations for different commands that are related to this invocation. A kind of hyper-linking.  
│       ├── `sha1hex`: The SHA1 cryptographic hash of the command string; useful for linking to related commands. Required field.  
│       └── `string`: Actual string that could be passed to the shell and executed. Required field.  
├── `related-commands`: SHA1 hashes of the descriptions of other commands that are related to this one, e.g. a command that accomplishes the same thing with different component commands.  
└── `relevant-urls`: A list of URLs that discuss the command or an equivalent command with the same component commands.  

</html>
