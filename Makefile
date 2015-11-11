TARGS := $(shell sed -n 's/^\([-a-z]\+\):.*/\1/p' Makefile|sort -u|xargs)
.PHONY: $(TARGS)

all: test build install

build:
	./forestanza.py

install:
	[[ ! -d /mnt/0/Books ]] || sudo cp -vrfT ~/.cache/forestanza /mnt/0/Books/forestanza

test: test-exec
test-exec: export PYTHONPATH += .
test-exec:
	py.test -- $(shell pwd)
