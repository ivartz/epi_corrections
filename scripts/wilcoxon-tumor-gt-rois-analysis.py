import argparse
import numpy as np
from scipy.stats import wilcoxon

tumorroivalues = np.array([ 0,  1,  2,  3], dtype=np.int32)

tumorroinames = np.array(['Non-tumor', 'Necrotic', 'Edema', 'Enhancing'])

def read_roi_medians(file):
    with open(file, "r") as f:
        lines = f.readlines()    
    return zip(*[(np.int32(np.float32(lines[0].split(" ")[:-1][i])), np.float32(col)) for i, col in enumerate(lines[1].split(" ")[:-1]) if col != "Excluded"])

if __name__ == "__main__":
    CLI=argparse.ArgumentParser()
    CLI.add_argument(
        "--rawmedians",
        nargs="*",
        help=".txt files containing rCBV medians of uncorrected rCBV files",
        type=str,
        default=["tumorroismedians.txt"],
    )
    CLI.add_argument(
        "--cormedians",
        nargs="*",
        help=".txt files containing rCBV medians of corrected rCBV files",
        type=str,
        default=["tumorroismedians.txt"],
    )
    args = CLI.parse_args()
    
    num_sub = len(args.rawmedians)
    num_rois = len(tumorroivalues)
    
    # numpy array of nan to store all median raw (uncorrected)
    # and corrected (epic or topup) values
    allrawmedians, allcormedians = np.empty((num_rois, num_sub)), \
                                   np.empty((num_rois, num_sub))
    allrawmedians[:], allcormedians[:] = np.nan, np.nan
    
    for i in range(num_sub):
        
        # Read the files
        res = read_roi_medians(args.rawmedians[i])
        if any(True for _ in res):
            rawrois, rawmedians = read_roi_medians(args.rawmedians[i])
        res = read_roi_medians(args.cormedians[i])
        if any(True for _ in res):
            corrois, cormedians = read_roi_medians(args.cormedians[i])
        
        # Find the common rois
        rois = np.intersect1d(rawrois, corrois)
        
        # Find the common medians by
        # using the common rois
        rawmedians_common = [rawmedians[idx] for idx in [np.where(rawrois == roi)[0][0] for roi in rois]]
        cormedians_common = [cormedians[idx] for idx in [np.where(corrois == roi)[0][0] for roi in rois]]
        
        assert len(rois) == len(rawmedians_common) == len(cormedians_common), \
        "Failed to find common regions for analysis of medians and dice scores"
        
        # Store the medians in the numpy array
        allrawmedians[[np.where(tumorroivalues == roi)[0][0] for roi in rois], i] = rawmedians_common
        allcormedians[[np.where(tumorroivalues == roi)[0][0] for roi in rois], i] = cormedians_common
    
    # Remove nan
    allrawmedians_nonan = [roisamples[~np.isnan(roisamples)] for roisamples in allrawmedians]
    allcormedians_nonan = [roisamples[~np.isnan(roisamples)] for roisamples in allcormedians]

    # numpy array to store Wilcoxon results
    wilcoxonresults = np.empty((2, num_rois))
    wilcoxonresults[:] = np.nan
    
    # Perform the Wilcoxon test on each roi (Necrotic, Enhancing and Edema) if at least 10 samples available
    for i in range(num_rois):
        if len(allrawmedians_nonan[i]) >= 10 and len(allcormedians_nonan[i]) >= 10:
            print(tumorroinames[i])
            print("Raw median")
            rmed = np.median(allrawmedians_nonan[i])
            print(rmed)
            print("Corrected median")
            cmed = np.median(allcormedians_nonan[i])
            print(cmed)
            print("Corrected-Raw median")
            crmeddiff = cmed-rmed
            print(crmeddiff)
            wilcoxonresults[:, i] = wilcoxon(allrawmedians_nonan[i], allcormedians_nonan[i])
    
    # How to sort the regions
    # By increaseing p-value
    sortidx = np.argsort(wilcoxonresults[1, :])#[::-1]
    
    # Bonferroni correction
    alpha = 0.05
    num_sub_test = len(wilcoxonresults[1, :][~np.isnan(wilcoxonresults[1, :])])
    cutoff = alpha/num_sub_test
    print("Threshold for significant p-value is %f" % cutoff)
    
    # Extract number of significant regions
    top = np.argwhere(np.sort(wilcoxonresults[1, :]) < cutoff)[-1][0] + 1
    
    # The significant regions
    topregions = tumorroinames[sortidx][:top]
    print("Number of significant regions: %i" % top)
    print("The significant regions are: ")
    print(topregions)
    toppvalues = wilcoxonresults[1, :][sortidx][:top]
    print("p-values are: ")
    print(toppvalues)
    statistic = wilcoxonresults[0, :][sortidx][:top]
    print("wilcoxon statistics: ")
    print(statistic)
