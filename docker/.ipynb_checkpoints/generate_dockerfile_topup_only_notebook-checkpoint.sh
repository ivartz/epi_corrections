#!/bin/bash

# Inspired from:
# https://github.com/kaczmarj/neurodocker/blob/master/ex /tmp/icc-config.cfgenerate.sh
# https://miykael.github.io/nipype_tutorial/notebooks/introduction_neurodocker.html

# The docker container is supposed to run as non-root with
# user name, user id and group id as in the host system.
# --user $USER creates equal user and user id,
# but NOT equal group id, which leads to different file
# permission attributes between files written in
# the host and docker environment, which leads to
# jupyter lab / notebook saving problems on mounted volumes.
# For this reason, the --run "groupadd ... command is necessary.

docker run kaczmarj/neurodocker:0.5.0 generate docker \
    --base=ubuntu:16.04 \
    --pkg-manager=apt \
    --fsl version=5.0.11 \
    --install less htop vim tmux rsync nload uuid-runtime \
    --run "groupadd -g $(id -g $USER) $(id -g $USER) && useradd -u $(id -u $USER) -g $(id -g $USER) --create-home --shell /bin/bash $USER" \
    --user $USER \
    --miniconda \
        create_env="epi_corrections" \
        activate=true \
        conda_install="python=3.6 jupyter jupyterlab jupyter_contrib_nbextensions nipy nipype scipy=1.2.0" \
    --run 'mkdir -p ~/.jupyter && echo c.NotebookApp.ip = \"0.0.0.0\" > ~/.jupyter/jupyter_notebook_config.py' \
    --workdir /home/$USER \
    --cmd jupyter-lab > Dockerfile
