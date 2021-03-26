: '
bash applytopup.sh dynamic.nii topup-results/generic_out aquisition_parameters.txt dynamic_corrected.nii
'

infile=$1
topupresults=$2
param=$3
outfile=$4

# Assuming infile has the file extension *.nii
startdir=$(pwd)
scriptdir=$(dirname $0)

filetype_command="FSLOUTPUTTYPE=NIFTI"

echo $filetype_command
eval $filetype_command

infilenamewe=$(basename $infile)

infilename=${infilenamewe%.nii}

outdir=$(dirname $outfile)

outfilewe=$(basename $outfile)

workfilenamewe=raw_$infilenamewe

workfilenamewoe=${workfilenamewe%.nii}

# Make a copy of infile to work with
cp_command="cp -v $infile $outdir/$workfilenamewe"

echo $cp_command
eval $cp_command

bash $scriptdir/add-duplicate-slices.sh $workfilenamewe $outdir

# Apply field (topup results)
output_prep=$outdir/${workfilenamewoe}_prep_topup

outfilenamewoe=${output_prep}_applytopup

topup_command="applytopup \
               --imain=$output_prep \
               --inindex=1 \
               --datain=$param \
               --topup=$topupresults \
               --out=$outfilenamewoe \
               --interp=trilinear \
               --method=jac"

# --interp=spline on the earlier DSC files

echo $topup_command
eval $topup_command

# Remove duplicate top and bottom z slice
xdim_command="xdim=$(fslval $outfilenamewoe dim1)"
ydim_command="ydim=$(fslval $outfilenamewoe dim2)"
zdim_command="zdim=$(fslval $outfilenamewoe dim3)"

echo $xdim_command
eval $xdim_command
echo $ydim_command
eval $ydim_command
echo $zdim_command
eval $zdim_command

outfilenamepostpwoe=${outfilenamewoe}_postp

output_postp_command="fslroi $outfilenamewoe \
                             $outfilenamepostpwoe \
                             0 $xdim \
                             0 $ydim \
                             1 $((zdim-2))"

echo $output_postp_command
eval $output_postp_command

# cd back to the original directory so that arguments are valid
cd_command="cd $startdir"

echo $cd_command
eval $cd_command

# Replace header of output file with header of input file
#cpgeom_command="fslcpgeom $infile $outfilenamepostpwoe.nii"

echo $cpgeom_command
eval $cpgeom_command

# Rename final output file
mv_command="mv -v $outfilenamepostpwoe.nii $outfile"

echo $mv_command
eval $mv_command

output_zmax=$outdir/${workfilenamewoe}_zmax.nii
output_zmin=$outdir/${workfilenamewoe}_zmin.nii
output_base=$outdir/$workfilenamewe

# Clean up
rm_command="rm -v $outfilenamewoe.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $output_prep.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $output_zmax"
echo $rm_command
eval $rm_command

rm_command="rm -v $output_zmin"
echo $rm_command
eval $rm_command

rm_command="rm -v $output_base"
echo $rm_command
eval $rm_command
