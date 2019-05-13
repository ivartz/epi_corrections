#!/bin/bash

# Using FreeSurfer's FSFAST preprocessing on EPI data
# https://surfer.nmr.mgh.harvard.edu/fswiki/FsFastTutorialV5.1/FsFastPreProc
# for head motion correction only.

FSF_OUTPUT_FORMAT=nii

epi_root_folder=$1

mkdir sess_dir
mkdir sess_dir/func_dir
mkdir sess_dir/func_dir/001

DSC_to_preproc_array=()

# Get GE / e1 DSC
while IFS=  read -r -d $'\0'; do
    DSC_to_preproc_array+=("$REPLY")
done < <(find $epi_root_folder -type f -iname "*e1.nii" -print0)

# Get SE / e2 DSC
while IFS=  read -r -d $'\0'; do
    DSC_to_preproc_array+=("$REPLY")
done < <(find $epi_root_folder -type f -iname "*e2.nii" -print0)

for i in "${!DSC_to_preproc_array[@]}"; do

    echo "---- iteration $i ----"

    DSC_nii=${DSC_to_preproc_array[i]}

    # Temporarily copy the DSC file into a
    # directory structure that FSFAST understands.
    cp -v $DSC_nii sess_dir/func_dir/001/f.nii

    # Preprocess command.
    preproc-sess -per-run -s sess_dir -fsd func_dir -nostc -nosmooth -nomask -noreg -noinorm -no-subcort-mask
    
    #plot-twf-sess -s sess_dir -fsd func_dir -mc

    # Copy back
    #cp -v sess_dir/func_dir/001/fmcpr.nii ${DSC_nii%.nii}_mc_fs.nii
    # Version that overwrites the original DSC file
    cp -v sess_dir/func_dir/001/fmcpr.nii $DSC_nii
    
    #cp -v sess_dir/func_dir/fmcpr.mcdat.png ${DSC_nii%.nii}_mc_plot.png

    rm -rd log
    rm sess_dir/func_dir/001/*
    rm sess_dir/func_dir/template*

done

rm -rd sess_dir

