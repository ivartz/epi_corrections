# epi_corrections
Python script for pipeline implementation for correction of magnetic susceptibility induced (geometric and intensity) artefacts from off-resonance field in EPI MRI images. Using existing libraries, such as FSL topup and EPIC.

The methods make use of the different distortions in Echo Planar Images (EPI) depending on direction of phase encoding in the k-space EPI encoding (positive/blip-up and negative blip-down phase encoding).

For a correction of a pair of EPI images (blip-up, blip-down), the different type of distortion based on phase encoding directions are used to to make an off-resonance field.

The off-resonance field is then used to "unwrap" each EPI image in the pair, aiming the two to be identical.

Dependencies (might work with other versions too):

FSL 6.0.0 : For topup and various tools used
EPIC (TODO included in the folder epic)
freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.0-2beb96c : For mri_robust_register
nipype : for similarity metrics
dcm2niiX version v1.0.20180622 GCC4.9.2 (64-bit Linux) (included under scripts along with wrapper script) : For DICOM (.dcm) to NIFTI (.nii) file conversion

References:

FSL topup:

Andersson, J. L. R., Skare, S. & Ashburner, J. How to correct susceptibility distortions in spin-echo echo-planar images: application to diffusion tensor imaging. NeuroImage 20, 870–888 (2003).

EPIC:

Holland, D., Kuperman, J. M. & Dale, A. M. Efficient Correction of Inhomogeneous Static Magnetic Field-Induced Distortion in Echo Planar Imaging. Neuroimage 50, 175 (2010).
