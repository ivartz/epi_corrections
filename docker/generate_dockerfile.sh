#!/bin/bash

# Inspired from:
# https://github.com/kaczmarj/neurodocker/blob/master/examples/conda_python/generate.sh
# https://miykael.github.io/nipype_tutorial/notebooks/introduction_neurodocker.html

# A FreeSurfer license.txt needs to exist in freesurfer/

# The two run commands are used instead of only --user $USER
# in order to create a non-root user with equal 
# user name, user id and group id as the host system.
# --user $USER creates equal user and user id,
# but NOT equal group id, which leads to different file
# permission attributes between files written in
# the host and docker environment, which leads to
# jupyter lab / notebook saving problems on mounted volumes.

docker run kaczmarj/neurodocker:0.5.0 generate docker \
    --base=neurodebian:stretch-non-free \
    --pkg-manager=apt \
    --install htop vim tmux rsync nload \
    --freesurfer version=6.0.0-min \
    --copy freesurfer/license.txt /opt/freesurfer-6.0.0-min/license.txt \
    --fsl version=5.0.11 \
    --matlabmcr version=2018a \
    --run "groupadd $(id -g $USER)" \
    --run "test "'"$(getent passwd '$USER')"'" || useradd -u $(id -u $USER) -g $(id -g $USER) --create-home --shell /bin/bash $USER" \
    --user $USER \
    --miniconda \
        create_env="epi_corrections" \
        activate=true \
        conda_install="python=3.6 jupyter jupyterlab jupyter_contrib_nbextensions nipy nipype scipy=1.2.0" \
    --run 'mkdir -p ~/.jupyter && echo c.NotebookApp.ip = \"0.0.0.0\" > ~/.jupyter/jupyter_notebook_config.py' \
    --workdir /home/$USER \
    --cmd jupyter-lab > Dockerfile
