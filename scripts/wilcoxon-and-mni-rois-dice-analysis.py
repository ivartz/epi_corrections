import numpy as np
import argparse
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import wilcoxon
import seaborn as sns
import pandas as pd
import sys

mniroivalues = np.array([ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11., 12., 13.,
       14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25., 26.,
       27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39.,
       40., 41., 42., 43., 44., 45., 46., 47., 48., 49., 50., 51., 52.,
       53., 54., 55., 56., 57., 58., 59., 60., 61., 62., 63., 64., 65.,
       66., 67., 68., 69., 70., 71., 72.])

mniroivalues = np.array([np.int32(v) for v in mniroivalues])

mniroinames = np.array(['3rd Ventricle', '4th Ventricle', 'Left & right Accumbens Area',
       'Amygdala', 'Brain Stem', 'Caudate',
       'Cerebellum Exterior',
       'Cerebellum White Matter',
       'Cerebral White Matter', 'Cerebrospinal Fluid',
       'Hippocampus', 'Inferior Lateral Ventricle',
       'Lateral Ventricle', 'Pallidum',
       'Putamen', 'Thalamus Proper',
       'Ventral Diencephalon (DC)', 'Vessel', 'Optic Chiasm',
       'Cerebellar Vermal Lobules I-V',
       'Cerebellar Vermal Lobules VI-VII',
       'Cerebellar Vermal Lobules VIII-X', 'Basal Forebrain',
       'Anterior cingulate gyrus',
       'Anterior insula',
       'Anterior orbital gyrus',
       'Angular gyrus',
       'Calcarine cortex',
       'Central operculum', 'Cuneus',
       'Entorhinal area',
       'Frontal operculum',
       'Frontal pole', 'Fusiform gyrus',
       'Gyrus rectus',
       'Inferior occipital gyrus',
       'Inferior temporal gyrus',
       'Lingual gyrus',
       'Lateral orbital gyrus',
       'Middle cingulate gyrus',
       'Medial frontal cortex',
       'Middle frontal gyrus',
       'Middle occipital gyrus',
       'Medial orbital gyrus',
       'Postcentral gyrus medial segment',
       'Precentral gyrus medial segment',
       'Superior frontal gyrus medial segment',
       'Middle temporal gyrus',
       'Occipital pole',
       'Occipital fusiform gyrus',
       'Opercular part of the inferior frontal gyrus',
       'Obital part of the inferior frontal gyrus',
       'Posterior cingulate gyrus',
       'Precuneus',
       'Parahippocampal gyrus',
       'Posterior insula',
       'Parietal operculum',
       'Postcentral gyrus',
       'Posterior orbital gyrus',
       'Planum polare',
       'Precentral gyrus',
       'Planum temporale',
       'Subcallosal area',
       'Superior frontal gyrus',
       'Supplementary motor cortex',
       'Supramarginal gyrus',
       'Superior occipital gyrus',
       'Superior parietal lobule',
       'Superior temporal gyrus',
       'Temporal pole',
       'Triangular part of the inferior frontal gyrus',
       'Transverse temporal gyrus'])

#mniroinames = np.array([np.str(v) for v in mniroinames])

def read_roi_medians(file):
    with open(file, "r") as f:
        lines = f.readlines()    
    return zip(*[(np.int32(np.float32(lines[0].split(" ")[:-1][i])), np.float32(col)) for i, col in enumerate(lines[1].split(" ")[:-1]) if col != "Excluded"])

def read_roi_dice_scores(file):
    with open(file, "r") as f:
        lines = f.readlines()    
    return zip(*[(np.int32(np.float32(lines[0].split(" ")[:-1][i])), np.float32(col)) for i, col in enumerate(lines[1].split(" ")[:-1])])

