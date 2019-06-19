#!/bin/bash
# https://gist.github.com/bastman/5b57ddb3c11942094f8d0a97d461b430

docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

