# bash scripts/clear-docker-output-single-EPI-pair.sh DSC_e2.nii out

target_dyn_file=$1
outdir=$2

# Remaining steps assume that main.py was only run on a single EPI pair

# Rename and copy corrected dynamic file, field (Hz) and TOPUP output
# for re-use with applytopup (--topup https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/topup/ApplyTopupUsersGuide)
target_corrected_dyn_file=$(ls $outdir/EPI_applytopup/*applytopup* | head -n 1)

target_dyn_file_woe=${target_dyn_file%.nii}

mv_cmd="mv -v $target_corrected_dyn_file $outdir/${target_dyn_file_woe}_corrected.nii"
echo $mv_cmd
eval $mv_cmd

field_hz_file=$(ls $outdir/EPI_applytopup/*field* | head -n 1)

mv_cmd="mv -v $field_hz_file $outdir/field_hz.nii"
echo $mv_cmd
eval $mv_cmd

readarray topup_results_arr < <(ls $outdir/TOPUP/*/*/*generic_out*)

for res in ${topup_results_arr[*]}; do
    mv_cmd="mv -v $res $outdir"
    echo $mv_cmd
    eval $mv_cmd
done

mv_cmd="mv -v $outdir/$(ls $outdir | grep fieldcoef | head -n 1) $outdir/generic_out_fieldcoef.nii"
echo $mv_cmd
eval $mv_cmd

mv_cmd="mv -v $outdir/$(ls $outdir | grep movpar | head -n 1) $outdir/generic_out_movpar.txt"
echo $mv_cmd
eval $mv_cmd

# Clean up
rm_cmd="rm -rd $outdir/EPI"
echo $rm_cmd
eval $rm_cmd

rm_cmd="rm -rd $outdir/EPI_applytopup"
echo $rm_cmd
eval $rm_cmd

rm_cmd="rm -rd $outdir/TOPUP"
echo $rm_cmd
eval $rm_cmd
