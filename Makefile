all: validate_json test_python_script lint_database
.PHONY : validate_json test_python_script lint_database

validate_json : command-database.json Makefile
	json_verify < command-database.json

test_python_script : find-command.py Makefile
	python find-command.py "ping"

lint_database : command-database.json lint-database.py Makefile
	python lint-database.py
