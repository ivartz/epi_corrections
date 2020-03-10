# Run from epi_corrections dir as
# bash scripts/compute-dice-between-rois.sh ../epi_corrections_out_2019_07_02_native_tumor_excluded_from_rcbv

correction_dir=$1

run_evals=1

script=$(dirname $0)/get-dice-between-rois.py

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
    
    echo "---- RAW TO EPIC ----"
    cbvdir=$(dirname ${rcbv_epic_files_arr_e1[i]})
    
    mniroiscommand="python $script --rois1 ${mnirois_raw_files_arr_e1[i]} --rois2 ${mnirois_epic_files_arr_e1[i]} > $cbvdir/mniroisrawcordice.txt"
    tumorroiscommand="python $script --rois1 ${tumorrois_raw_files_arr_e1[i]} --rois2 ${tumorrois_epic_files_arr_e1[i]} > $cbvdir/tumorroisrawcordice.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    
    if [ $run_evals == 1 ] ; then
        echo $mniroiscommand > $cbvdir/mniroisrawcordicecommand.txt
        echo $tumorroiscommand > $cbvdir/tumorroisrawcordicecommand.txt
        eval $mniroiscommand
        eval $tumorroiscommand
    fi
    
    echo "---- RAW TO TOPUP ----"
    cbvdir=$(dirname ${rcbv_topup_files_arr_e1[i]})
    
    mniroiscommand="python $script --rois1 ${mnirois_raw_files_arr_e1[i]} --rois2 ${mnirois_topup_files_arr_e1[i]} > $cbvdir/mniroisrawcordice.txt"
    tumorroiscommand="python $script --rois1 ${tumorrois_raw_files_arr_e1[i]} --rois2 ${tumorrois_topup_files_arr_e1[i]} > $cbvdir/tumorroisrawcordice.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    
    if [ $run_evals == 1 ] ; then
        echo $mniroiscommand > $cbvdir/mniroisrawcordicecommand.txt
        echo $tumorroiscommand > $cbvdir/tumorroisrawcordicecommand.txt
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
    
    echo "---- RAW TO EPIC ----"
    cbvdir=$(dirname ${rcbv_epic_files_arr_e2[i]})
    
    mniroiscommand="python $script --rois1 ${mnirois_raw_files_arr_e2[i]} --rois2 ${mnirois_epic_files_arr_e2[i]} > $cbvdir/mniroisrawcordice.txt"
    tumorroiscommand="python $script --rois1 ${tumorrois_raw_files_arr_e2[i]} --rois2 ${tumorrois_epic_files_arr_e2[i]} > $cbvdir/tumorroisrawcordice.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    
    if [ $run_evals == 1 ] ; then
        echo $mniroiscommand > $cbvdir/mniroisrawcordicecommand.txt
        echo $tumorroiscommand > $cbvdir/tumorroisrawcordicecommand.txt
        eval $mniroiscommand
        eval $tumorroiscommand
    fi
        
    echo "---- RAW TO TOPUP ----"
    cbvdir=$(dirname ${rcbv_topup_files_arr_e2[i]})
    
    mniroiscommand="python $script --rois1 ${mnirois_raw_files_arr_e2[i]} --rois2 ${mnirois_topup_files_arr_e2[i]} > $cbvdir/mniroisrawcordice.txt"
    tumorroiscommand="python $script --rois1 ${tumorrois_raw_files_arr_e2[i]} --rois2 ${tumorrois_topup_files_arr_e2[i]} > $cbvdir/tumorroisrawcordice.txt"
    
    echo $mniroiscommand
    echo $tumorroiscommand
    
    if [ $run_evals == 1 ] ; then
        echo $mniroiscommand > $cbvdir/mniroisrawcordicecommand.txt
        echo $tumorroiscommand > $cbvdir/tumorroisrawcordicecommand.txt
        eval $mniroiscommand
        eval $tumorroiscommand
    fi
done
