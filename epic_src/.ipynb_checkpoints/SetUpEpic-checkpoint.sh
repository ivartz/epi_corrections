#!/bin/sh
# Copyright (C) 2012 UC San Diego. All rights reserved.
#
# The information and source code contained herein is the exclusive property
# of UC San Diego and may not be disclosed, examined, or reproduced in
# whole or in part without explicit written authorization from the Company.
#
# Invoke this script with the 'source' command. For example:
#
#    source <my_install_location>/SetUpEpic.sh

# This command is only required for compilation and must be run one time
# before compilation. It is part of the compilation steps in README.md
source /opt/intel/parallel_studio_xe_2019/psxevars.sh

# These commands enable the compiled program to load
# ctxsrc shared objects at run-time through adding the 
# directory paths of the shared objects to LD_LIBRARY_PATH
EPIC_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export EPIC_HOME

if [ -z "${LD_LIBRARY_PATH}" ]
   then
      LD_LIBRARY_PATH="${EPIC_HOME}/ctxsrc/BasicStructs";
   else
      LD_LIBRARY_PATH="${EPIC_HOME}/ctxsrc/BasicStructs:${LD_LIBRARY_PATH}";
fi

LD_LIBRARY_PATH="${EPIC_HOME}/ctxsrc/Interpolation:${LD_LIBRARY_PATH}";

# Finally, update the LD_LIBRARY_PATH environmental variable.
export LD_LIBRARY_PATH
