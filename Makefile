all : command_database check_json docs
.PHONY : command_database check_json docs
docs: README.html TODO.html

command_database : find-command.py CmdOysters/
	python find-command.py --substring 'ping -i' > /dev/null
	python find-command.py --commands ping espeak sed > /dev/null
	python find-command.py --tokens '|' sed localhost ping > /dev/null
	python find-command.py --description 'audible voice' > /dev/null
	python find-command.py --substring 'ping -i' --commands ping espeak sed --tokens '|' sed localhost ping --description 'audible voice' > /dev/null
	python find-command.py --description-tokens ping generates seconds > /dev/null

check_json : validate-database.py CmdOysters/ templates/ schemas/full-schema.json
	python validate-database.py CmdOysters/
	python validate-database.py templates/

README.html : README.rst
	rst2html README.rst README.html

TODO.html : TODO.rst
	rst2html TODO.rst TODO.html

clean :
	rm --force --verbose README.html
	rm --force --verbose TODO.html
