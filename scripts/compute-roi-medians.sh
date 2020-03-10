# Run from epi_corrections dir as
# bash scripts/compute-roi-medians.sh ../epi_corrections_out_2019_07_02_native_tumor_excluded_from_rcbv

correction_dir=$1

run_evals=1

script=$(dirname $0)/get-median-values-from-rois.py

# Gradient echo (e1)

# rCBV files
readarray rcbv_epic_files_arr_e1 < <(find $correction_dir/EPI_applyepic -type d -name *e1_applyepic_perf | xargs -I {} echo {}/Normalized_rCBV_map_-Leakage_corrected.nii)

readarray rcbv_topup_files_arr_e1 < <(find $correction_dir/EPI_applytopup -type d -name *e1_prep_topup_applytopup_postp_perf | xargs -I {} echo {}/Normalized_rCBV_map_-Leakage_corrected.nii)

readarray rcbv_raw_files_arr_e1 < <(find $correction_dir/EPI_raw_DSC -type d -name *e1_perf | xargs -I {} echo {}/Normalized_rCBV_map_-Leakage_corrected.nii)

# Template ROIs in DSC space
readarray mnirois_epic_files_arr_e1 < <(find $correction_dir/EPI_applyepic -type f -name ryinvapplied_e1*)
readarray mnirois_topup_files_arr_e1 < <(find $correction_dir/EPI_applytopup -type f -name ryinvapplied_e1*)
readarray mnirois_raw_files_arr_e1 < <(find $correction_dir/EPI_raw_DSC -type f -name ryinvapplied_e1*)

# Tumor ROIs in DSC space
readarray tumorrois_epic_files_arr_e1 < <(find $correction_dir/EPI_applyepic -type f -name re1_tumor_segments.nii)
readarray tumorrois_topup_files_arr_e1 < <(find $correction_dir/EPI_applytopup -type f -name re1_tumor_segments.nii)
readarray tumorrois_raw_files_arr_e1 < <(find $correction_dir/EPI_raw_DSC -type f -name re1_tumor_segments.nii)

