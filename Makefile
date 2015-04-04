all: validate_json test_python_script lint_database pseudo_schema sort_database
.PHONY : validate_json test_python_script lint_database pseudo_schema sort_database

validate_json : command-database.json Makefile
	json_verify < command-database.json

test_python_script : find-command.py Makefile
	python find-command.py "ping"

lint_database : command-database.json lint-database.py Makefile
	python lint-database.py command-database.json

sort_database : command-database.json sort-json.py Makefile
	python sort-json.py

pseudo_schema : pseudo-schema check-pseudoschema.py Makefile
	tree --noreport pseudo-schema/ > pseudo-schema-tree.txt
	python check-pseudoschema.py command-database.json
