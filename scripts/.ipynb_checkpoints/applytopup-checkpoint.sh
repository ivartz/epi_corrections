# bash applytopup.sh rois_e1.nii topupd/generic_out aquisition_parameters_opposite.txt topupd/rois_e1.nii 2>&1 | tee applytopup_log.txt

infile=$1
topupresults=$2
param=$3
outfile=$4

# Assuming infile has the file extension *.nii

startdir=$(pwd)
scriptdir="$(dirname $0)"

filetype_command="FSLOUTPUTTYPE=NIFTI"

echo $filetype_command
eval $filetype_command

infilenamewe=$(basename $infile)

infilename=${infilenamewe%.nii}

outdir=$(dirname $outfile)

outfilewe=$(basename $outfile)

workfilenamewe="raw_$infilenamewe"

workfilenamewoe=${workfilenamewe%.nii}

cp_command="cp -v $infile $outdir/$workfilenamewe"

echo $cp_command
eval $cp_command

bash $scriptdir/add-duplicate-slices.sh $workfilenamewe $outdir
: '
# Add duplicate top and bottom z slice

output_base="raw_$infilename"
output_zmin="${output_base}_zmin"
output_zmax="${output_base}_zmax"
output_prep="${output_base}_prep_topup"

cd_command="cd $outdir"

echo $cd_command
eval $cd_command

xdim_command="xdim=$(fslval $workfilenamewoe dim1)"
ydim_command="ydim=$(fslval $workfilenamewoe dim2)"
zdim_command="zdim=$(fslval $workfilenamewoe dim3)"

echo $xdim_command
eval $xdim_command
echo $ydim_command
eval $ydim_command
echo $zdim_command
eval $zdim_command

output_zmin_command="fslroi $workfilenamewoe \
                            $output_zmin \
                            0 $xdim \
                            0 $ydim \
                            0 1"
echo $output_zmin_command
eval $output_zmin_command

output_zmax_command="fslroi $workfilenamewoe \
                            $output_zmax \
                            0 $xdim \
                            0 $ydim \
                            $((zdim-1)) 1"
echo $output_zmax_command
eval $output_zmax_command

output_prep_command="fslmerge -z $output_prep \
                                 $output_zmin \
                                 $workfilenamewoe \
                                 $output_zmax"
echo $output_prep_command
eval $output_prep_command
'

# Apply field (topup results)

topupresultsfilebasename=$(basename $topupresults)

outfilenamewoe="${output_prep}_applytopup"

topup_command="applytopup \
               --imain=$output_prep \
               --inindex=1 \
               --datain=$param \
               --topup=$topupresultsfilebasename \
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

cpgeom_command="fslcpgeom $infile $outdir/$outfilenamepostpwoe.nii"

echo $cpgeom_command
eval $cpgeom_command

# Rename final output file

mv_command="mv -v $outdir/$outfilenamepostpwoe.nii $outfile"

echo $mv_command
eval $mv_command

# Clean up

rm_command="rm -v $outdir/$outfilenamewoe.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/$output_prep.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/$output_zmax.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/$output_zmin.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/$output_base.nii"
echo $rm_command
eval $rm_command

