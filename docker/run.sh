#!/bin/bash

docker run -it \
    --net=host \
    -v $(pwd):/home/$USER \
    epi_corrections_docker
