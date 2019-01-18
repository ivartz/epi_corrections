## EPIC

The reference of EPIC is
Efficient correction of inhomogeneous static magnetic field-induced
distortion in Echo Planar Imaging.
Holland D, Kuperman JM, Dale AM.
Neuroimage. 2010 Mar;50(1):175-83.

https://doi.org/10.1016/j.neuroimage.2009.11.044
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2819607/
https://www.sciencedirect.com/science/article/pii/S1053811909012294

Original source code from https://github.com/dominicholland/EPIC
(f6bfa4abd19c95deb9e28a63c16515075847c1fa) 
modified to compile with following dependencies:

## Dependencies

- Ubuntu 16.04 LTS
- l_mkl_2019.1.144 Intel Math Kernel Library (sudo ./install_GUI.sh)
- ifort Intel Fortran Compiler provided with Intel Parallel Studio XE Cluster Edition for Linux, version 2019 Update 1 Eng/Jpn (sudo ./install_GUI.sh)
- icc Intel C Compiler provided with Intel Parallel Studio XE Cluster Edition for Linux, version 2019 Update 1 Eng/Jpn (sudo ./install_GUI.sh)
- icpc Intel C++ Compiler provided with Intel Parallel Studio XE Cluster Edition for Linux, version 2019 Update 1 Eng/Jpn (sudo ./install_GUI.sh)
- (optional, for bin/Makefile) FreeSurfer in order to run mri_convert

## How does the correction look like?
Have a look at the included uncorrected and corrected example in bin/testenv/img-mgz and bin/testenv/out respectively with an .mgz image viewer (such as freeview or fsleyes)

## Modifications from original code

- Added the precompiled executable 'applyEpic' in folder bin/. The code to compile seems to only compile the main 'epic' program that computes the deformation field (that 'applyEpic' uses). Taken from an older EPIC code repository used for research purposes at Oslo University Hospital (MMIL EPIC) (executable created Feb. 15 2016). You might have to chmod +x applyEpic for it to run.
- Modified Makefile file. The MKLLIBS static linking inside Makefile was based upon the Intel Math Kernel Library Link Line Advisor with settings as specified in the screenshot .pdf in doc/Suggested static link line from Intel Math Kernel Library Link Line Advisor.pdf . -lifcore and -lifcoremt allows icc and icpc to use some Fortran runtime libraries that were necessary in the compiled Fortran code from ifort. -lstdc++ allows Fortran code to use some c++ std stuff (I think). Unshure if this setting is necessary. Two copmiler options were prepended to INCS according to the mentioned link advisor. Lastly, added -qopenmp compiler flag. See the original Makefile in the original source code if you want to see further differences.
- Modified MakeMacros file to use ifort as Fortran and removed following non-compatilbe Fortran compiler flags. Added -qopenmp ifort Fortran compiler flag since I think this helps the Fortran code to be compabible with Intel compiled C/C++ code using corresponding -qopenmp compilation flag.
- Added BasicStructs (libcorstruct.so) and Interpolation (libcorinterp.so, libg2c.so.0) shared objects from CorTechs Labs. Taken from an older EPIC code repository used for research purposes at Oslo University Hospital (MMIL EPIC) (These files were created Feb. 15 2016).
- Added interpolation.h and basicstructs.h from CorTechs Labs. Taken from another older EPIC code repository used for research purposes at Oslo University Hospital (EPI-EPIC_OUS modified by Raimo Salo at Oslo University Hospital) (interpolation.h and basicstructs.h last modified April 8th 2011)
- Added modified SetUpEpic.sh from older EPIC code used for research purposes at Oslo University Hospital (MMIL EPIC)
- Added modified Makefile (not for EPIC compilation) in bin/ from the previously mentioned Raimo Salotal code repository (EPI-EPIC_OUS). This Makefile runs EPIC on Dynamic Susceptibility Contrast images in batch mode according the the description in this Makefile
- A few changes was done to the C++ and Fortran code in order to get it to compile on this Linux system, f. ex. using exit() after an #include <cstdlib> instead of std::exit in .cpp files. Another change was changing #include <string> to #include <string.h> in order for memset() to work. In computeDeformationField.cpp, simply printing with std::cout (line 107 and 114) seemed to force a memory allocation necessary to avoid segmentation error at run-time. Adding the two print lines lead avoided segmentation fault in computeDeformationField.cpp at run-time on this system. Windows-specific stuff such as the /* Deal with Windows*/ #ifndef DLLTYPE etc. in files such as imgvol.h were commented out, and all DLLTYPE type declarations (written before normal types) in the relevant files were removed
- Added modified second Makefile inside bin/ by Raimo Salo that runs complete EPIC DSC correction (see section "EPIC for DSC EPI susceptibility correction").

## Compilation

# Almost one-line compilation

- You will likely have to change the source command inside SetUpEpic.sh
  to your correct Intel Parallel Studio root installation directory and version.
  See SetUpEpic.sh . This is for making the icpc compiler available at the 
  command line, for instance.

- source SetUpEpic.sh && make clean && make && make copy_to_bin

# Complete step-by-step

1. Install dependencies

  Optional: Next step seems to invoke mklvars.sh and set MKLROOT correctly. Makefile uses MKLROOT as mkl installation directory, which for me was:
    /opt/intel/compilers_and_libraries_2019.1.144/linux/mkl
  sorce /opt/intel/compilers_and_libraries_2019.1.144/linux/mkl/bin/mklvars.sh
    to set MKLROOT

2. Source Intel Parallel Studio environmental variable script to make the Intel Compilers (ifort, icc, icpc) available in the bash shell (after figuring out what is the default root install for Intel Parallel Studio. NB!: If multiple parallel_studio_* folders, choose the one with the version specified at the end, like here)

  source /opt/intel/parallel_studio_xe_2019.1.053/psxevars.sh

  This command can be placed inside SetUpEpic.sh for easier use

3. make

  Will make the executable epic

  (Optional, for bin/Makefile to work) make copy_to_bin

  make copy_to_bin just copies the compled program (epic) from make to the bin/ folder in this repository. This is done so that bin/Makefile can easily call ./epic

## Test-run
- cd bin
- ./epic -f testenv/img-mgz/EPI_forward.mgz -r testenv/img-mgz/EPI_reverse.mgz -od testenv/out
- inspect files in testenv/out and compare with raw data in testenv/img-mgz

## Run

1. One-time setup. unwarpB0 will try to dynamically load the shared objects at ctxsrc at run-time. This will work if the two directories inside ctxsrc are part of the LD_LIBRARY_PATH envirommental variable. 
  SetUpEpic.sh will do this for you with the command

  source SetUpEpic.sh

2. ./epic

  Should give a list of input options

## Clean compilated files (*.o, unwarpB0 etc)
- make clean

## EPIC for DSC EPI susceptibility correction

# Run distortion correction

1. make copy_to_bin 
  if not done already
2. Follow instructions in bin/Makefile to correctly organize .nii EPI files inside bin/data
3. cd bin
4. chmod +x applyEpic
  if not done already
5. make clean
6. make correct_all

# Clean distortion corrected files 
make clean
  (inside bin/)

