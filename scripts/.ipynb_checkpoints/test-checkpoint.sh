# Run from epi_corrections dir as
# bash scripts/test.sh ../epi_corrections_out_2019_07_02_native_tumor_excluded_from_rcbv

correction_dir=$1

# Gradient echo (e1) and Spin echo (e2)

for (( i = 1 ; i < 3 ; i++ )) ; do

    # MNI ROI median rCBV files
    readarray mni_medians_epic_files_arr_e${i} < <(find $correction_dir/EPI_applyepic -type d -name *e${i}_applyepic_perf | xargs -I {} echo {}/mniroismedians.txt)

    readarray mni_medians_topup_files_arr_e${i} < <(find $correction_dir/EPI_applytopup -type d -name *e${i}_prep_topup_applytopup_postp_perf | xargs -I {} echo {}/mniroismedians.txt)

    readarray mni_medians_raw_files_arr_e${i} < <(find $correction_dir/EPI_raw_DSC -type d -name *e${i}_perf | xargs -I {} echo {}/mniroismedians.txt)

    # MNI ROI dice files (ground truth)

    readarray gt_epic_mni_dice_files_arr_e${i} < <(find $correction_dir/EPI_applyepic -type d -name *e${i}_applyepic_perf | xargs -I {} echo {}/mniroisgtepicdice.txt)

    readarray gt_topup_mni_dice_files_arr_e${i} < <(find $correction_dir/EPI_applytopup -type d -name *e${i}_prep_topup_applytopup_postp_perf | xargs -I {} echo {}/mniroisgttopupdice.txt)

    readarray gt_raw_mni_dice_files_arr_e${i} < <(find $correction_dir/EPI_raw_DSC -type d -name *e${i}_perf | xargs -I {} echo {}/mniroisgtrawdice.txt)

    # MNI ROI dice files
    : '
    readarray raw_epic_mni_dice_files_arr_e${i} < <(find $correction_dir/EPI_applyepic -type d -name *e${i}_applyepic_perf | xargs -I {} echo {}/mniroisrawcordice.txt)

    readarray raw_topup_mni_dice_files_arr_e${i} < <(find $correction_dir/EPI_applytopup -type d -name *e${i}_prep_topup_applytopup_postp_perf | xargs -I {} echo {}/mniroisrawcordice.txt)

    # Tumor ROI dice files
    
    readarray raw_epic_tumor_dice_files_arr_e${i} < <(find $correction_dir/EPI_applyepic -type d -name *e${i}_applyepic_perf | xargs -I {} echo {}/tumorroisrawcordice.txt)

    readarray raw_topup_tumor_dice_files_arr_e${i} < <(find $correction_dir/EPI_applytopup -type d -name *e${i}_prep_topup_applytopup_postp_perf | xargs -I {} echo {}/tumorroisrawcordice.txt)
    '

done

# Split arrays into SENSE and not SENSE acceleration
# With SENSE
readarray mni_medians_epic_files_arr_e1_sense < <(printf '%s\n' ${mni_medians_epic_files_arr_e1[*]} | grep -i sense)
readarray mni_medians_topup_files_arr_e1_sense < <(printf '%s\n' ${mni_medians_topup_files_arr_e1[*]} | grep -i sense)
readarray mni_medians_raw_files_arr_e1_sense < <(printf '%s\n' ${mni_medians_raw_files_arr_e1[*]} | grep -i sense)

readarray gt_epic_mni_dice_files_arr_e1_sense < <(printf '%s\n' ${gt_epic_mni_dice_files_arr_e1[*]} | grep -i sense)
readarray gt_topup_mni_dice_files_arr_e1_sense < <(printf '%s\n' ${gt_topup_mni_dice_files_arr_e1[*]} | grep -i sense)
readarray gt_raw_mni_dice_files_arr_e1_sense < <(printf '%s\n' ${gt_raw_mni_dice_files_arr_e1[*]} | grep -i sense)

readarray mni_medians_epic_files_arr_e2_sense < <(printf '%s\n' ${mni_medians_epic_files_arr_e2[*]} | grep -i sense)
readarray mni_medians_topup_files_arr_e2_sense < <(printf '%s\n' ${mni_medians_topup_files_arr_e2[*]} | grep -i sense)
readarray mni_medians_raw_files_arr_e2_sense < <(printf '%s\n' ${mni_medians_raw_files_arr_e2[*]} | grep -i sense)

