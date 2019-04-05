#!/bin/bash

# Example usage:
# bash EPI_perfusion_anal_nICE_make_uncorr_dir.sh EPI

raw_epi_root_folder=$1

cd "$raw_epi_root_folder"

cd ..

dir_to_cp=()

output_folder="EPI_raw_DSC"

while IFS=  read -r -d $'\0'; do
    dir_to_cp+=("$REPLY")
done < <(find $raw_epi_root_folder -type d -iname *_scan -print0)

while IFS=  read -r -d $'\0'; do
    dir_to_cp+=("$REPLY")
done < <(find $raw_epi_root_folder -type d -iname *h_sense -print0)

#echo $(pwd)

run_section () {
    dir_to_cp=$1
    raw_epi_root_folder=$2
    output_folder=$3
    workdir=$4

    cd "$workdir"

    newdir=$output_folder${dir_to_cp#$raw_epi_root_folder}

    echo $dir_to_cp
    echo $newdir
    
    mkdir_command="mkdir -p $newdir"

    eval $mkdir_command
    #echo $mkdir_command

    cp_command="cp -v $dir_to_cp/* $newdir"

    eval $cp_command
    #echo $cp_command
}

# So that run_section is visible in spawned bash shells by xargs
export -f run_section

# Multiprocessing pool on function with array elements as argument.
printf "%s\n" "${dir_to_cp[@]}" | xargs -I dir -n 1 -P $(nproc) bash -c 'run_section "$@"' _ dir $raw_epi_root_folder $output_folder "$(pwd)"

