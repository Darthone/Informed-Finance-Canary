init:
	virtualenv venv
	source ./venv/bin/activate
	pip install -r requirements.txt

test:
	source ./venv/bin/activate
	nosetests -v

.PHONY: init test
