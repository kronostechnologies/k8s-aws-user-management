#!/bin/bash

docker run -it --rm -e AWS_PROFILE -v $(pwd):/code -v $HOME/.aws:/root/.aws awscli python3 main.py "$@"
