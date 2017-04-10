init:
	setup/init.sh 

test:
	nosetests -v

style:
	pep8 ./ifc

.PHONY: init test
