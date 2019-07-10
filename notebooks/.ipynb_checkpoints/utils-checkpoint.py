import os
import shutil
import numpy as np
import nibabel as nib
import pandas as pd
from pathlib import Path
# Library for loading Matlab .mat files.
from scipy.io import loadmat
from scipy.spatial.distance import euclidean
from scipy.stats import wasserstein_distance

def load_mat_files(CBV_out_dir):
    
    # Loading CBV ROI histograms.
    region_values = loadmat(CBV_out_dir + "/" + "region_values.mat")["region_values"]
    hist_edges = loadmat(CBV_out_dir + "/" + "hist_edges.mat")["hist_edges"]

    raw_e1_CBV_region_histograms = \
    loadmat(CBV_out_dir + "/" + "raw_e1_CBV_region_histograms.mat")["raw_e1_CBV_region_histograms"]
    raw_e1_CBV_dirs = \
    loadmat(CBV_out_dir + "/" + "raw_e1_CBV_dirs.mat")["raw_e1_CBV_dirs"]
    raw_e2_CBV_region_histograms = \
    loadmat(CBV_out_dir + "/" + "raw_e2_CBV_region_histograms.mat")["raw_e2_CBV_region_histograms"]
    raw_e2_CBV_dirs = \
    loadmat(CBV_out_dir + "/" + "raw_e2_CBV_dirs.mat")["raw_e2_CBV_dirs"]

    topup_e1_CBV_region_histograms = \
    loadmat(CBV_out_dir + "/" + "topup_e1_CBV_region_histograms.mat")["topup_e1_CBV_region_histograms"]
    topup_e1_CBV_dirs = \
    loadmat(CBV_out_dir + "/" + "topup_e1_CBV_dirs.mat")["topup_e1_CBV_dirs"]
    topup_e2_CBV_region_histograms = \
    loadmat(CBV_out_dir + "/" + "topup_e2_CBV_region_histograms.mat")["topup_e2_CBV_region_histograms"]
    topup_e2_CBV_dirs = \
    loadmat(CBV_out_dir + "/" + "topup_e2_CBV_dirs.mat")["topup_e2_CBV_dirs"]

    epic_e1_CBV_region_histograms = \
    loadmat(CBV_out_dir + "/" + "epic_e1_CBV_region_histograms.mat")["epic_e1_CBV_region_histograms"]
    epic_e1_CBV_dirs = \
    loadmat(CBV_out_dir + "/" + "epic_e1_CBV_dirs.mat")["epic_e1_CBV_dirs"]
    epic_e2_CBV_region_histograms = \
    loadmat(CBV_out_dir + "/" + "epic_e2_CBV_region_histograms.mat")["epic_e2_CBV_region_histograms"]
    epic_e2_CBV_dirs = \
    loadmat(CBV_out_dir + "/" + "epic_e2_CBV_dirs.mat")["epic_e2_CBV_dirs"]
    
    return region_values,\
            hist_edges,\
            raw_e1_CBV_region_histograms,\
            raw_e1_CBV_dirs,\
            raw_e2_CBV_region_histograms,\
            raw_e2_CBV_dirs,\
            topup_e1_CBV_region_histograms,\
            topup_e1_CBV_dirs,\
            topup_e2_CBV_region_histograms,\
            topup_e2_CBV_dirs,\
            epic_e1_CBV_region_histograms,\
            epic_e1_CBV_dirs,\
            epic_e2_CBV_region_histograms,\
            epic_e2_CBV_dirs

def replace_spaces_with_underscore(parent_path):
    # https://stackoverflow.com/questions/41176509/python-how-to-replace-whitespaces-by-underscore-in-the-name-of-all-files-folde
    # Renames the folder and file names within the (also relative) 
    # directory parent_path to be Unix friendly
    # -> Changes spaces to _
    """   
    for path, folders, files in os.walk(parent_path):
        for f in files:
            os.rename(os.path.join(path, f), os.path.join(path, f.replace(' ', '_')))
        for i in range(len(folders)):
            new_name = folders[i].replace(' ', '_')
            os.rename(os.path.join(path, folders[i]), os.path.join(path, new_name))
            folders[i] = new_name
    """
    # https://stackoverflow.com/questions/225735/batch-renaming-of-files-in-a-directory
    #[os.rename(f, f.replace(' ', '_')) for f in os.listdir(parent_path) if not f.startswith('.')]

    # https://askubuntu.com/questions/771225/remove-leading-whitespace-from-files-folders-and-their-subfolders
    for root, dirs, files in os.walk(parent_path, topdown=False):
        for f in files:
            if " " in f:
                shutil.move(root+"/"+f, root+"/"+f.replace(" ", "_"))
        for dr in dirs:
            if " " in dr:
                shutil.move(root+"/"+dr, root+"/"+dr.replace(" ", "_"))

def load_nifti(file):
    # Returns 
    # voxel data : numpy array
    # voxel dimensions (x, y, z) : tuple(,,)
    # nifti header : nibabel.nifti1.Nifti1Header
    data_class = nib.load(file)
    return data_class.get_fdata(), tuple(data_class.header["pixdim"][1:4]), data_class.header

def xyzt_to_tzyx(vol_xyzt):
    vol_tyzx = np.swapaxes(vol_xyzt, 0, 3)
    vol_tzyx = np.swapaxes(vol_tyzx, 1, 2)
    
    # Return data with reverse x axis
    #return vol_tzyx[:,:,:,::-1]
    return vol_tzyx

def xyz_to_zyx(vol_xyz):
    vol_zyx = np.swapaxes(vol_xyz, 0, 2)
    
    # Return data with reverse x axis
    #return vol_zyx[:,:,::-1]
    return vol_zyx

