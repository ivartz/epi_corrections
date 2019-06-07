#!/bin/bash

# Example usage:
# bash EPI_perfusion_anal_nICE_prepare_dir.sh EPI_raw_DSC raw

epi_root_folder=$1

susc_corr_method=$2

cd "$epi_root_folder"

cd ..

output_root_folder="EPI_for_nICE_batch_perfusion_analysis"

DSC_to_preproc_array=()

if [ $susc_corr_method = "raw" ]; then
    # Get GE DSC
    while IFS=  read -r -d $'\0'; do
        DSC_to_preproc_array+=("$REPLY")
    done < <(find $epi_root_folder -type f -iname "*e1.nii" -print0)

    # Get SE DSC
    while IFS=  read -r -d $'\0'; do
        DSC_to_preproc_array+=("$REPLY")
    done < <(find $epi_root_folder -type f -iname "*e2.nii" -print0)
elif [ $susc_corr_method = "topup" ]; then
    # Get GE DSC
    while IFS=  read -r -d $'\0'; do
        DSC_to_preproc_array+=("$REPLY")
    done < <(find $epi_root_folder -type f -iname "*e1_prep_topup_applytopup_postp.nii" -print0)

    # Get SE DSC
    while IFS=  read -r -d $'\0'; do
        DSC_to_preproc_array+=("$REPLY")
    done < <(find $epi_root_folder -type f -iname "*e2_prep_topup_applytopup_postp.nii" -print0)
elif [ $susc_corr_method = "epic" ]; then
    # Get GE DSC
    while IFS=  read -r -d $'\0'; do
        DSC_to_preproc_array+=("$REPLY")
    done < <(find $epi_root_folder -type f -iname "*e1_applyepic.nii" -print0)

    # Get SE DSC
    while IFS=  read -r -d $'\0'; do
        DSC_to_preproc_array+=("$REPLY")
    done < <(find $epi_root_folder -type f -iname "*e2_applyepic.nii" -print0)
else
    echo "not known susc_corr_method"
    exit
fi
# Important.
cd "$epi_root_folder"

cd ..

# Now we are in at the right location for mkdir.

mkdir_command="mkdir -p $output_root_folder"

eval $mkdir_command

run_section () {

    DSC_nii=$1

    workdir=$2

    output_root_folder=$3

    id=$RANDOM

    cd "$workdir"

    # Assuming file name ends with
    # either ..e1.nii or ..e2.nii
    #echo_type=${DSC_nii:(-6):(-4)}
    
    mkdir_command="mkdir -p $output_root_folder/$id/DSC"

    eval $mkdir_command

    #DSC_dir=$(dirname "${DSC_nii}")

    echo_command="echo $DSC_nii > $output_root_folder/$id/orig_DSC_file.txt"

    eval $echo_command

    cp_command="cp -v $DSC_nii $output_root_folder/$id/DSC"

    eval $cp_command
 
}

# So that run_section is visible in spawned bash shells by xargs
export -f run_section

# Multiprocessing pool on function with array elements as argument.
printf "%s\n" "${DSC_to_preproc_array[@]}" | xargs -I file -n 1 -P $(nproc) bash -c 'run_section "$@"' _ file "$(pwd)" $output_root_folder

