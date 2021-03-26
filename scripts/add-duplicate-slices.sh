: '
bash add-duplicate-slices.sh workfile outdir
'

workfile=$1
outdir=$2

# Add duplicate top and bottom z slice
output_base=${workfile%.nii}
output_zmin=${output_base}_zmin
output_zmax=${output_base}_zmax
output_prep=${output_base}_prep_topup

cd_command="cd $outdir"

echo $cd_command
eval $cd_command

xdim_command="xdim=$(fslval $workfile dim1)"
ydim_command="ydim=$(fslval $workfile dim2)"
zdim_command="zdim=$(fslval $workfile dim3)"

echo $xdim_command
eval $xdim_command
echo $ydim_command
eval $ydim_command
echo $zdim_command
eval $zdim_command

output_zmin_command="fslroi $workfile \
                            $output_zmin \
                            0 $xdim \
                            0 $ydim \
                            0 1"
echo $output_zmin_command
eval $output_zmin_command

output_zmax_command="fslroi $workfile \
                            $output_zmax \
                            0 $xdim \
                            0 $ydim \
                            $((zdim-1)) 1"
echo $output_zmax_command
eval $output_zmax_command

output_prep_command="fslmerge -z $output_prep \
                                 $output_zmin \
                                 $output_base \
                                 $output_zmax"
echo $output_prep_command
eval $output_prep_command