def zero_two_tail(series, fraction=0.05):
    # series: Pandas Series (1-D DataFrame)
    # sets the data at a fraction of the
    # start and beginning if the series to 0.
    row_array = series.values
    row_array[:np.int(np.floor(len(row_array)*(fraction)))] = 0
    row_array[np.int(np.floor(len(row_array)*(1-fraction))):] = 0
    return pd.Series(row_array, index=series.keys())

def preprocess_histograms(hists_orig, two_tail_fraction=0.05):
    """
    hists_orig: pandas.core.frame.DataFrame
    contains all MNI region histograms 
    for a single cbv volume .
    Returns: pandas.core.frame.DataFrame
    Preprocessing:
    
    1. Setting values to 0 in a fraction of the start and end
    # of the intensity range to 0 .
    
    2. Remove rows with only 0s .
    
    3. For each histogram, compute the area.
    The divide each histogram bin by the area.
    
    """
    hists = hists_orig.copy()
    
    # 1.
    hists.apply(lambda row: zero_two_tail(row, fraction=two_tail_fraction), axis=1)
    # 2.
    hists = hists.loc[~(hists==0).all(axis=1)]
    # 3.
    hists = hists.apply(lambda row: row/row.sum(), axis=1)
    return hists

def hellinger_distance(p, q):
    """
    "Probabillistic euclidean distance"
    Fidelity similarity.
    https://gist.github.com/larsmans/3116927
    """
    return euclidean(np.sqrt(p), np.sqrt(q)) / np.sqrt(2)

def calculate_similarities(hists1, hists2, method="hellinger"):
    """
    There are many histogram comparison algorithms, for instance see:
    https://stats.stackexchange.com/questions/7400/how-to-assess-the-similarity-of-two-histograms
    
    - Earths movers distance or Wasserstein distance
    https://en.wikipedia.org/wiki/Hellinger_distance

    - Hellinger metric
    https://en.wikipedia.org/wiki/Wasserstein_metric
    https://en.wikipedia.org/wiki/Earth_mover%27s_distance
    """
    return pd.concat((hists1, hists2), axis=1, join="inner")\
            .apply(lambda row: eval(method + "_distance")(hists1.loc[row.name].values, hists2.loc[row.name].values), axis=1)

def get_cbv_and_labels_paths(raw_e1_CBV_region_histograms,\
                                raw_e1_CBV_dirs,\
                                raw_e2_CBV_region_histograms,\
                                raw_e2_CBV_dirs,\
                                topup_e1_CBV_region_histograms,\
                                topup_e1_CBV_dirs,\
                                topup_e2_CBV_region_histograms,\
                                topup_e2_CBV_dirs,\
                                epic_e1_CBV_region_histograms,\
                                epic_e1_CBV_dirs,\
                                epic_e2_CBV_region_histograms,\
                                epic_e2_CBV_dirs,\
                                subject_number=0,\
                                correction_method="raw",\
                                cbv_based_on="e1"):
    d_remote = Path(eval(correction_method + "_" + cbv_based_on + "_CBV_dirs")[0][subject_number][0])
    # https://stackoverflow.com/questions/26724275/removing-the-first-folder-in-a-path
    d = Path.joinpath(Path.cwd().parent.parent, *d_remote.parts[6:])
    cbv_path = Path.joinpath(d, "wr_coregest_Normalized_rCBV_map_-Leakage_corrected.nii")
    labels_path = d.joinpath(d.parent, "r_" + cbv_based_on + "_labels_Neuromorphometrics.nii")
    return cbv_path, labels_path

def preprocess_and_calculate_all_histogram_distances(region_values_array,\
                                                     region_names_array,\
                                                     hist_edges_array,\
                                                     cbv_hists_1_array,\
                                                     cbv_hists_2_array,\
                                                     two_tail_fraction,\
                                                     comparison_method="hellinger"):
    
    assert len(region_values_array.flatten()) == len(region_names_array), "The region values and names lists have different length!"
    assert len(cbv_hists_1_array) == len(cbv_hists_2_array), "The two histogram collections have different length!"
    
    num_subjects = len(cbv_hists_1_array)
    num_regions = len(region_values_array.flatten())
    
    all_distances_array = np.empty((num_subjects, num_regions))
    all_distances_array[:] = np.nan
    
    for subj_idx in range(num_subjects):
        
        # For instance histograms of non-corrected GE rCBV
        subj_cbv_hists_1_df = \
        pd.DataFrame(data=cbv_hists_1_array[subj_idx], \
                     index=region_values_array.flatten(), \
                     columns=hist_edges_array[0][:-1])
        
        subj_cbv_hists_1_prep_df = preprocess_histograms(subj_cbv_hists_1_df, two_tail_fraction=two_tail_fraction)
        
        # For instance histograms of TOPUP corrected GE rCBV
        subj_cbv_hists_2_df = \
        pd.DataFrame(data=cbv_hists_2_array[subj_idx], \
                     index=region_values_array.flatten(), \
                     columns=hist_edges_array[0][:-1])
        
        subj_cbv_hists_2_prep_df = preprocess_histograms(subj_cbv_hists_2_df, two_tail_fraction=two_tail_fraction)
        
        subj_distances_df = calculate_similarities(subj_cbv_hists_1_prep_df, subj_cbv_hists_2_prep_df, method=comparison_method)
        
        for comparable_region in subj_distances_df.index:
            corresponding_region_idx = np.argwhere(region_values_array.flatten() == comparable_region)[0][0]
            
            all_distances_array[subj_idx, corresponding_region_idx] = subj_distances_df.loc[comparable_region]
    
    all_distances_df = pd.DataFrame(all_distances_array, columns=region_names_array)
    
    return all_distances_df