
.PHONY: clean tests

all: ctags tests

tests:
	@pkg-config --libs-only-L fribidi
	@echo
	python test/test1.py
	@#python test/test2.py

ctags:
	@clear
	@ctags -R . `pkg-config --libs-only-L fribidi | sed s'/^-L//'`


clean:
	find *.pyc | xargs rm -f

