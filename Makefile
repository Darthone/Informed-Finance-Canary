init:
	setup/init.sh 

test:
	nosetests -v

.PHONY: init test
