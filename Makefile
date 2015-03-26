all: validate_json
.PHONY : validate_json

validate_json : command-database.json Makefile
	json_verify < command-database.json
