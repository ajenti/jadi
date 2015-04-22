all:
	./setup.py sdist
	
test:
	nosetests --with-coverage --cover-package=jadi --cover-html 