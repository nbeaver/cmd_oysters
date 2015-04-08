.. -*- coding: utf-8 -*-

==========================================
Shell command repository and metadatabase.
==========================================

----------
Quickstart
----------

.. Required packages: python
.. Recommended packages: tree (for pseudoschema), yajl (for verification)

----------
Motivation
----------

.. Ever tried to debug your laptop without an internet connection and not had the commands?

.. Ever stored a useful command for later in a text file and been unable to find it later?

.. Restarting daemons, changing permissions, shell incompatibility.

.. Security of shell commands, looking online ones.

.. Composite commands versus component commands.

.. Order of arguments.

--------
Examples
--------

------------
Design goals
------------

.. Mergeability (use hashes of descriptions and commands, not arbitrary primary keys).

.. One-liners vs longer scripts.

.. Extensibility of JSON fields without breaking.

.. Why different invocations? Same component commands, different forms.

.. Requirements: if the command fails, why? Is it an installation problem? Is the command not in my $PATH? Is it a permissions problem? Is it a network problem?

----------------------------------
Process for adding to the database
----------------------------------

-------------------
Future improvements
-------------------

.. Make it spit out the required packages for a given command, depending on OS.

.. Semantics of command requirements: is it only as the command is used in the invocation, or anytime the command is used?

.. The "always, sometimes, never" is a useful distinction, but what about "depends on flags" or "dependson on arguments" or "depends on configuration" or "depends on shell"?
