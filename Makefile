.PHONY : default all_json cmd_oyster_templates cmd_oysters test_searchoysters
default : readme.html todo.html
validate: test_searchoysters cmd_oyster_templates cmd_oyster_testing cmd_oysters

test_searchoysters : searchoysters.py
	python searchoysters.py --substring 'ping -i' > /dev/null
	python searchoysters.py --commands ping espeak sed > /dev/null
	python searchoysters.py --tokens '|' sed localhost ping > /dev/null
	python searchoysters.py --description 'audible voice' > /dev/null
	python searchoysters.py --substring 'ping -i' --commands ping espeak sed --tokens '|' sed localhost ping --description 'audible voice' > /dev/null
	python searchoysters.py --description-tokens ping generates seconds > /dev/null

cmd_oysters : validate-database.py cmdoysters/* schemas/full-schema.json
	python2 validate_database.py --input cmdoysters/

cmd_oyster_testing : validate-database.py cmdoysters/* schemas/full-schema.json
	python2 validate_database.py --input testing/

cmd_oyster_templates : validate-database.py cmdoysters/* schemas/full-schema.json
	python2 validate_database.py --input templates/

readme.html : readme.rst
	rst2html readme.rst readme.html

todo.html : todo.md
	markdown todo.md > todo.html

clean :
	rm --force --verbose readme.html
	rm --force --verbose todo.html
