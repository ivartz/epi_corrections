#!/bin/bash

# RUN
# dicom_to_niix_same_folder_structure.sh <dicom_root_folder> <nifti_output_folder> <directory_keyword> 2>&1 | tee Baseline\ nii\ conversion\ report\ 3D.txt

# Converts .dcm files in all subfolders of dicom_root_folder 
# with file name containing directory_keyword to .nii files .

# The .nii files are placed in a folder called NIFTI starting from
# the root directory of the script.

# The .nii files in the NIFTI folder are organized in original 
# file structure as in dicom_root_folder .

# This script was used on Philips DICOM data. 

# Author: Ivar Thokle Hovden
# Last modified: 2018-11-26

# dcm2niix version used: 1.0.20180622

# This dcm2niix version correctly performs
# Philips-specific pixel value scaling if the 
# DICOM files are from a Philips MRI
# based on the conventional DICOM 
# header values of:

# Rescale Slope: RS
# Rescale Intercept: RI
# Scale Slope: SS

# Source of Philips pixel scaling convention:
# https://www.jiscmail.ac.uk/cgi-bin/webadmin?A2=MRICRO;af27b9c2.0801

# Each raw pixel gray scale value (PV) in the .dcm
# files is represented as a scaled intensity value (SI)
# in the NiFTI file according to the formula:

##|||||||||||||||||||||||||||||||||##
##                                 ##
## SI = PV * scl_slope + scl_inter ##
##                                 ##
##|||||||||||||||||||||||||||||||||##


# Depending on the combination of the values
# RS, RI and SS;
# SI is set by folliwng the Philips-specific
# calculations:

# Calculate displayed value on console (DV)
# DV = PV * RS + RI  

# Calculate floating poing value (FP)
# FP = DV / (RS * SS)

# DV is on same form as SI .

# Determine SI:

# If RI=0 and SS>0, then:

# scl_slope = RS
# scl_inter = RI
# SI = FP

# else:

# scl_slope = RS
# scl_inter = RI
# SI = DV

# An example:
#
# By inspection of dcm2niix output (RS:RI:SS),
# original dicom header files (0040,9225 Real World Value Slope)
# and corresponding NiFTI header file (scl_slope and scl_inter)
# it was observed that 
# 0040,9225 Real World Value Slope = 1.115018315018315 
# ~= 
# scl_slope = 1.11502
# ~=
# Using RWVSlope:RWVIntercept = 1.11502:0
#  Philips Scaling Values RS:RI:SS = 1.11502:0:0 (see PMC3998685)

# SS=0, so the scaling should have chosen the "else" - option.
# Hence, 
# scl_slope = RS = 1.11502
# scl_inter = RI = 0
# SI = DV
# and the pixel value scaling resulting from 
# converting a series of DICOM files to a NiFTI file
# is supposed to be:
# SI = PV * 1.11502
# The scaling was further verified by multiplying an original DICOM image with 1.11502, and comparing the ROI statistics (max and min) of the resulting image with the
# ROI statistics of the corresponding NiFTI image in NordicICE. Only marginal (rounding error)
# differences were observed for the min and max values (0.1 error). ROI histograms identical by eye.

#dicom_root_folder="../DICOM"
dicom_root_folder=$1
#nifti_output_folder="../../../../../../../home/ivar/Documents/data_local/IVS\ EPI\ Baseline\ Local/NIFTI_3D"
nifti_output_folder=$2

# Select only subfolders inside dicom_root_folder
# containing following keyword/string.
directory_keyword=$3

delete_pre_existing_destination_folders=false

# Create empty array to fill inn matched dicom folders w. filepath
# that contain .dcm files to be converted to .nii files (input directories).
directories_to_convert_array=()

# Store input directories to bash array directories_to_convert_array
while IFS=  read -r -d $'\0'; do
    directories_to_convert_array+=("$REPLY")
done < <(find $dicom_root_folder -type d -iname "*$directory_keyword*" -print0)

# Iterate over input directories
for i in "${!directories_to_convert_array[@]}"; do

    echo "---- iteration $i ----"

    input_folder=${directories_to_convert_array[i]}

    echo "input folder $i: $input_folder"

    output_folder="$nifti_output_folder${input_folder#$dicom_root_folder}"

    echo "output folder $i: $output_folder"    

    if [ -d "$output_folder" ]; then
        echo "output folder $i already exists"

        if [ ! $delete_pre_existing_destination_folders = true ]; then
            echo "delete_pre_existing_destination_folders is set to false"
            echo "not deleting pre-existing files"
            echo "assuming already converted files"
            echo "skipping conversion"
            continue
        fi
        
        echo "delete_pre_existing_destination_folders is set to true"
        echo "deleting pre-existing output folder"
        rm -rd "$output_folder"        
    fi  

    echo "output folder $i doesn't exist, creating"
    mkdir -p "$output_folder"

    # Here is the dcm2niix command
    #command="dcm2nii -4 y -d y -e y -g n -m n -n y -o '$output_folder' -p y -r y -v y '$input_folder'"
    command="/home/ivar/mricrogl_lx/dcm2niix -f %t_%p_%s -o '$output_folder' -z n '$input_folder'"

    echo "converting DICOM files in input folder number $i to NIFTI files in output folder number $i with the command:"

    echo $command

    # Run the conversion command
    eval $command

done

