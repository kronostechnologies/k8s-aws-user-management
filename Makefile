all: build

build:
	docker build . -t kronostechnologies/k8s-aws-user-management

test: build
	docker run -i --entrypoint="python3" --rm -v $(realpath .):/code kronostechnologies/k8s-aws-user-management -m unittest discover
