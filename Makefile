all: validate_json test_python_script lint_database pseudo_schema
.PHONY : validate_json test_python_script lint_database pseudo_schema

validate_json : command-database.json Makefile
	json_verify < command-database.json

test_python_script : find-command.py Makefile
	python find-command.py "ping"

lint_database : command-database.json lint-database.py Makefile
	#python lint-database.py

pseudo_schema : pseudo-schema Makefile
	tree --noreport pseudo-schema/ > pseudo-schema-tree.txt
