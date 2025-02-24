include .env 
export

tag ?= alpha
image = rxinui/yodelr
psize ?= 10000

ifeq ($(APP_ENV), local)
    BUILDER=podman
else
    BUILDER=docker
endif

build:
	$(BUILDER) build -t docker.io/$(image):$(tag) .

unittest-in-container: clean
	$(BUILDER) run --rm docker.io/$(image):$(tag) -m pytest --color=yes tests/test_yodelr_api.py

perftest-in-container: clean
	$(BUILDER) run --rm --env PERF_GENERATOR_SIZE=$(psize) $(image):$(tag) -m pytest --color=yes --log-cli-level=WARNING tests/*_perf*.py

clean:
	$(BUILDER) rm -f $(image):$(tag)
	
localtest:
	clear && pytest

ltest: localtest

perftest:
	clear && PERF_GENERATOR_SIZE=$(psize) pytest --log-cli-level=WARNING tests/*_perf*.py

ptest: perftest
