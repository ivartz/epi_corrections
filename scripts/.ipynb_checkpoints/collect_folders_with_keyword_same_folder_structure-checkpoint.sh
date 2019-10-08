#!/bin/bash

# RUN
# collect_folders_with_keyword_same_folder_structure.sh <dicom_input_folder> <dicom_output_folder> <directory_keyword>

# Collects .dcm files in all subfolders of dicom_input_folder 
# with file name containing directory_keyword and saves in 
# with same folder structure in dicom_input_folder .

dicom_input_folder=$1

dicom_output_folder=$2

# Select only subfolders inside dicom_input_folder
# containing following keyword/string.
directory_keyword=$3

delete_pre_existing_destination_folders=false

# Create empty array to fill inn matched dicom folders w. filepath
# that contain .dcm files to be converted to .nii files (input directories).
directories_to_convert_array=()

# Store input directories to bash array directories_to_convert_array
while IFS=  read -r -d $'\0'; do
    directories_to_copy_array+=("$REPLY")
done < <(find $dicom_input_folder -type d -iname "*$directory_keyword*" -print0)

# Iterate over input directories
for i in "${!directories_to_copy_array[@]}"; do

    echo "---- iteration $i ----"

    input_folder=${directories_to_copy_array[i]}

    echo "input folder $i: $input_folder"

    output_folder="$dicom_output_folder${input_folder#$dicom_input_folder}"

    echo "output folder $i: $output_folder"    

    if [ -d "$output_folder" ]; then
        echo "output folder $i already exists"

        if [ ! $delete_pre_existing_destination_folders = true ]; then
            echo "delete_pre_existing_destination_folders is set to false"
            echo "not deleting pre-existing files"
            echo "assuming already converted files"
            echo "skipping copy"
            continue
        fi
        
        echo "delete_pre_existing_destination_folders is set to true"
        echo "deleting pre-existing output folder"
        rm -rd "$output_folder"        
    fi  

    echo "output folder $i doesn't exist, creating"
    mkdir -p "$output_folder"

    # Here is the copy command
    #command="dcm2nii -4 y -d y -e y -g n -m n -n y -o '$output_folder' -p y -r y -v y '$input_folder'"
    command="cp -av '$input_folder' '$output_folder'"

    echo "copying DICOM files in input folder number $i to DICOM files in output folder number $i with the command:"

    echo $command

    # Run the conversion command
    eval $command

done