for (( i = 0 ; i < ${#rcbv_epic_files_arr_e1[@]} ; i++ )) ; do
    
    echo "---- EPIC ----"
    cbv=${rcbv_epic_files_arr_e1[i]}
    cbvdir=$(dirname ${rcbv_epic_files_arr_e1[i]})
    mnirois=${mnirois_epic_files_arr_e1[i]}
    tumorrois=${tumorrois_epic_files_arr_e1[i]}
    
    mniroiscommand="python $script --datanifti ${rcbv_epic_files_arr_e1[i]} --roinifti ${mnirois_epic_files_arr_e1[i]} > $cbvdir/mniroismedians.txt"
    tumorroiscommand="python $script --datanifti ${rcbv_epic_files_arr_e1[i]} --roinifti ${tumorrois_epic_files_arr_e1[i]} > $cbvdir/tumorroismedians.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    echo $mniroiscommand > $cbvdir/mniroiscommand.txt
    echo $tumorroiscommand > $cbvdir/tumorroiscommand.txt
    
    if [ $run_evals == 1 ] ; then
        eval $mniroiscommand
        eval $tumorroiscommand
    fi
        
    echo "---- TOPUP ----"
    cbv=${rcbv_topup_files_arr_e1[i]}
    cbvdir=$(dirname ${rcbv_topup_files_arr_e1[i]})
    mnirois=${mnirois_topup_files_arr_e1[i]}
    tumorrois=${tumorrois_topup_files_arr_e1[i]}
    
    mniroiscommand="python $script --datanifti ${rcbv_topup_files_arr_e1[i]} --roinifti ${mnirois_topup_files_arr_e1[i]} > $cbvdir/mniroismedians.txt"
    tumorroiscommand="python $script --datanifti ${rcbv_topup_files_arr_e1[i]} --roinifti ${tumorrois_topup_files_arr_e1[i]} > $cbvdir/tumorroismedians.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    
    if [ $run_evals == 1 ] ; then
        echo $mniroiscommand > $cbvdir/mniroiscommand.txt
        echo $tumorroiscommand > $cbvdir/tumorroiscommand.txt
        eval $mniroiscommand
        eval $tumorroiscommand
    fi
    
    echo "---- RAW ----"
    cbv=${rcbv_raw_files_arr_e1[i]}
    cbvdir=$(dirname ${rcbv_raw_files_arr_e1[i]})
    mnirois=${mnirois_raw_files_arr_e1[i]}
    tumorrois=${tumorrois_raw_files_arr_e1[i]}
    
    mniroiscommand="python $script --datanifti ${rcbv_raw_files_arr_e1[i]} --roinifti ${mnirois_raw_files_arr_e1[i]} > $cbvdir/mniroismedians.txt"
    tumorroiscommand="python $script --datanifti ${rcbv_raw_files_arr_e1[i]} --roinifti ${tumorrois_raw_files_arr_e1[i]} > $cbvdir/tumorroismedians.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    
    if [ $run_evals == 1 ] ; then
        echo $mniroiscommand > $cbvdir/mniroiscommand.txt
        echo $tumorroiscommand > $cbvdir/tumorroiscommand.txt
        eval $mniroiscommand
        eval $tumorroiscommand
    fi
done

# Spin echo (e2)

# rCBV files
readarray rcbv_epic_files_arr_e2 < <(find $correction_dir/EPI_applyepic -type d -name *e2_applyepic_perf | xargs -I {} echo {}/Normalized_rCBV_map_-Leakage_corrected.nii)

readarray rcbv_topup_files_arr_e2 < <(find $correction_dir/EPI_applytopup -type d -name *e2_prep_topup_applytopup_postp_perf | xargs -I {} echo {}/Normalized_rCBV_map_-Leakage_corrected.nii)

readarray rcbv_raw_files_arr_e2 < <(find $correction_dir/EPI_raw_DSC -type d -name *e2_perf | xargs -I {} echo {}/Normalized_rCBV_map_-Leakage_corrected.nii)

# Template ROIs in DSC space
readarray mnirois_epic_files_arr_e2 < <(find $correction_dir/EPI_applyepic -type f -name ryinvapplied_e2*)
readarray mnirois_topup_files_arr_e2 < <(find $correction_dir/EPI_applytopup -type f -name ryinvapplied_e2*)
readarray mnirois_raw_files_arr_e2 < <(find $correction_dir/EPI_raw_DSC -type f -name ryinvapplied_e2*)

# Tumor ROIs in DSC space
readarray tumorrois_epic_files_arr_e2 < <(find $correction_dir/EPI_applyepic -type f -name re2_tumor_segments.nii)
readarray tumorrois_topup_files_arr_e2 < <(find $correction_dir/EPI_applytopup -type f -name re2_tumor_segments.nii)
readarray tumorrois_raw_files_arr_e2 < <(find $correction_dir/EPI_raw_DSC -type f -name re2_tumor_segments.nii)

for (( i = 0 ; i < ${#rcbv_epic_files_arr_e2[@]} ; i++ )) ; do
    
    echo "---- EPIC ----"
    cbv=${rcbv_epic_files_arr_e2[i]}
    cbvdir=$(dirname ${rcbv_epic_files_arr_e2[i]})
    mnirois=${mnirois_epic_files_arr_e2[i]}
    tumorrois=${tumorrois_epic_files_arr_e2[i]}
    
    mniroiscommand="python $script --datanifti ${rcbv_epic_files_arr_e2[i]} --roinifti ${mnirois_epic_files_arr_e2[i]} > $cbvdir/mniroismedians.txt"
    tumorroiscommand="python $script --datanifti ${rcbv_epic_files_arr_e2[i]} --roinifti ${tumorrois_epic_files_arr_e2[i]} > $cbvdir/tumorroismedians.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    
    if [ $run_evals == 1 ] ; then
        echo $mniroiscommand > $cbvdir/mniroiscommand.txt
        echo $tumorroiscommand > $cbvdir/tumorroiscommand.txt
        eval $mniroiscommand
        eval $tumorroiscommand
    fi
    
    echo "---- TOPUP ----"
    cbv=${rcbv_topup_files_arr_e2[i]}
    cbvdir=$(dirname ${rcbv_topup_files_arr_e2[i]})
    mnirois=${mnirois_topup_files_arr_e2[i]}
    tumorrois=${tumorrois_topup_files_arr_e2[i]}
    
    mniroiscommand="python $script --datanifti ${rcbv_topup_files_arr_e2[i]} --roinifti ${mnirois_topup_files_arr_e2[i]} > $cbvdir/mniroismedians.txt"
    tumorroiscommand="python $script --datanifti ${rcbv_topup_files_arr_e2[i]} --roinifti ${tumorrois_topup_files_arr_e2[i]} > $cbvdir/tumorroismedians.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    
    if [ $run_evals == 1 ] ; then
        echo $mniroiscommand > $cbvdir/mniroiscommand.txt
        echo $tumorroiscommand > $cbvdir/tumorroiscommand.txt
        eval $mniroiscommand
        eval $tumorroiscommand
    fi
    
    echo "---- RAW ----"
    cbv=${rcbv_raw_files_arr_e2[i]}
    cbvdir=$(dirname ${rcbv_raw_files_arr_e2[i]})
    mnirois=${mnirois_raw_files_arr_e2[i]}
    tumorrois=${tumorrois_raw_files_arr_e2[i]}
    
    mniroiscommand="python $script --datanifti ${rcbv_raw_files_arr_e2[i]} --roinifti ${mnirois_raw_files_arr_e2[i]} > $cbvdir/mniroismedians.txt"
    tumorroiscommand="python $script --datanifti ${rcbv_raw_files_arr_e2[i]} --roinifti ${tumorrois_raw_files_arr_e2[i]} > $cbvdir/tumorroismedians.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    
    if [ $run_evals == 1 ] ; then
        echo $mniroiscommand > $cbvdir/mniroiscommand.txt
        echo $tumorroiscommand > $cbvdir/tumorroiscommand.txt
        eval $mniroiscommand
        eval $tumorroiscommand
    fi
done