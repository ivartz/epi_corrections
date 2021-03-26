: '
bash computetopup.sh dynamic.nii dymamic_opposite.nii aquisition_parameters.txt b02b0.cnf topup-corrected
'

infile=$1
infile_oppos=$2
param=$3
config=$4
outdir=$5

scriptdir=$(dirname $0)

# Assuming infile and infile_opposite have the file extension *.nii

# Make output directory if not existing
mkdir_cmd="mkdir -p $outdir"

echo $mkdir_cmd
eval $mkdir_cmd


# Tell FSL to always output uncompressed nifti files
filetype_command="FSLOUTPUTTYPE=NIFTI"

echo $filetype_command
eval $filetype_command

# Extract file names
infile_name=$(basename $infile)
infile_oppos_name=$(basename $infile_oppos)

# Extract first temporary window of infile and infile_opposite
output_base_name=$outdir/${infile_name%.nii}0000
command="fslroi $infile $output_base_name 0 1"
workfile=${infile_name%.nii}0000.nii

echo $command
eval $command

output_base_name=$outdir/${infile_oppos_name%.nii}0000
command="fslroi $infile_oppos $output_base_name 0 1"
workfile_oppos=${infile_oppos_name%.nii}0000.nii

echo $command
eval $command

# Add duplicate slices to the first temporary window of infile and infile_opposite
bash $scriptdir/add-duplicate-slices.sh $workfile $outdir
workfile=${workfile%.nii}_prep_topup.nii

bash $scriptdir/add-duplicate-slices.sh $workfile_oppos $outdir
workfile_oppos=${workfile_oppos%.nii}_prep_topup.nii


# Merge together the volumes with added duplicate slices
merged=$outdir/merged.nii
command="fslmerge -t $merged $outdir/$workfile $outdir/$workfile_oppos"

echo $command
eval $command


# TOPUP Compute
out_name=$(dirname $merged)/generic_out
fout_name=$(dirname $merged)/field

command="topup --imain=$merged --datain=$param --config=$config --out=$out_name --fout=$fout_name"

echo $command
eval $command

# Clean up
rm_command="rm -v $outdir/${infile_name%.nii}0000.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/${infile_oppos_name%.nii}0000.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/$workfile"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/$workfile_oppos"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/${infile_name%.nii}0000_zmax.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/${infile_name%.nii}0000_zmin.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/${infile_oppos_name%.nii}0000_zmax.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $outdir/${infile_oppos_name%.nii}0000_zmin.nii"
echo $rm_command
eval $rm_command

rm_command="rm -v $merged"
echo $rm_command
eval $rm_command
