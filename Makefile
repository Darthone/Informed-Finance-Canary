WORKDIR="./work/"
ROOT=`pwd`

init:
	mkdir -p $(WORKDIR)
	pip install -r ./requirements.txt
	python $(ROOT)/src/ifc/db.py

test:
	cd $(ROOT)/src/ifc/ && nosetests -v

style:
	pep8 ./src/ifc

build:
	cd ./web/frontend/ && grunt build

docs:
	cd ./docs/ && make gen html

clean:
	rm -rf $(WORKDIR)

run:
	#todo
	#launch loader
	#launch gather
	#launch web server

.PHONY: init test style build docs clean run

