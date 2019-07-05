#!/bin/bash

# Inspired from:
# https://github.com/kaczmarj/neurodocker/blob/master/ex /tmp/icc-config.cfgenerate.sh
# https://miykael.github.io/nipype_tutorial/notebooks/introduction_neurodocker.html

# The two run commands are used instead of only --user $USER
# in order to create a non-root user with equal 
# user name, user id and group id as the host system.
# --user $USER creates equal user and user id,
# but NOT equal group id, which leads to different file
# permission attributes between files written in
# the host and docker environment, which leads to
# jupyter lab / notebook saving problems on mounted volumes.

docker run kaczmarj/neurodocker:0.5.0 generate docker \
    --base=ubuntu:16.04 \
    --pkg-manager=apt \
    --install bzip2 ca-certificates curl git cpio build-essential wget libfftw3-dev procps apt-utils \
    --freesurfer version=6.0.0-min \
    --copy conf/freesurfer/license.txt /opt/freesurfer-6.0.0-min/license.txt \
    --fsl version=5.0.11 \
    --spm12 version=r7219 \
    --copy conf/intel/config.cfg /tmp/icc-config.cfg \
    --copy conf/intel/license.lic /tmp/icc-license.lic \
    --run 'cd /tmp && \
    wget -O icc.tgz http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14850/parallel_studio_xe_2019_update1_cluster_edition_online.tgz && \
    tar -xvzf icc.tgz && \
    cd /tmp/parallel_studio_xe_* && \
    bash ./install.sh --silent=/tmp/icc-config.cfg && \
    cd /tmp && \
    rm -rf parallel_studio_xe_* icc.tgz && \
    rm /tmp/icc-config.cfg' \
    --install less htop vim tmux rsync nload uuid-runtime \
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
