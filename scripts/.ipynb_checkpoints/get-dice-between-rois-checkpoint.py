import numpy as np
import nibabel as nib
import argparse

if __name__ == "__main__":
    CLI=argparse.ArgumentParser()
    CLI.add_argument(
      "--rois1",
      help="Nifti file containing the first set of ROIs",
      type=str,
      default="rois1.nii",
    )
    CLI.add_argument(
      "--rois2",
      help="Nifti file containing the second set of ROIs",
      type=str,
      default="rois2.nii",
    )
    args = CLI.parse_args()

    rois1img = nib.load(args.rois1)
    rois2img = nib.load(args.rois2)
    
    rois1values = np.unique(rois1img.get_fdata())
    rois2values = np.unique(rois2img.get_fdata())
    roisvalues = np.intersect1d(rois1values, rois2values)
    [print(roivalue, end=" ") for roivalue in roisvalues]
    print("")
    [print(2 * np.sum((rois1img.get_fdata() == roivalue) & (rois2img.get_fdata() == roivalue))/\
               (np.sum(rois1img.get_fdata() == roivalue) + \
                np.sum(rois2img.get_fdata() == roivalue)), end=" ") for roivalue in roisvalues]
    print("")
    