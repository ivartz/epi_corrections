#!/bin/bash

epi_root_folder=$1

cd $epi_root_folder

cd ..

# Now we are shure that we are at the correct location.

epi_mc_root_folder="EPI_for_nICE_batch_head_motion_correction"

DSC_to_preproc_array=()

# Get motion corrected files
while IFS=  read -r -d $'\0'; do
    DSC_to_preproc_array+=("$REPLY")
done < <(find $epi_mc_root_folder -type f -iname "moco_*" -print0)

DSC_orig_file_info_array=()

# Get log file of original location
while IFS=  read -r -d $'\0'; do
    DSC_orig_file_info_array+=("$REPLY")
done < <(find $epi_mc_root_folder -type f -iname "orig_file.txt" -print0)

# We want to interleave DSC_to_preproc_array
# and DSC_orig_file_array, so that 
# the motion corrected files in 
# DSC_to_preproc_array can ovewrite
# the original (noncorrected) files in
# DSC_orig_file_array .

for i in ${!DSC_to_preproc_array[@]}; do

    DSC_preproc_nii=$(pwd)/${DSC_to_preproc_array[i]}
    DSC_orig_nii_info=$(pwd)/${DSC_orig_file_info_array[i]}

    DSC_preproc_orig_interleaved_array[i++]="$DSC_preproc_nii;$DSC_orig_nii_info"

done

declare -p DSC_preproc_orig_interleaved_array

run_section () {
    
    DSC_preproc_orig_interleaved_string=$1

    DSC_preproc_orig_interleaved_array=()

    IFS=';' read -ra DSC_preproc_orig_interleaved_array <<< $DSC_preproc_orig_interleaved_string

    # This is the filepath + "/" + file name
    # for the motion corrected file by NordicICE .
    DSC_preproc_nii=${DSC_preproc_orig_interleaved_array[0]}

    DSC_orig_nii_info=${DSC_preproc_orig_interleaved_array[1]}

    # This is the filepath + "/" + file name
    # for the original, not motion corrected
    # file, that is going to be overwritten.
    DSC_orig_nii=`cat $DSC_orig_nii_info`

    # nICE bug workaround?!
    # Set sform to qform , since nICE seems to sform_i_orientation and sform_j_orientation
    reorient_command="fslorient -copysform2qform $DSC_preproc_nii"
    
    eval $reorient_command
    
    copy_back_command="cp -v $DSC_preproc_nii $DSC_orig_nii"
    
    eval $copy_back_command
}

# So that run_section is visible in spawned bash shells by xargs
export -f run_section

# Multiprocessing pool on function with array elements as argument.
printf "%s\n" ${DSC_preproc_orig_interleaved_array[@]} | xargs -I file -n 1 -P $(nproc) bash -c 'run_section "$@"' _ file
