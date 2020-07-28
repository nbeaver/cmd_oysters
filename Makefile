.PHONY : default
default : readme.html todo.html

.PHONY : validate
validate: test_search cmd_oyster_templates cmd_oyster_testing cmd_oysters

.PHONY : test_search
test_search : cmdoysters.py
	python3 cmdoysters.py --substring 'ping -i' > /dev/null
	python3 cmdoysters.py --commands ping espeak sed > /dev/null
	python3 cmdoysters.py --tokens '|' sed localhost ping > /dev/null
	python3 cmdoysters.py --description 'audible voice' > /dev/null
	python3 cmdoysters.py --substring 'ping -i' --commands ping espeak sed --tokens '|' sed localhost ping --description 'audible voice' > /dev/null
	python3 cmdoysters.py --description-tokens ping generates seconds > /dev/null

.PHONY: unittest
unittest:
	./test_script.py

.PHONY : cmd_oysters
cmd_oysters : validate_database.py cmdoysters/* schemas/full-schema.json
	python3 validate_database.py --input cmdoysters/

.PHONY : cmd_oyster_testing
cmd_oyster_testing : validate_database.py cmdoysters/* schemas/full-schema.json
	python3 validate_database.py --input testing/

.PHONY : cmd_oyster_templates
cmd_oyster_templates : validate_database.py cmdoysters/* schemas/full-schema.json
	python3 validate_database.py --input templates/

readme.html : readme.rst
	rst2html readme.rst readme.html

todo.html : todo.md
	markdown todo.md > todo.html

.PHONY: new_cmd_oyster
new_cmd_oyster:
	./new_oyster.py cmdoysters/ my-command

format_py:
	yapf3 --in-place *.py

.PHONY : clean
clean :
	rm --force --verbose readme.html
	rm --force --verbose todo.html
