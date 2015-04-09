all: command_database simple_template full_command_template temp sorted.json pseudo_schema_tree
.PHONY : command_database simple_template full_command temp pseudo_schema_tree

command_database : command-database.json check-pseudoschema.py validate-database.py find-command.py
	json_verify < command-database.json
	python check-pseudoschema.py command-database.json
	python validate-database.py command-database.json
	python find-command.py --substring 'ping -i' > /dev/null
	python find-command.py --commands ping espeak sed > /dev/null
	python find-command.py --tokens '|' sed localhost ping > /dev/null
	python find-command.py --description 'audible voice' > /dev/null
	python find-command.py --substring 'ping -i' --commands ping espeak sed --tokens '|' sed localhost ping --description 'audible voice' > /dev/null

sorted.json : sort-json.py command-database.json
	python sort-json.py
	diff --ignore-all-space --ignore-blank-lines command-database.json sorted.json

pseudo_schema_tree: pseudo-schema
	tree --noreport pseudo-schema/ > pseudo-schema-tree.txt

simple_template : simple-template.json pseudo-schema/ check-full-template.py check-pseudoschema.py
	json_verify < simple-template.json
	python check-pseudoschema.py simple-template.json
	python check-full-template.py full-command-template.json pseudo-schema/

full_command_template : full-command-template.json pseudo-schema/ check-full-template.py check-pseudoschema.py
	json_verify < full-command-template.json
	python check-pseudoschema.py full-command-template.json
	python validate-database.py full-command-template.json
	python check-full-template.py full-command-template.json pseudo-schema/

temp : validate-database.py check-pseudoschema.py
	json_verify < temp.json
	python validate-database.py temp.json
	python check-pseudoschema.py temp.json
