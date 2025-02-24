include .env
export

tag ?= alpha
image = rxinui/yodelr
psize ?= 10000
build:
	podman build -t $(image):$(tag) .

unittest-in-container: clean
	podman run --rm $(image):$(tag) -m pytest --color=yes

perftest-in-container: clean
	podman run --rm --env PERF_GENERATOR_SIZE=$(psize) $(image):$(tag) -m pytest --color=yes --log-cli-level=WARNING tests/*_perf*.py

clean:
	podman rm -f $(image):$(tag)
	
localtest:
	clear && pytest

ltest: localtest

perftest:
	clear && PERF_GENERATOR_SIZE=$(psize) pytest --log-cli-level=WARNING tests/*_perf*.py

ptest: perftest
