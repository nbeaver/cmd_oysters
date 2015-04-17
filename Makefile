all : command_database minimal_template full_command_template temp sorted.json pseudo_schema_tree README.html pseudo-schema-notes.html TODO.html
.PHONY : command_database minimal_template full_command_template temp pseudo_schema_tree

command_database : command-database.json check-pseudoschema.py validate-database.py find-command.py
	json_verify < command-database.json
	python check-pseudoschema.py command-database.json
	python validate-database.py command-database.json
	python find-command.py --substring 'ping -i' > /dev/null
	python find-command.py --commands ping espeak sed > /dev/null
	python find-command.py --tokens '|' sed localhost ping > /dev/null
	python find-command.py --description 'audible voice' > /dev/null
	python find-command.py --substring 'ping -i' --commands ping espeak sed --tokens '|' sed localhost ping --description 'audible voice' > /dev/null
	python find-command.py --description-tokens ping generates seconds > /dev/null

sorted.json : sort-json.py command-database.json
	python sort-json.py
	diff --ignore-all-space --ignore-blank-lines command-database.json sorted.json

# The target really should be pseudo-schema-tree.txt,
# but the timestamp of the directory doesn't change when the files inside are,
# so we need to make it a phony target so that it gets called every time.
pseudo_schema_tree : pseudo-schema
	tree --noreport pseudo-schema/ > pseudo-schema-tree.txt

minimal_template : minimal-template.json pseudo-schema/ check-pseudoschema.py
	json_verify < minimal-template.json
	python check-pseudoschema.py minimal-template.json
	#python validate-database.py minimal-template.json

full_command_template : full-command-template.json pseudo-schema/ check-full-template.py check-pseudoschema.py
	json_verify < full-command-template.json
	python check-pseudoschema.py full-command-template.json
	#python validate-database.py full-command-template.json
	python check-full-template.py full-command-template.json pseudo-schema/

temp : validate-database.py check-pseudoschema.py
	json_verify < temp.json
	#python validate-database.py temp.json
	python check-pseudoschema.py temp.json

README.html : README.rst
	rst2html README.rst README.html

TODO.html : TODO.rst
	rst2html TODO.rst TODO.html

pseudo-schema-notes.html : pseudo-schema-notes.markdown
	markdown pseudo-schema-notes.markdown > pseudo-schema-notes.html

clean :
	rm --force --verbose pseudo-schema-tree.txt
	rm --force --verbose sorted.json
	rm --force --verbose README.html
	rm --force --verbose TODO.html
	rm --force --verbose pseudo-schema-notes.html
