all : command_database check_json pseudo_schema_tree full_command_template docs
.PHONY : command_database check_json minimal_template full_command_template temp pseudo_schema_tree docs
docs: README.html pseudo-schema-notes.html TODO.html

command_database : find-command.py CmdOysters/
	python find-command.py --substring 'ping -i' > /dev/null
	python find-command.py --commands ping espeak sed > /dev/null
	python find-command.py --tokens '|' sed localhost ping > /dev/null
	python find-command.py --description 'audible voice' > /dev/null
	python find-command.py --substring 'ping -i' --commands ping espeak sed --tokens '|' sed localhost ping --description 'audible voice' > /dev/null
	python find-command.py --description-tokens ping generates seconds > /dev/null

check_json : validate-database.py CmdOysters/ CmdOyster-templates/
	python validate-database.py CmdOysters/
	python validate-database.py CmdOyster-templates/

full_command_template : CmdOyster-templates/full-command-template.json check-full-template.py
	python check-full-template.py CmdOyster-templates/full-command-template.json pseudo-schema/

# The target really should be pseudo-schema-tree.txt,
# but the timestamp of the directory doesn't change when the files inside are,
# so we need to make it a phony target so that it gets called every time.
pseudo_schema_tree : pseudo-schema
	tree --noreport pseudo-schema/ > pseudo-schema-tree.txt

README.html : README.rst
	rst2html README.rst README.html

TODO.html : TODO.rst
	rst2html TODO.rst TODO.html

pseudo-schema-notes.html : pseudo-schema-notes.markdown
	markdown pseudo-schema-notes.markdown > pseudo-schema-notes.html

clean :
	rm --force --verbose pseudo-schema-tree.txt
	rm --force --verbose README.html
	rm --force --verbose TODO.html
	rm --force --verbose pseudo-schema-notes.html
