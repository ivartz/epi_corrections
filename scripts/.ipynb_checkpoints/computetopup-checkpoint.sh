# bash computetopup.sh DSC.nii opposite.nii aquisition_parameters_opposite.txt b02b0.cnf topupd 2>&1 | tee computetopup_log.txt
# for instance
# bash /media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections/scripts/computetopup.sh DSC_e2.nii DSC_opposite_e2.nii /media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections/topup_config/aquisition_parameters_opposite.txt /media/loek/HDD3TB1/data/IVS_EPI_BASELINE/epi_corrections/topup_config/b02b0.cnf out2

infile=$1
infile_oppos=$2
param=$3
config=$4
outdir=$5

scriptdir="$(dirname $0)"

# Assuming infile and infile_opposite have the file extension *.nii


# Make output directory if not existing
mkdir_cmd="mkdir -p $outdir"

echo $mkdir_cmd
eval $mkdir_cmd


# Tell FSL to always output uncompressed nifti files
filetype_command="FSLOUTPUTTYPE=NIFTI"

echo $filetype_command
eval $filetype_command


# Extract first temporary window of infile and infile_opposite
output_base_name="$outdir/${infile%.nii}0000"
command="fslroi $infile $output_base_name 0 1"
workfile="${infile%.nii}0000.nii"

echo $command
eval $command

output_base_name="$outdir/${infile_oppos%.nii}0000"
command="fslroi $infile_oppos $output_base_name 0 1"
workfile_oppos="${infile_oppos%.nii}0000.nii"

echo $command
eval $command


# Add duplicate slices to the first temporary window of infile and infile_opposite
bash $scriptdir/add-duplicate-slices.sh $workfile $outdir
workfile="${workfile%.nii}_prep_topup.nii"

bash $scriptdir/add-duplicate-slices.sh $workfile_oppos $outdir
workfile_oppos="${workfile_oppos%.nii}_prep_topup.nii"


# Merge together the volumes with added duplicate slices
merged="$outdir/merged.nii"
command="fslmerge -t $merged $outdir/$workfile $outdir/$workfile_oppos"

echo $command
eval $command


# TOPUP Compute
output_base_name="${merged%.nii}"
out_name="${output_base_name}_generic_out"
fout_name="${output_base_name}_field"
iout_name="${output_base_name}_corrected"

command="topup --imain=$merged --datain=$param --config=$config --out=$out_name --fout=$fout_name --iout=$iout_name"

echo $command
eval $command