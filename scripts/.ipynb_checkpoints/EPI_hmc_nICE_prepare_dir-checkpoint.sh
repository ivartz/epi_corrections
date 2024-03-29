#!/bin/bash

epi_root_folder=$1

output_root_folder="EPI_for_nICE_batch_head_motion_correction"

DSC_to_preproc_array=()

# Get GE DSC
while IFS=  read -r -d $'\0'; do
    DSC_to_preproc_array+=("$REPLY")
done < <(find $epi_root_folder -type f -iname "*e1.nii" -print0)

# Get SE DSC
while IFS=  read -r -d $'\0'; do
    DSC_to_preproc_array+=("$REPLY")
done < <(find $epi_root_folder -type f -iname "*e2.nii" -print0)

# Important.
cd $epi_root_folder

cd ..

# Now we are in at the right location for mkdir.

mkdir_command="mkdir $output_root_folder"

eval $mkdir_command

run_section () {

    DSC_nii=$1

    workdir=$2

    output_root_folder=$3

    id=$RANDOM

    cd $workdir

    # Assuming file name ends with
    # either ..e1.nii or ..e2.nii
    #echo_type=${DSC_nii:(-6):(-4)}
    
    mkdir_command="mkdir $output_root_folder/Perf_$id"

    eval $mkdir_command

    echo_command="echo $DSC_nii > $output_root_folder/Perf_$id/orig_file.txt"

    eval $echo_command

    cp_command="cp -v $DSC_nii $output_root_folder/Perf_$id"

    eval $cp_command
 
}

# So that run_section is visible in spawned bash shells by xargs
export -f run_section

# Multiprocessing pool on function with array elements as argument.
printf "%s\n" ${DSC_to_preproc_array[@]} | xargs -I file -n 1 -P $(nproc) bash -c 'run_section "$@"' _ file $(pwd) $output_root_folder
