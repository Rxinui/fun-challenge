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

unittest-in-container: clean build
	$(BUILDER) run --rm --pull=never docker.io/$(image):$(tag) -m pytest --color=yes tests/test_yodelr_api.py

perftest-in-container: clean build
	$(BUILDER) run --rm --pull=never -e PERF_GENERATOR_SIZE=$(psize) $(image):$(tag) -m pytest --color=yes --log-cli-level=WARNING tests/*_perf*.py

clean:
	$(BUILDER) rm -f $(image):$(tag)
	
localtest:
	clear && pytest --color=yes tests/test_yodelr_api.py

ltest: localtest

perftest:
	clear && PERF_GENERATOR_SIZE=$(psize) pytest --log-cli-level=WARNING tests/*_perf*.py

ptest: perftest
