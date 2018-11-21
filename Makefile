all: build

build:
	docker build . -t k8suser

test: build
	docker run -i --entrypoint="python3" --rm -v $(realpath .):/code k8suser -m unittest discover
