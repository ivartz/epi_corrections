#!/bin/bash

# Custom slow script for elastix based head rigid motion correction.

FSLOUTPUTTYPE=NIFTI

epi_root_folder=$1
#epi_root_folder=EPI

DSC_to_preproc_array=()

# Get GE DSC
while IFS=  read -r -d $'\0'; do
    DSC_to_preproc_array+=("$REPLY")
done < <(find $epi_root_folder -type f -iname "*e1.nii" -print0)

# Get SE DSC
while IFS=  read -r -d $'\0'; do
    DSC_to_preproc_array+=("$REPLY")
done < <(find $epi_root_folder -type f -iname "*e2.nii" -print0)

run_section () {

    DSC_nii=$1

    id=$RANDOM

    DSC_relative_file=$DSC_nii
    

    # Temporary dir
    temp_dir=temp_$id
    mkdir -p $temp_dir
    

    # Split
    dyn_prefix='dyn_'

    fsl_split_command="fslsplit $DSC_relative_file $temp_dir/$dyn_prefix -t"

    echo "$id: $fsl_split_command"

    eval $fsl_split_command

    
    #for dyn_i in `seq 1 $(ls temp_dir_name | wc -l)`; do
    #    echo $dyn_i
    #done

    temp_dir_elastix_dyn_out=$temp_dir/temp_dyn_cor_all
    mkdir -p $temp_dir_elastix_dyn_out

    #echo "$id: $fsl_split_command"

    num_dyn=$(($(ls $temp_dir | wc -l)-1))

    for ((dyn_i = 0 ; dyn_i < $num_dyn ; ++dyn_i)); do

        dyn_i_padded=$(printf "%04d\n" $dyn_i)
        
        temp_dir_elastix_dyn_i_out=$temp_dir/temp_dyn_cor_$dyn_i_padded

        #echo $temp_dir_elastix_dyn_i_out

        mkdir -p $temp_dir_elastix_dyn_i_out
        

        # intrapatient; rigid + B-spline transformation; localized mutual information combined with bending energy penalty
        # This performed best
        # http://elastix.bigr.nl/wiki/index.php/Par0023
        elastix_command='elastix -f "$temp_dir/dyn_0000.nii" -m "$temp_dir/dyn_$dyn_i_padded.nii" -p Par0023_Rigid.txt -out "$temp_dir_elastix_dyn_i_out"'

        # intra patient; rigid + B-spline transformation; mutual information, multi parametric mutual information
        # http://elastix.bigr.nl/wiki/index.php/Par0027
        #elastix_command='elastix -f "$temp_dir/dyn_0000.nii" -m "$temp_dir/dyn_$dyn_i_padded.nii" -p Par0027_Rigid.txt -out "$temp_dir_elastix_dyn_i_out"'

        #echo $elastix_command

        eval $elastix_command

        #fslcpgeom_command='fslcpgeom "$temp_dir/dyn_$dyn_i_padded.nii" "$temp_dir_elastix_dyn_i_out/result.0.nii"'

        #eval $fslcpgeom_command

        cp_command='cp -v "$temp_dir_elastix_dyn_i_out/result.0.nii" "$temp_dir_elastix_dyn_out/r_dyn_$dyn_i_padded.nii"'
        
        eval $cp_command
    done

    # Merge
    fslmerge -t $temp_dir/r_dyn_cor_merged.nii $temp_dir_elastix_dyn_out/r_dyn_[0-9][0-9][0-9][0-9].nii
    
    
    # Copy back
    #cp -v $temp_dir/r_dyn_cor_merged.nii ${DSC_relative_file%.nii}_mc_elastix.nii
    # Version that overwrites the original DSC file
    cp -v $temp_dir/r_dyn_cor_merged.nii $DSC_relative_file

    # Delete temporary dir
    rm -rdf $temp_dir
}

# So that run_section is visible in spawned bash shells by xargs
export -f run_section

# Multiprocessing pool on function with array elements as argument.
printf "%s\n" ${DSC_to_preproc_array[@]} | xargs -I file -n 1 -P $(nproc) bash -c 'run_section "$@"' _ file