if __name__ == "__main__":
    CLI=argparse.ArgumentParser()
    CLI.add_argument(
        "--rawmedians",
        nargs="*",
        help=".txt files containing rCBV medians of uncorrected rCBV files",
        type=str,
        default=["mniroismedians.txt"],
    )
    CLI.add_argument(
        "--cormedians",
        nargs="*",
        help=".txt files containing rCBV medians of corrected rCBV files",
        type=str,
        default=["mniroismedians.txt"],
    )
    CLI.add_argument(
        "--dicescores",
        nargs="*",
        help=".txt files containing DICE scores of between pairs of ROIs based on raw and corrected rCBV",
        type=str,
        default=["mniroisrawcordice.txt"],
    )
    args = CLI.parse_args()
    
    assert len(args.rawmedians) == len(args.cormedians) == len(args.dicescores), \
    "Not equal number of rawmedians, cormedians and dicescores files passed as argument"
    
    num_sub = len(args.rawmedians)
    num_rois = len(mniroivalues)
    
    allrawmedians, allcormedians, alldicescores = np.empty((num_rois, num_sub)), \
                                                  np.empty((num_rois, num_sub)), \
                                                  np.empty((num_rois, num_sub))
    #allrawmedians, allcormedians, alldicescores = np.empty((num_sub, num_rois)), \
    #                                              np.empty((num_sub, num_rois)), \
    #                                              np.empty((num_sub, num_rois))
    allrawmedians[:], allcormedians[:], alldicescores[:] = np.nan, np.nan, np.nan
    
    for i in range(num_sub):
        
        # Read the files
        rawrois, rawmedians = read_roi_medians(args.rawmedians[i])
        corrois, cormedians = read_roi_medians(args.cormedians[i])
        dicerois, dicescores = read_roi_dice_scores(args.dicescores[i])
        
        # Find the common rois
        rois = np.intersect1d(rawrois, corrois)
        rois = np.intersect1d(rois, dicerois)
        
        # Find the common medians and dice scores by
        # using the common rois
        rawmedians_common = [rawmedians[idx] for idx in [np.where(rawrois == roi)[0][0] for roi in rois]]
        cormedians_common = [cormedians[idx] for idx in [np.where(corrois == roi)[0][0] for roi in rois]]
        dicescores_common = [dicescores[idx] for idx in [np.where(dicerois == roi)[0][0] for roi in rois]]
        
        assert len(rois) == len(rawmedians_common) == len(cormedians_common) == len(dicescores_common), \
        "Failed to find common regions for analysis of medians and dice scores"
        
        allrawmedians[[np.where(mniroivalues == roi)[0][0] for roi in rois], i] = rawmedians_common
        allcormedians[[np.where(mniroivalues == roi)[0][0] for roi in rois], i] = cormedians_common
        alldicescores[[np.where(mniroivalues == roi)[0][0] for roi in rois], i] = dicescores_common
    
        #allrawmedians[i, [np.where(mniroivalues == roi)[0][0] for roi in rois]] = rawmedians_common
        #allcormedians[i, [np.where(mniroivalues == roi)[0][0] for roi in rois]] = cormedians_common
        #alldicescores[i, [np.where(mniroivalues == roi)[0][0] for roi in rois]] = dicescores_common
    
    
    allrawmedians_nonan = [roisamples[~np.isnan(roisamples)] for roisamples in allrawmedians]
    allcormedians_nonan = [roisamples[~np.isnan(roisamples)] for roisamples in allcormedians]
    alldicescores_nonan = [roisamples[~np.isnan(roisamples)] for roisamples in alldicescores]
    
    wilcoxonresults = np.empty((2, num_rois))
    wilcoxonresults[:] = np.nan
    
    for i in range(num_rois):
        if len(allrawmedians_nonan[i]) >= 10 and len(allcormedians_nonan[i]) >= 10:
            wilcoxonresults[:, i] = wilcoxon(allrawmedians_nonan[i], allcormedians_nonan[i])
    
    # How to sort the regions
    # By increaseing p-value
    sortidx = np.argsort(wilcoxonresults[1, :])#[::-1]
    # By increasing dice score
    #sortidx = np.argsort([np.median(s) for s in alldicescores_nonan])#[::-1]
        
    # Bonferroni correction
    alpha = 0.05
    num_sub_test = len(wilcoxonresults[1, :][~np.isnan(wilcoxonresults[1, :])])
    cutoff = alpha/num_sub_test
    print("Threshold for significant p-value is %f" % cutoff)
    
    # Extract number of significant regions
    top = np.argwhere(np.sort(wilcoxonresults[1, :]) < cutoff)[-1][0] + 1
    #top = 66
    
    # Then sort significant regions by increasing dice score
    topmediandicescores = np.array([np.median(scores) for scores in np.array(alldicescores_nonan)[sortidx][:top]])
    sortidx2 = np.argsort(topmediandicescores)
    
    # The significant regions
    topregions = mniroinames[sortidx][:top][sortidx2]
    print("Number of significant regions: %i" % top)
    print("The significant regions are: ")
    print(topregions)
    toppvalues = wilcoxonresults[1, :][sortidx][:top][sortidx2]
    print("p-values are: ")
    print(toppvalues)
    #topmediandicescores = np.array([np.median(scores) for scores in np.array(alldicescores_nonan)[sortidx][:top]])
    print("Median dice scores are: ")
    print(topmediandicescores)
    
    descriptionchoice = 3
    description = ["TOPUP impact on gradient echo DSC rCBV", \
                   "TOPUP impact on spin echo DSC rCBV", \
                   "EPIC impact on gradient echo DSC rCBV", \
                   "EPIC impact on spin echo DSC rCBV"]
    
    fig = plt.figure(figsize=[2*6.4, 4.8], tight_layout=True)
    
    fig.suptitle(description[descriptionchoice] + " (p < " + "{:.4f}".format(cutoff) + ")")
    
    gs = gridspec.GridSpec(1, 5)
    
    ax1 = fig.add_subplot(gs[0, 0:3])
    ax2 = fig.add_subplot(gs[0, 3], sharey=ax1)
    ax3 = fig.add_subplot(gs[0, 4], sharey=ax1)
    
    # Making split violin kernel density plot
    # Prepare median values for uncorrected rCBV
    topmediandata = np.array(allrawmedians_nonan)[sortidx][:top][sortidx2]
    topmediandatadf = \
    pd.DataFrame({"Median rCBV" : np.array([pd.Series([sample for sample in samples], dtype=float) for samples in topmediandata])}).explode("Median rCBV")
    topcorrectiontypedf = \
    pd.DataFrame({"Correction" : np.array([pd.Series(["Uncorrected" for num_samples in range(len(samples))], dtype="category") for samples in topmediandata])}).explode("Correction")
    topregionsdatadf = \
    pd.DataFrame({"Region" : np.array([pd.Series([region for num_samples in range(len(samples))], dtype="category") for region, samples in zip(topregions, topmediandata)])}).explode("Region")
    d1 = pd.concat((topcorrectiontypedf, topregionsdatadf, topmediandatadf), axis=1).astype({"Correction" : str, "Region" : str, "Median rCBV" : float})
    
    # --"-- corrected rCBV
    topmediandata = np.array(allcormedians_nonan)[sortidx][:top][sortidx2]
    topmediandatadf = \
    pd.DataFrame({"Median rCBV" : np.array([pd.Series([sample for sample in samples], dtype=float) for samples in topmediandata])}).explode("Median rCBV")
    topcorrectiontypedf = \
    pd.DataFrame({"Correction" : np.array([pd.Series(["Corrected" for num_samples in range(len(samples))], dtype="category") for samples in topmediandata])}).explode("Correction")
    topregionsdatadf = \
    pd.DataFrame({"Region" : np.array([pd.Series([region for num_samples in range(len(samples))], dtype="category") for region, samples in zip(topregions, topmediandata)])}).explode("Region")
    d2 = pd.concat((topcorrectiontypedf, topregionsdatadf, topmediandatadf), axis=1).astype({"Correction" : str, "Region" : str, "Median rCBV" : float})
    
    # Combine dataframes for uncorrected and corrected median rCBV
    d = pd.concat((d1, d2))
    
    # Plot rCBV
    sns.violinplot(x="Median rCBV",
                   y="Region",
                   hue="Correction",
                   split=True, 
                   inner="quart",
                   data=d, 
                   ax=ax1)
    
    # Plot p-values
    sns.barplot(x=toppvalues,
                y=topregions,
                ax=ax3)
        
    ax3.set_xlabel("Wilcoxon p-value")
    
    plt.setp(ax3.get_yticklabels(), visible=False)
    
    # Prepare Dice scores for swarm plot
    topdicedata = np.array(alldicescores_nonan)[sortidx][:top][sortidx2]
    topregionsdatadf = \
    pd.DataFrame({"Region" : np.array([pd.Series([region for num_samples in range(len(samples))], dtype="category") for region, samples in zip(topregions, topdicedata)])}).explode("Region")
    topdicedatadf = \
    pd.DataFrame({"Dice score" : np.array([pd.Series([sample for sample in samples], dtype=float) for samples in topdicedata])}).explode("Dice score")
    d = pd.concat((topregionsdatadf, topdicedatadf), axis=1).astype({"Region" : str, "Region" : str, "Dice score" : float})
    
    # Plot Dice scores
    sns.swarmplot(x="Dice score", y="Region", data=d, ax=ax2)
    
    plt.setp(ax2.get_yticklabels(), visible=False)
    ax2.set_ylabel("")
    
    # Make some free space for suptitle
    gs.tight_layout(fig, rect=[0, 0, 1, 0.95])
    
    plt.show()