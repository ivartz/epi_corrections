#!/bin/bash

# Example usage:
# bash EPI_perfusion_anal_nICE_prepare_copy_back.sh EPI_raw_DSC

epi_root_folder=$1

cd "$epi_root_folder"

cd ..

# Now we are sure that we are at the correct location.

epi_perf_root_folder="EPI_for_nICE_batch_perfusion_analysis"

perf_dir_array=()

# Get perf files
while IFS=  read -r -d $'\0'; do
    perf_dir_array+=("$REPLY")
done < <(find $epi_perf_root_folder -type d -iname "Perf" -print0)

DSC_orig_nii_file_info_array=()

# Get log file of original location
while IFS=  read -r -d $'\0'; do
    DSC_orig_nii_file_info_array+=("$REPLY")
done < <(find $epi_perf_root_folder -type f -iname "orig_DSC_file.txt" -print0)

# We want to interleave DSC_to_preproc_array
# and DSC_orig_file_array, so that 
# the motion corrected files in 
# DSC_to_preproc_array can ovewrite
# the original (noncorrected) files in
# DSC_orig_file_array .

for i in ${!perf_dir_array[@]}; do

    perf_dir_array=$(pwd)/${perf_dir_array[i]}

    #echo $perf_dir_array

    DSC_orig_nii_info=$(pwd)/${DSC_orig_nii_file_info_array[i]}

    #echo $DSC_orig_nii_info

    perf_dir_orig_DSC_nii_info_interleaved_array[i++]="$perf_dir_array;$DSC_orig_nii_info"

    #echo "$perf_dir_array;$DSC_orig_nii_info"

done

declare -p perf_dir_orig_DSC_nii_info_interleaved_array

run_section () {
    
    perf_dir_orig_DSC_nii_info_interleaved_string=$1

    #echo $perf_dir_orig_DSC_nii_info_interleaved_string

    perf_dir_orig_DSC_nii_info_interleaved_array=()

    IFS=';' read -ra perf_dir_orig_DSC_nii_info_interleaved_array <<< $perf_dir_orig_DSC_nii_info_interleaved_string

    # This is the directory
    # for the perfusion files by NordicICE .
    perf_dir=${perf_dir_orig_DSC_nii_info_interleaved_array[0]}

    DSC_orig_nii_info=${perf_dir_orig_DSC_nii_info_interleaved_array[1]}

    #echo $perf_dir
    #echo $DSC_orig_nii_info

    # This is the filepath + "/" + file name
    # for the original DSC file
    DSC_orig_nii=`cat "$DSC_orig_nii_info"`

    #echo $DSC_orig_nii

    DSC_orig_nii_file_name=$(basename "${DSC_orig_nii}")
    #echo $DSC_orig_nii_file_name
    
    DSC_orig_dir=$(dirname "${DSC_orig_nii}")
    #echo $DSC_orig_dir


    # Make the final perfusion output folder
    mkdir_command="mkdir -p $DSC_orig_dir/${DSC_orig_nii_file_name%.nii}_perf"

    #echo $mkdir_command
    eval $mkdir_command
    
    copy_back_command='cp -v "$perf_dir"/* "$DSC_orig_dir/${DSC_orig_nii_file_name%.nii}"_perf'

    #echo $copy_back_command    
    eval $copy_back_command

    # nICE bug workaround?!
    # Set sform to qform , since nICE seems to flip qform parameters in the header
    
    # Not currently done, since it seems to not cause problems (caused problems for FSL topup previously). 
    #reorient_command='fslorient -copysform2qform "$DSC_orig_dir/${DSC_orig_nii_file_name%.nii}"_perf/*'
    
    #eval $reorient_command
}

# So that run_section is visible in spawned bash shells by xargs
export -f run_section

# Multiprocessing pool on function with array elements as argument.
printf "%s\0" "${perf_dir_orig_DSC_nii_info_interleaved_array[@]}" | xargs -0 -I file -n 1 -P $(nproc) bash -c 'run_section "$@"' _ file

