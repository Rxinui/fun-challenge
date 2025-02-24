include .env
export

tag ?= alpha
image = rxinui/yodelr
psize ?= 10000
build:
	podman build -t $(image):$(tag) .

test: clean build
	podman run --rm $(image):$(tag) -m pytest --color=yes

clean:
	podman rm -f $(image):$(tag)
	
localtest:
	clear && pytest

ltest: localtest

ptest:
	clear && PERF_GENERATOR_SIZE=$(psize) pytest --log-cli-level=WARNING tests/test_yodelr_perf.py