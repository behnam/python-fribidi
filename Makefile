
all: ctags test

test:
	python tests/test1.py
	python tests/test2.py

ctags:
	@clear
	@echo `pkg-config --libs-only-L fribidi | sed s'/^-L//'`
	@ctags -R . `pkg-config --libs-only-L fribidi | sed s'/^-L//'`

clean:
	find *.pyc | xargs rm -f

