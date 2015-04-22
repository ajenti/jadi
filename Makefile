all:
	./setup.py sdist
	
upload:
	./setup.py sdist upload --sign --identity "Ajenti Packagers"
	
test:
	nosetests --with-coverage --cover-package=jadi --cover-html 