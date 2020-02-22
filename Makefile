.PHONY : default
default : readme.html todo.html

.PHONY : validate
validate: test_search cmd_oyster_templates cmd_oyster_testing cmd_oysters

.PHONY : test_search
test_search : cmdoysters.py
	python cmdoysters.py --substring 'ping -i' > /dev/null
	python cmdoysters.py --commands ping espeak sed > /dev/null
	python cmdoysters.py --tokens '|' sed localhost ping > /dev/null
	python cmdoysters.py --description 'audible voice' > /dev/null
	python cmdoysters.py --substring 'ping -i' --commands ping espeak sed --tokens '|' sed localhost ping --description 'audible voice' > /dev/null
	python cmdoysters.py --description-tokens ping generates seconds > /dev/null

.PHONY : cmd_oysters
cmd_oysters : validate_database.py cmdoysters/* schemas/full-schema.json
	python2 validate_database.py --input cmdoysters/

.PHONY : cmd_oyster_testing
cmd_oyster_testing : validate_database.py cmdoysters/* schemas/full-schema.json
	python2 validate_database.py --input testing/

.PHONY : cmd_oyster_templates
cmd_oyster_templates : validate_database.py cmdoysters/* schemas/full-schema.json
	python2 validate_database.py --input templates/

readme.html : readme.rst
	rst2html readme.rst readme.html

todo.html : todo.md
	markdown todo.md > todo.html

.PHONY : clean
clean :
	rm --force --verbose readme.html
	rm --force --verbose todo.html
