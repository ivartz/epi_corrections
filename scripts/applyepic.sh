# bash applyepic.sh rois_e1.nii epicd/field.nii /media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections/epic_src epicd/rois_e1.nii 2>&1 | tee applytopup_log.txt

infile=$1
displacementfile=$2
epic_src=$3
outfile=$4

source_command="source $epic_src/SetUpEpic.sh ''" # '' to avoid passing the same arguments into source

echo $source_command
eval $source_command

infilenamewe=$(basename $infile)

outdir=$(dirname $outfile)

infile_conv=$outdir/raw_${infilenamewe%.nii}.mgz

conv_command="mri_convert $infile $infile_conv"

echo $conv_command
eval $conv_command

displacementfile_conv=${displacementfile%.nii}.mgz

conv_command="mri_convert $displacementfile $displacementfile_conv"

echo $conv_command
eval $conv_command

outfilenamewe=$(basename $outfile)

outfilename=${outfilenamewe%.nii}

epic_command="$epic_src/bin/applyEpic \
             -r $infile_conv \
             -d $displacementfile_conv \
             -ro $outfilename.mgz \
             -od $outdir"

echo $epic_command
eval $epic_command

conv_command="mri_convert $outdir/$outfilename.mgz $outfile"

echo $conv_command
eval $conv_command

rm_command="rm -v $outdir/$outfilename.mgz"
echo $rm_command
eval $rm_command

rm_command="rm -v $infile_conv"
echo $rm_command
eval $rm_command

rm_command="rm -v $displacementfile_conv"
echo $rm_command
eval $rm_command

