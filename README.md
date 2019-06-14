# epi_corrections
Python script for pipeline implementation for correction of 
magnetic susceptibility induced (geometric and intensity) 
artefacts from off-resonance field in EPI MRI images. 
Using FSL TOPUP and EPIC.

## Methods

See reports/PosterHovden.pdf (NFMF MedFys 2019).

The methods make use of the different distortions in 
Echo Planar Images (EPI) depending on direction of 
phase encoding in the k-space EPI encoding 
(positive/blip-up and negative blip-down phase encoding).

For a correction of a pair of EPI images (blip-up, blip-down), 
the different type of distortion based on phase encoding 
directions are used to to make an off-resonance field (FSL TOPUP
or a displacement field (EPIC)).

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
    │   ├── freesurfer
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
Register on https://surfer.nmr.mgh.harvard.edu/fswiki/License to get a FreeSurfer License file.
Store the license file accordingly in:

    epi_corrections/docker/freesurfer/license.txt

Make sure docker (CE) is installed before running the following commands:
```bash
cd epi_corrections/docker
bash generate_dockerfile.sh
bash build.sh
cd ../../
bash epi_corrections/docker/run.sh
```
starts a docker environment with JupyterLab in the top directory specified in the folder structure.
Note that this will create the hidden folders .ipynb_checkpoints, .ipython, .jupyter, .local as well as the folder matlab
in this top directory.
Access JupyterLab in a browser from the provided URL in the terminal output.
From JupyterLab, open epi_corrections/notebooks/corretion_assessment_part_1.ipynb and follow the interactive guide.

## Standalone dependencies

- FSL 6.0.0 : For topup and various tools used
- EPIC (included in the folder epic_src)
- freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.0-2beb96c : For mri_robust_register
- nipype : for similarity metrics
- dcm2niix version v1.0.20181125  GCC7.3.0 (64-bit Linux) 
modified by Oliver M. Geier to not reorient the scan to the 
scanner's RPI coordinate system (so that the orientation of .nii 
files converted with dcm2niix match the orientation of the 
original .dcm files (if the patient was not correctly aligned with the 
MRI scanner RPI corrdinate system during the scan. If the patient's orientation 
was correctly aligned with the mri machine coordinate system, then this
modification does not have an effect on the .dcm -> .nii conversion
than with the nonmodified version)).
Included under scripts along with wrapper script : For DICOM (.dcm) to NIFTI (.nii) file conversion

## References

__FSL topup__:

Andersson, J. L. R., Skare, S. & Ashburner, J. How to correct susceptibility distortions in spin-echo echo-planar images: application to diffusion tensor imaging. NeuroImage 20, 870–888 (2003).

__EPIC__:

Holland, D., Kuperman, J. M. & Dale, A. M. Efficient Correction of Inhomogeneous Static Magnetic Field-Induced Distortion in Echo Planar Imaging. Neuroimage 50, 175 (2010).
