include .env
export

tag ?= alpha
image = rxinui/yodelr
build:
	podman build -t $(image):$(tag) .

test: clean build
	podman run --rm $(image):$(tag) -m pytest --color=yes

clean:
	podman rm -f $(image):$(tag)
	
localtest:
	pytest -s 
