# This Makefile script tries to correct B0 inhomogeneities from
# sets of images acquired by EPI sequence
#
# Author(s): Raimo Salo (Oslo University Hospital)
# Modified to only work on DSC images by
# Ivar Thokle Hovden (Oslo University Hospital)
#
# The script uses executable 'epic' by Holland et. al.
# to calculate the displacement field. In additional, it 
# uses the executable 'applyEpic'  by Holland et. al. to 
# apply the displacement field calculated by 'epic'
# to correct the DSC image sequence.
#
# (*) Dominic Holland, Joshua M. Kuperman, Anders M. Dale:
# "Efficient correction of inhomogeneous static magnetic field-induced
# distortion in Echo Planar Imaging", NeuroImage 50, 175-183
#
#  - Image data should consist of NIFTI images
#  - Image data should be saved under directory 'data'
#  - Directory structure under 'data' should be as follows:
#     Patient#/Examination#/ImageSetName/
#    where Patient# is a zero-padded three digit number (e.g. 004 for patient #4)
#          Examination# is a zero-padded two digit number (e.g. 06 for examination #6)
#          ImageSetName is DSC_prescan_P for forward prescan DSC EPI images
#                          DSC_prescan_A for reverse prescan DSC EPI images
#                          DSC for dynamic DSC image set
#
# Example directories: data/005/02/DSC_prescan_A
#                      data/019/07/DSC
#
# to get B0 corrected DSC images for all of the DSC images under directory data, type:
#  > make dsc_corrected
#
# to get the displacement maps for all of the data under directory data, type:
#  > make dsc_displacements
#
# to re-run everything, type
#  > make clean
#  > make correct_all
#
# Input targets
dsc_target_dirs = $(wildcard ./data/[0-9][0-9][0-9]/[0-9][0-9]/DSC)
dsc_A_target_dirs = $(wildcard ./data/[0-9][0-9][0-9]/[0-9][0-9]/DSC_prescan_A)
dsc_P_target_dirs = $(wildcard ./data/[0-9][0-9][0-9]/[0-9][0-9]/DSC_prescan_P)

# Output targets
dsc_disp_targets = $(subst DSC,dsc_displacement.mgz,$(dsc_target_dirs))
dsc_EPI_corr_targets = $(subst DSC,dsc_epic.mgz,$(dsc_target_dirs))
dsc_EPI_conv_targets = $(subst DSC,dsc_epic.nii.gz,$(dsc_target_dirs))

# do everything
.PHONY: correct_all
correct_all: dsc_check dsc_convert

.PHONY: dsc_convert
dsc_convert: $(dsc_EPI_conv_targets)

.PHONY: dsc_corrected
dsc_corrected: $(dsc_EPI_corr_targets)

.PHONY: dsc_displacements
dsc_displacements: $(dsc_disp_targets)

%/dsc_epic.nii.gz: %/dsc_epic_nice.nii.gz
	cp -f $< $@

# convert mgz to nii
%/dsc_epic_nice.nii.gz: %/dsc_epic.mgz
	mri_convert $< $@

.PRECIOUS: %/dsc_epic_nice.nii.gz

%/dsc_epic.mgz: %/DSC/dsc.mgz %/dsc_displacement.mgz
	./applyEpic -f $< -d $(@D)/dsc_displacement.mgz -fo $(@F) -od $(@D)

.PRECIOUS: %/dsc_epic.mgz

%/dsc_displacement.mgz: %/DSC_prescan_P/dsc_prescan_p.mgz %/DSC_prescan_A/dsc_prescan_a.mgz
	./epic -f $(@D)/DSC_prescan_P/dsc_prescan_p.mgz -r $(@D)/DSC_prescan_A/dsc_prescan_a.mgz -od $(@D) -do $(@F)

.PRECIOUS: %/dsc_displacements.mgz


# convert nii to mgz
%/DSC/dsc.mgz: %/DSC/1.nii
	mri_convert  $< $@

# convert nii forward prescan to mgz
%/DSC_prescan_A/dsc_prescan_a.mgz: %/DSC_prescan_A/1.nii
	mri_convert  $^ $@

# convert nii reverse prescan to mgz
%/DSC_prescan_P/dsc_prescan_p.mgz: %/DSC_prescan_P/1.nii
	mri_convert  $^ $@

.PRECIOUS: %/DSC/dsc.mgz %/DSC_prescan_A/dsc_prescan_a.mgz %/DSC_prescan_P/dsc_prescan_p.mgz


dsc_A_target_dirs = $(subst DSC,DSC_prescan_A,$(dsc_target_dirs))
dsc_P_target_dirs = $(subst DSC,DSC_prescan_P,$(dsc_target_dirs))

dsc_check: $(dsc_A_target_dirs) $(dsc_P_target_dirs)

#
# clean
#
.PHONY: clean
clean:
	rm -f data/*/*/*.mgz data/*/*/*/*.mgz data/*/*/*.nii data/*/*/*/*.bv* data/*/*/*.bv* data/*/*/*/*.gz data/*/*/*/*.nii.gz data/*/*/*/*.ecclog data/*/*/*.nii.gz data/*/*/*/*.mgh data/*/*/*/*_bv??s

