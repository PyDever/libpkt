.PHONY: help build

.DEFAULT: help
help:
	@echo "make build"
	@echo "     build and install source."
	@echo "make help"
	@echo "		show this page."

build:
	sudo python setup.py build install


