import numpy as np
import nibabel as nib
import argparse

if __name__ == "__main__":
    CLI=argparse.ArgumentParser()
    CLI.add_argument(
      "--datanifti",
      help="The nifti file containing the data we want to extract median values from, based on roinifti",
      type=str,
      default="rcbv.nii",
    )
    CLI.add_argument(
      "--roinifti",
      help="The nifti file containing ROIs",
      type=str,
      default="rcbv.nii",
    )
    args = CLI.parse_args()

    dataimg = nib.load(args.datanifti)
    roiimg = nib.load(args.roinifti)
    
    roivalues = np.unique(roiimg.get_fdata())
    [print(roivalue, end=" ") for roivalue in roivalues]
    print("")
    [print(np.median(dataimg.get_fdata()[roiimg.get_fdata() == roivalue]), end=" ") if np.sum(dataimg.get_fdata()[roiimg.get_fdata() == roivalue] != 0)/np.sum(roiimg.get_fdata() == roivalue) >= 0.7 else print("Excluded", end=" ") for roivalue in roivalues]
    print("")
    