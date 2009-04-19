
.PHONY: clean tests

all: ctags tests

tests:
	@echo `pkg-config --libs-only-L fribidi | sed s'/^-L//'`
	python test/test1.py
	python test/test2.py

ctags:
	@clear
	@ctags -R . `pkg-config --libs-only-L fribidi | sed s'/^-L//'`


clean:
	find *.pyc | xargs rm -f

