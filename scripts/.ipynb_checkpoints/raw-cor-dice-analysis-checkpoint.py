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

mniroinames = np.array(['3rd Ventricle', '4th Ventricle', 'Accumbens Area',
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

def read_roi_dice_scores(file):
    with open(file, "r") as f:
        lines = f.readlines()    
    return zip(*[(np.int32(np.float32(lines[0].split(" ")[:-1][i])), np.float32(col)) for i, col in enumerate(lines[1].split(" ")[:-1])])

if __name__ == "__main__":
    CLI=argparse.ArgumentParser()
    CLI.add_argument(
        "--rawdices",
        nargs="*",
        help=".txt files containing DICE scores of between pairs of ground truth and raw DSC ROIs",
        type=str,
        default=["mniroisgtrawdice.txt"],
    )
    CLI.add_argument(
        "--cordices",
        nargs="*",
        help=".txt files containing DICE scores of between pairs of ground truth and corrected DSC ROIs",
        type=str,
        default=["mniroisgtepicdice.txt"],
    )
    args = CLI.parse_args()
    
    assert len(args.rawdices) == len(args.cordices), \
    "Not equal number of rawdice and cordice files passed as argument"
    
    num_sub = len(args.rawdices)
    num_rois = len(mniroivalues)
    
    allrawdicescores, allcordicescores = np.empty((num_rois, num_sub)), \
                                         np.empty((num_rois, num_sub))
    
    allrawdicescores[:], allcordicescores[:] = np.nan, np.nan
    
    for i in range(num_sub):
        
        # Read the files
        rawdicerois, rawdicescores = read_roi_dice_scores(args.rawdices[i])
        cordicerois, cordicescores = read_roi_dice_scores(args.cordices[i])
        
        # Find the common rois
        rois = np.intersect1d(rawdicerois, cordicerois)
        
        # Remove outside of the brain ROI value (0.0) if exists
        if 0 in rois:
            rois = np.delete(rois, np.where(rois == 0))
        
        # Find the common medians and dice scores by
        # using the common rois
        rawdicescores_common = [rawdicescores[idx] for idx in [np.where(rawdicerois == roi)[0][0] for roi in rois]]
        cordicescores_common = [cordicescores[idx] for idx in [np.where(cordicerois == roi)[0][0] for roi in rois]]
        
        assert len(rois) == len(rawdicescores_common) == len(cordicescores_common), \
        "Failed to find common regions for analysis of dice scores"
        
        allrawdicescores[[np.where(mniroivalues == roi)[0][0] for roi in rois], i] = rawdicescores_common
        allcordicescores[[np.where(mniroivalues == roi)[0][0] for roi in rois], i] = cordicescores_common
    
    allrawdicescores_nonan = [roisamples[~np.isnan(roisamples)] for roisamples in allrawdicescores]
    allcordicescores_nonan = [roisamples[~np.isnan(roisamples)] for roisamples in allcordicescores]
    
    wilcoxonresults = np.empty((2, num_rois))
    wilcoxonresults[:] = np.nan
    
    for i in range(num_rois):
        if len(allrawdicescores_nonan[i]) >= 10 and len(allcordicescores_nonan[i]) >= 10:
            wilcoxonresults[:, i] = wilcoxon(allrawdicescores_nonan[i], allcordicescores_nonan[i])
    
    #print("HER")
    #print(wilcoxonresults[1,:])
    
    # How to sort the regions
    # By increaseing p-value
    sortidxbla = np.argsort(wilcoxonresults[1, :])
        
    # Bonferroni correction
    alpha = 0.05
    num_sub_test = len(wilcoxonresults[1, :][~np.isnan(wilcoxonresults[1, :])])
    cutoff = alpha/num_sub_test
    print("Threshold for significant p-value is %f" % cutoff)
    
    # Extract number of significant regions
    topbla = np.argwhere(np.sort(wilcoxonresults[1, :]) < cutoff)[-1][0] + 1
    
    print("Se her!")
    print(topbla)
    print(mniroinames[sortidxbla][:topbla])
    
    top = 72 # 72 or more selects all regions. 71 for TOPUP GE beceause region "vessel" contain only
    # nan . This causes problems.
    #top = 10
    
    # Then sort significant regions by increasing ground truth Dice score
    medianrawdicescores = np.array([np.median(scores) for scores in np.array(allrawdicescores_nonan)])
    sortidx = np.argsort(medianrawdicescores)
    topmedianrawdicescores = medianrawdicescores[sortidx][:top]
    
    # The top regions
    topregions = mniroinames[sortidx][:top]
    print("Number of top regions: %i" % top)
    print("The top regions are: ")
    print(topregions)
    print("Top ground truth Dice scores are: ")
    print(topmedianrawdicescores)
    
    descriptionchoice = 2
    description = ["TOPUP impact on gradient echo DSC Dice", \
                   "TOPUP impact on spin echo DSC Dice", \
                   "EPIC impact on gradient echo DSC Dice", \
                   "EPIC impact on spin echo DSC Dice"]
    
    fig = plt.figure(figsize=[2*6.4, 6*4.8], tight_layout=True)
    
    fig.suptitle(description[descriptionchoice])
    
    gs = gridspec.GridSpec(1, 5)
    
    ax1 = fig.add_subplot(gs[0, 0:3])
    ax2 = fig.add_subplot(gs[0, 3], sharey=ax1)
    ax3 = fig.add_subplot(gs[0, 4], sharey=ax1)
    
    # Making split violin kernel density plot
    # Prepare median values for uncorrected Dice
    topdicedata = np.array(allrawdicescores_nonan)[sortidx][:top]
    topdicedatadf = \
    pd.DataFrame({"Dice" : np.array([pd.Series([sample for sample in samples], dtype=float) for samples in topdicedata])}).explode("Dice")
    topcorrectiontypedf = \
    pd.DataFrame({"Comparison" : np.array([pd.Series(["1. GT vs. uncorrected" for num_samples in range(len(samples))], dtype="category") for samples in topdicedata])}).explode("Comparison")
    topregionsdatadf = \
    pd.DataFrame({"Region" : np.array([pd.Series([region for num_samples in range(len(samples))], dtype="category") for region, samples in zip(topregions, topdicedata)])}).explode("Region")
    d1 = pd.concat((topcorrectiontypedf, topregionsdatadf, topdicedatadf), axis=1).astype({"Comparison" : str, "Region" : str, "Dice" : float})
    
    # --"-- corrected Dice
    topdicedata = np.array(allcordicescores_nonan)[sortidx][:top]
    topdicedatadf = \
    pd.DataFrame({"Dice" : np.array([pd.Series([sample for sample in samples], dtype=float) for samples in topdicedata])}).explode("Dice")
    topcorrectiontypedf = \
    pd.DataFrame({"Comparison" : np.array([pd.Series(["2. GT vs. corrected" for num_samples in range(len(samples))], dtype="category") for samples in topdicedata])}).explode("Comparison")
    topregionsdatadf = \
    pd.DataFrame({"Region" : np.array([pd.Series([region for num_samples in range(len(samples))], dtype="category") for region, samples in zip(topregions, topdicedata)])}).explode("Region")
    d2 = pd.concat((topcorrectiontypedf, topregionsdatadf, topdicedatadf), axis=1).astype({"Comparison" : str, "Region" : str, "Dice" : float})
    
    # Combine dataframes for uncorrected and corrected Dice
    d = pd.concat((d1, d2))
    
    #d_xls = "/run/user/1001/gvfs/smb-share:server=desktop-suc40rk,share=onedrive/work/OUS/distortion_correction/article_figures/dsc-space/topsedice.xlsx"
    
    #d.to_excel(d_xls)
    
    print("START")
    
    print(d1)
    
    print("MIDDLE")
    
    print(d2)
    
    print("HERE")
    
    topmedianrawdicescoressorted = \
    np.array([np.median(scores) for scores in np.array(allrawdicescores_nonan)[sortidx][:top]])
    topmediancordicescoressorted = \
    np.array([np.median(scores) for scores in np.array(allcordicescores_nonan)[sortidx][:top]])
    
    print(topmedianrawdicescoressorted)
    print(topmediancordicescoressorted)
    
    print("A")
    print(topmediancordicescoressorted-topmedianrawdicescoressorted)
    print(np.sum(topmediancordicescoressorted-topmedianrawdicescoressorted))
    
    print("B")
    print(topmedianrawdicescoressorted-topmediancordicescoressorted)
    print(np.sum(topmedianrawdicescoressorted-topmediancordicescoressorted))
    
    print("END")
    
    # Plot Dice
    sns.violinplot(x="Dice",
                   y="Region",
                   hue="Comparison",
                   split=True, 
                   inner="quart",
                   data=d, 
                   ax=ax1)
    
    # Prepare uncorrected Dice scores for box plot
    topdicedata = np.array(allrawdicescores_nonan)[sortidx][:top]
    topregionsdatadf = \
    pd.DataFrame({"Region" : np.array([pd.Series([region for num_samples in range(len(samples))], dtype="category") for region, samples in zip(topregions, topdicedata)])}).explode("Region")
    topdicedatadf = \
    pd.DataFrame({"1" : np.array([pd.Series([sample for sample in samples], dtype=float) for samples in topdicedata])}).explode("1")
    d = pd.concat((topregionsdatadf, topdicedatadf), axis=1).astype({"Region" : str, "Region" : str, "1" : float})
    
    # Plot uncorrected Dice
    #sns.barplot(x=toppvalues,
    #            y=topregions,
    #            ax=ax3)
    #ax3.set_xlabel("Corrected Dice")
    sns.boxplot(x="1", y="Region", data=d, ax=ax2)
    
    plt.setp(ax2.get_yticklabels(), visible=False)
    ax2.set_ylabel("")
    
    # Prepare corrected Dice scores for box plot
    topdicedata = np.array(allcordicescores_nonan)[sortidx][:top]
    topregionsdatadf = \
    pd.DataFrame({"Region" : np.array([pd.Series([region for num_samples in range(len(samples))], dtype="category") for region, samples in zip(topregions, topdicedata)])}).explode("Region")
    topdicedatadf = \
    pd.DataFrame({"2" : np.array([pd.Series([sample for sample in samples], dtype=float) for samples in topdicedata])}).explode("2")
    d = pd.concat((topregionsdatadf, topdicedatadf), axis=1).astype({"Region" : str, "Region" : str, "2" : float})
    
    # Plot corrected Dice scores
    sns.boxplot(x="2", y="Region", data=d, ax=ax3)
    
    plt.setp(ax3.get_yticklabels(), visible=False)
    ax3.set_ylabel("")
    
    # Make some free space for suptitle
    gs.tight_layout(fig, rect=[0, 0, 1, 0.95])
    
    plt.show()
