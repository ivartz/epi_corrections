# epi_corrections
Pipeline for correction of 
magnetic susceptibility induced (geometric and intensity) 
artefacts from off-resonance field in EPI MRI images. 
Using FSL TOPUP and EPIC.

## Update: Running on a single EPI pair

- TOPUP: Install FSL and have a look at https://github.com/ivartz/epi_corrections/blob/master/scripts/applytopup.sh and https://github.com/ivartz/epi_corrections/blob/master/scripts/computetopup.sh
- EPIC: Install the Computational Morphometry Toolkit (https://neuro.debian.net/pkgs/cmtk.html) and have a look at https://www.nitrc.org/docman/view.php/212/1187/UnwarpEchoPlanar.pdf

## Methods

See reports/PosterHovden.pdf (NFMF MedFys 2019).

The methods make use of the different distortions in 
Echo Planar Images (EPI) depending on direction of 
phase encoding in the k-space EPI encoding 
(positive/blip-up and negative blip-down phase encoding).

For a correction of a pair of EPI images (blip-up, blip-down), 
the different type of distortion based on phase encoding 
directions are used to to make an off-resonance field (FSL TOPUP)
or a displacement field (EPIC).

In each of the medhods, the field is then used to "unwrap" each EPI 
image in the pair, aiming the two to be identical.

## Folder structure

epi_corrections requires the following folder structure:

    DICOM_directory/
    epi_corrections/
    ├── docker/
    │   ├── generate_dockerfile.sh
    │   ├── build.sh
    │   ├── run.sh
    │   ├── clean.sh
    │   ├── rm-img.sh
    │   ├── rm-unused-imgs.sh
    │   ├── conf/
    .
    .
    .
    epi_corrections_out_*

where epi_corrections is the directory from
```bash
git clone https://github.com/ivartz/epi_corrections
```
and DICOM_directory is a directory containing .dcm files from various sequences, each sequence in a separate folder.
The program creates the folder epi_corrections_out_* with similar folder structure as in DICOM_folder.

## Running in Docker environment
```bash
git clone https://github.com/ivartz/epi_corrections
```
- Register at https://surfer.nmr.mgh.harvard.edu/fswiki/License to get a FreeSurfer License file. Place the license at

    epi_corrections/docker/conf/freesurfer/license.txt

- Register at Intel for receiving a Intel Parallel Studio XE 2019 Update 1 license at https://software.intel.com/en-us/parallel-studio-xe/choose-download/free-trial-cluster-linux-fortran . After creating a user and logging in at the Intel webpage, go to the serial numbers tab at the Products page at https://registrationcenter.intel.com/en/products/ to download the license file associated with the serial number for Intel® Parallel Studio XE Cluster Edition for Linux . After downloading the license file, rename it to license.lic and place it at 

    epi_corrections/docker/conf/intel/license.lic

- Make sure docker (CE) is installed before running the following commands:
```bash
cd epi_corrections/docker
bash generate_dockerfile.sh
bash build.sh
cd ../../
bash epi_corrections/docker/run.sh
```
This will start a docker environment with JupyterLab in the top directory specified in the folder structure.

Note that this might create the hidden folders .ipynb_checkpoints, .ipython, .python_history, .bash_history, .jupyter, .local, .config as well as the folder matlab
in this top directory. These folders can later be removed by running (from top level directory)
```bash
bash epi_corrections/docker/clean.sh
```

- Access JupyterLab in a browser from the provided URL in the terminal output.
From JupyterLab, open epi_corrections/notebooks/corretion_assessment_part_1.ipynb and follow the interactive guide.

The provided dcm2niix_ogeier, FreeSurfer's mri_robust_register, FSL TOPUP and EPIC should run fine with the precompiled binaries on a recent Intel CPU inside the docker environment. Instructions for recompiling EPIC can be found in epic_src . The Matlab SPM coregistration + MNI normalization code and other Matlab scripts in the notebook do not yet run inside the docker environment (need compilation of Matlab scripts to executables that can be run by the Matlab Compiler Runtime, which is installed in the docker environment), and thus require installation without docker.

## Dependencies for running without docker

- FSL (6.0.0) : For topup and various tools used.
- EPIC (included in the folder epic_src). See epic_src for a separate README.md for EPIC dependencies for compilation.
- libfftw3-dev (3.3.4) : for EPIC.
- freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.0-2beb96c : For mri_robust_register.
- nipy (0.4.1), nipype (1.1.5): for similarity metrics.
- dcm2niix version v1.0.20181125  GCC7.3.0 (64-bit Linux) 
modified by Oliver M. Geier to not reorient the scan to the 
scanner's RPI coordinate system (so that the orientation of .nii 
files converted with dcm2niix match the orientation of the 
original .dcm files (if the patient was not correctly aligned with the 
MRI scanner RPI corrdinate system during the scan. If the patient's orientation 
was correctly aligned with the mri machine coordinate system, then this
modification does not have an effect on the .dcm -> .nii conversion
than with the nonmodified version)).
Included under scripts along with wrapper script : For DICOM (.dcm) to NIFTI (.nii) file conversion.
- (optional) Nordic ICE 4.x : For running Head Motion Corrections and Perfusion Analysis.
- (optional) Matlab r2018b . : For analysing TOPUP and EPIC impacts in MNI space.
- (optional) spm12 . : --"--
- (optional) Anaconda distribution for Python 3 . : For running the remaining notebooks.

## References

__FSL topup__:

Andersson, J. L. R., Skare, S. & Ashburner, J. [How to correct susceptibility distortions in spin-echo echo-planar images: application to diffusion tensor imaging](https://www.sciencedirect.com/science/article/abs/pii/S1053811903003367). Neuroimage 20, 870–888 (2003).

__EPIC__:

Holland, D., Kuperman, J. M. & Dale, A. M. [Efficient Correction of Inhomogeneous Static Magnetic Field-Induced Distortion in Echo Planar Imaging](https://www.sciencedirect.com/science/article/abs/pii/S1053811909012294). Neuroimage 50, 175 (2010).
