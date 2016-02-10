default : cmd_oysters cmd_oyster_testing cmd_oyster_templates find_command_tests readme.html TODO.html
all_json: cmd_oyster_templates cmd_oyster_testing cmd_oysters
.PHONY : default all_json cmd_oyster_templates cmd_oysters test_find_command

find_command_tests : find-command.py cmdoysters/
	python2 find-command.py --substring 'ping -i' > /dev/null
	python2 find-command.py --commands ping espeak sed > /dev/null
	python2 find-command.py --tokens '|' sed localhost ping > /dev/null
	python2 find-command.py --description 'audible voice' > /dev/null
	python2 find-command.py --substring 'ping -i' --commands ping espeak sed --tokens '|' sed localhost ping --description 'audible voice' > /dev/null
	python2 find-command.py --description-tokens ping generates seconds > /dev/null

cmd_oysters : validate-database.py cmdoysters/ schemas/full-schema.json
	python2 validate-database.py --fix-all --input cmdoysters/

cmd_oyster_testing : validate-database.py cmdoysters/ schemas/full-schema.json
	python2 validate-database.py --fix-all --input testing/

cmd_oyster_templates : validate-database.py cmdoysters/ schemas/full-schema.json
	python2 validate-database.py --input templates/

readme.html : readme.rst
	rst2html readme.rst readme.html

TODO.html : TODO.rst
	rst2html TODO.rst TODO.html

clean :
	rm --force --verbose readme.html
	rm --force --verbose TODO.html
