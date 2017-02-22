init:
	setup/init.sh 

test:
	source ./venv/bin/activate
	nosetests -v

.PHONY: init test