readarray gt_epic_mni_dice_files_arr_e2_sense < <(printf '%s\n' ${gt_epic_mni_dice_files_arr_e2[*]} | grep -i sense)
readarray gt_topup_mni_dice_files_arr_e2_sense < <(printf '%s\n' ${gt_topup_mni_dice_files_arr_e2[*]} | grep -i sense)
readarray gt_raw_mni_dice_files_arr_e2_sense < <(printf '%s\n' ${gt_raw_mni_dice_files_arr_e2[*]} | grep -i sense)

# Without SENSE
readarray mni_medians_epic_files_arr_e1_nosense < <(printf '%s\n' ${mni_medians_epic_files_arr_e1[*]} | grep -iv sense)
readarray mni_medians_topup_files_arr_e1_nosense < <(printf '%s\n' ${mni_medians_topup_files_arr_e1[*]} | grep -iv sense)
readarray mni_medians_raw_files_arr_e1_nosense < <(printf '%s\n' ${mni_medians_raw_files_arr_e1[*]} | grep -iv sense)

readarray gt_epic_mni_dice_files_arr_e1_nosense < <(printf '%s\n' ${gt_epic_mni_dice_files_arr_e1[*]} | grep -iv sense)
readarray gt_topup_mni_dice_files_arr_e1_nosense < <(printf '%s\n' ${gt_topup_mni_dice_files_arr_e1[*]} | grep -iv sense)
readarray gt_raw_mni_dice_files_arr_e1_nosense < <(printf '%s\n' ${gt_raw_mni_dice_files_arr_e1[*]} | grep -iv sense)

readarray mni_medians_epic_files_arr_e2_nosense < <(printf '%s\n' ${mni_medians_epic_files_arr_e2[*]} | grep -iv sense)
readarray mni_medians_topup_files_arr_e2_nosense < <(printf '%s\n' ${mni_medians_topup_files_arr_e2[*]} | grep -iv sense)
readarray mni_medians_raw_files_arr_e2_nosense < <(printf '%s\n' ${mni_medians_raw_files_arr_e2[*]} | grep -iv sense)

readarray gt_epic_mni_dice_files_arr_e2_nosense < <(printf '%s\n' ${gt_epic_mni_dice_files_arr_e2[*]} | grep -iv sense)
readarray gt_topup_mni_dice_files_arr_e2_nosense < <(printf '%s\n' ${gt_topup_mni_dice_files_arr_e2[*]} | grep -iv sense)
readarray gt_raw_mni_dice_files_arr_e2_nosense < <(printf '%s\n' ${gt_raw_mni_dice_files_arr_e2[*]} | grep -iv sense)


#for f in ${gt_raw_mni_dice_files_arr_e2_nosense[*]}; do
#    echo $f
#done

echo ${#mni_medians_epic_files_arr_e1_sense[*]}
echo ${#mni_medians_topup_files_arr_e1_sense[*]}
echo ${#mni_medians_raw_files_arr_e1_sense[*]}

echo ${#gt_epic_mni_dice_files_arr_e1_sense[*]}
echo ${#gt_topup_mni_dice_files_arr_e1_sense[*]}
echo ${#gt_raw_mni_dice_files_arr_e1_sense[*]}

echo ${#mni_medians_epic_files_arr_e2_sense[*]}
echo ${#mni_medians_topup_files_arr_e2_sense[*]}
echo ${#mni_medians_raw_files_arr_e2_sense[*]}

echo ${#gt_epic_mni_dice_files_arr_e2_sense[*]}
echo ${#gt_topup_mni_dice_files_arr_e2_sense[*]}
echo ${#gt_raw_mni_dice_files_arr_e2_sense[*]}

echo ${#mni_medians_epic_files_arr_e1_nosense[*]}
echo ${#mni_medians_topup_files_arr_e1_nosense[*]}
echo ${#mni_medians_raw_files_arr_e1_nosense[*]}

echo ${#gt_epic_mni_dice_files_arr_e1_nosense[*]}
echo ${#gt_topup_mni_dice_files_arr_e1_nosense[*]}
echo ${#gt_raw_mni_dice_files_arr_e1_nosense[*]}

echo ${#mni_medians_epic_files_arr_e2_nosense[*]}
echo ${#mni_medians_topup_files_arr_e2_nosense[*]}
echo ${#mni_medians_raw_files_arr_e2_nosense[*]}

echo ${#gt_epic_mni_dice_files_arr_e2_nosense[*]}
echo ${#gt_topup_mni_dice_files_arr_e2_nosense[*]}
echo ${#gt_raw_mni_dice_files_arr_e2_nosense[*]}
