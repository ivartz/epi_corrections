#!/bin/bash

OHDirectory="/cygdrive/e/temp/ONCOhabitats_GBM_analysis_modified_pipeline"
OHANTsDirectory="/cygdrive/f/OneDrive/work/OUS/distortion_correction/ONCOhabitats_scripts/ANTs"
inputFilePath="native/Segmentation.nii.gz"
referencePath="native/Flair.nii.gz"
transformations="transforms/transform_Flair_to_T1c_0GenericAffine.mat"
outputFilePath="native/Segmentation_Flair_space.nii.gz"

readarray results_dirs < <(ls -d $OHDirectory/*/results)

#echo ${results_dirs[@]}

applyInverseRegistrationDiscrete () {
OHANTsDirectory=$1
results_dir=$2
inputFilePath=$3
referencePath=$4
transformations=$5
outputFilePath=$6

cd $results_dir

#echo $(pwd)

# Apply transform
command_transform="$OHANTsDirectory/antsApplyTransforms.exe --dimensionality 3 --input $inputFilePath --reference-image $referencePath --output $outputFilePath --interpolation MultiLabel[0.3,0] --transform [$transformations, 1] --verbose 0"
echo $command_transform
eval $command_transform

# Convert to uint8
command_convert="$OHANTsDirectory/ConvertImage.exe 3 $outputFilePath $outputFilePath 1"
echo $command_convert
eval $command_convert
}


#printf "%s\n" "${results_dirs[@]}" | xargs -I dir -n 1 -P $(nproc) bash -c 'echo $1' _ dir

export -f applyInverseRegistrationDiscrete

printf "%s\n" "${results_dirs[@]}" | xargs -I results_dir -n 1 -P $(nproc) bash -c 'applyInverseRegistrationDiscrete "$@"' _ $OHANTsDirectory results_dir $inputFilePath $referencePath $transformations $outputFilePath

