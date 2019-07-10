from spimagine import volshow, volfig
import numpy as np
from utils import xyz_to_zyx, load_nifti, preprocess_histograms
import pandas as pd
import matplotlib
#matplotlib.use('Qt5Agg')
#%matplotlib qt5
#%matplotlib notebook
#%matplotlib widget
import matplotlib.pyplot as plt

def spimagine_show_volume_numpy(numpy_array, stackUnits=(1, 1, 1), interpolation="nearest", cmap="grays"):
    # Spimagine OpenCL volume renderer.
    volfig()
    spim_widget = \
    volshow(numpy_array, stackUnits=stackUnits, interpolation=interpolation)
    spim_widget.set_colormap(cmap)
    
def visualize_regions(regions_df, labels_data, labels_dims, interpolation="nearest", cmap="hot"):
    """
    regions_df : pandas.core.frame.DataFrame
    contains regions as index, together with a float
    labels_dims
    labels_data : np.array 
    """
    heat_map = labels_data.copy()
    for region_value in np.array(np.unique(heat_map)):
        if region_value not in regions_df.index:
            heat_map[heat_map == region_value] = 0
        else:
            heat_map[heat_map == region_value] = regions_df.loc[region_value]
    spimagine_show_volume_numpy(heat_map, stackUnits=labels_dims, interpolation=interpolation, cmap=cmap)

def load_and_visualize_cbv(cbv_path, interpolation="linear", cmap="hot"):
    cbv_data_temp, cbv_dims_temp, cbv_hdr_temp = load_nifti(str(cbv_path))
    cbv_data_temp[np.isnan(cbv_data_temp)] = 0
    cbv_data_temp = xyz_to_zyx(cbv_data_temp)
    spimagine_show_volume_numpy(cbv_data_temp, stackUnits=cbv_dims_temp, interpolation=interpolation, cmap=cmap)

def load_and_visualize_labels(labels_path, interpolation="nearest", cmap="grays"):
    labels_data_temp, labels_dims_temp, labels_hdr_temp = load_nifti(str(labels_path))
    labels_data_temp = xyz_to_zyx(labels_data_temp)
    spimagine_show_volume_numpy(labels_data_temp, stackUnits=labels_dims_temp, interpolation=interpolation, cmap=cmap)

def preprocess_and_plot_all_histograms(region_values,\
                                       hist_edges,\
                                       raw_e1_CBV_region_histograms,\
                                       raw_e2_CBV_region_histograms,\
                                       topup_e1_CBV_region_histograms,\
                                       topup_e2_CBV_region_histograms,\
                                       epic_e1_CBV_region_histograms,\
                                       epic_e2_CBV_region_histograms,\
                                       two_tail_fraction=0.03,\
                                       subject_number=0,\
                                       ID="1099269047"):
    raw_e1 = pd.DataFrame(\
                          data=raw_e1_CBV_region_histograms[subject_number], \
                          index=region_values.flatten(), \
                          columns=hist_edges[0][:-1])
    raw_e1_prep = preprocess_histograms(raw_e1, two_tail_fraction=two_tail_fraction)

    raw_e2 = pd.DataFrame(\
                        data=raw_e2_CBV_region_histograms[subject_number], \
                        index=region_values.flatten(), \
                        columns=hist_edges[0][:-1])
    raw_e2_prep = preprocess_histograms(raw_e2, two_tail_fraction=two_tail_fraction)

    topup_e1 = pd.DataFrame(\
                        data=topup_e1_CBV_region_histograms[subject_number], \
                        index=region_values.flatten(), \
                        columns=hist_edges[0][:-1])
    topup_e1_prep = preprocess_histograms(topup_e1, two_tail_fraction=two_tail_fraction)

    topup_e2 = pd.DataFrame(\
                        data=topup_e2_CBV_region_histograms[subject_number], \
                        index=region_values.flatten(), \
                        columns=hist_edges[0][:-1])
    topup_e2_prep = preprocess_histograms(topup_e2, two_tail_fraction=two_tail_fraction)

    epic_e1 = pd.DataFrame(\
                        data=epic_e1_CBV_region_histograms[subject_number], \
                        index=region_values.flatten(), \
                        columns=hist_edges[0][:-1])
    epic_e1_prep = preprocess_histograms(epic_e1, two_tail_fraction=two_tail_fraction)

    epic_e2 = pd.DataFrame(\
                        data=epic_e2_CBV_region_histograms[subject_number], \
                        index=region_values.flatten(), \
                        columns=hist_edges[0][:-1])
    epic_e2_prep = preprocess_histograms(epic_e2, two_tail_fraction=two_tail_fraction)


    fig = plt.figure(figsize=np.array([6.4*0.8*3, 4.8*0.8]))

    ax1 = fig.add_subplot(2, 3, 1)
    ax1.yaxis.set_label_position("right")
    ax1.set_ylabel("raw e1")
    ax1.plot(raw_e1_prep.transpose());
    plt.subplots_adjust(hspace = 0.001)

    ax2 = fig.add_subplot(2, 3, 4, sharex=ax1, sharey=ax1)
    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel("raw e2")
    ax2.plot(raw_e2_prep.transpose());
    plt.subplots_adjust(hspace = 0.001)

    ax3 = fig.add_subplot(2, 3, 2, sharex=ax1, sharey=ax1)
    ax3.yaxis.set_label_position("right")
    ax3.set_ylabel("topup e1")
    ax3.plot(topup_e1_prep.transpose());
    plt.subplots_adjust(hspace = 0.001)

    ax4 = fig.add_subplot(2, 3, 5, sharex=ax1, sharey=ax1)
    ax4.yaxis.set_label_position("right")
    ax4.set_ylabel("topup e2")
    ax4.plot(topup_e2_prep.transpose());
    plt.subplots_adjust(hspace = 0.001)

    ax5 = fig.add_subplot(2, 3, 3, sharex=ax1, sharey=ax1)
    ax5.yaxis.set_label_position("right")
    ax5.set_ylabel("epic e1")
    ax5.plot(epic_e1_prep.transpose());
    plt.subplots_adjust(hspace = 0.001)

    ax6 = fig.add_subplot(2, 3, 6, sharex=ax1, sharey=ax1)
    ax6.yaxis.set_label_position("right")
    ax6.set_ylabel("epic e2")
    ax6.plot(epic_e2_prep.transpose());
    plt.subplots_adjust(hspace = 0.001)

    #fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    #fig.tight_layout()

    title = "MNI rCBV %s" % ID

    fig.suptitle(title)
    
    return raw_e1_prep,\
            raw_e2_prep,\
            topup_e1_prep,\
            topup_e2_prep,\
            epic_e1_prep,\
            epic_e2_prep

def preprocess_and_plot_selected_histograms(region_values,\
                                            hist_edges,\
                                            raw_e1_CBV_region_histograms,\
                                            raw_e2_CBV_region_histograms,\
                                            topup_e1_CBV_region_histograms,\
                                            topup_e2_CBV_region_histograms,\
                                            epic_e1_CBV_region_histograms,\
                                            epic_e2_CBV_region_histograms,\
                                            two_tail_fraction=0.03,\
                                            subject_number=0,\
                                            correction_method="raw",\
                                            ID="1099269047"):
    fig = plt.figure(figsize=np.array([6.4*0.8, 4.8*0.8]))

    cbv_hists_e1 = pd.DataFrame(\
                          data=eval(correction_method + "_e1_CBV_region_histograms")[subject_number], \
                          index=region_values.flatten(), \
                          columns=hist_edges[0][:-1])
    cbv_hists_e1_prep = preprocess_histograms(cbv_hists_e1, two_tail_fraction=two_tail_fraction)

    cbv_hists_e2 = pd.DataFrame(\
                          data=eval(correction_method + "_e2_CBV_region_histograms")[subject_number], \
                          index=region_values.flatten(), \
                          columns=hist_edges[0][:-1])
    cbv_hists_e2_prep = preprocess_histograms(cbv_hists_e2, two_tail_fraction=two_tail_fraction)

    ax1 = fig.add_subplot(2, 1, 1)
    ax1.yaxis.set_label_position("right")
    ax1.set_ylabel("e1")
    ax1.plot(cbv_hists_e1_prep.transpose());
    plt.subplots_adjust(hspace = 0.001)
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel("e2")
    ax2.plot(cbv_hists_e2_prep.transpose());
    plt.subplots_adjust(hspace = 0.001)

    title = "MNI rCBV %s %s" % (ID, correction_method)

    fig.suptitle(title)
    
    fig2 = plt.figure()
    cbv_hists_e1_prep.mean().plot()
    cbv_hists_e1_prep.median().plot()
    cbv_hists_e1_prep.std().plot()
    cbv_hists_e2_prep.mean().plot()
    cbv_hists_e2_prep.median().plot()
    cbv_hists_e2_prep.std().plot()
    plt.legend(("cbv_hists_e1 mean", "cbv_hists_e1 median", "cbv_hists_e1 std", "cbv_hists_e2 mean", "cbv_hists_e2 median", "cbv_hists_e2 std"))
    plt.suptitle(title)

def sorted_boxplot_histogram_distances(all_distances_df, ax, ylabel2="Sorted Box Plot", ylabel="Hellinger distance", title="n", top=20):

    all_distances_medians_df = all_distances_df.median()

    all_distances_medians_df.sort_values(ascending=False, inplace=True)

    all_distances_sorted_df = all_distances_df[all_distances_medians_df.index]
    
    if top=="all":
        selected_data = all_distances_sorted_df
    else:
        selected_data = all_distances_sorted_df[all_distances_sorted_df.keys()[0:top]]
    
    _, ymax = ax.get_ylim()
    this_ymax = selected_data.max().max()
    if ymax == 1 :
        # Replace the default value
        ax.set_ylim(top=this_ymax)
    _, ymax = ax.get_ylim()
    
    bp = selected_data.boxplot(rot=-90, ax=ax)
    x = np.arange(selected_data.shape[1])
    noofobs = selected_data.notna().sum()
    for tick, label in zip(x, bp.get_xticklabels()):
        bp.text(tick+1, ymax+0.05*ymax, noofobs[tick], horizontalalignment='center')
    plt.ylabel(ylabel)
    #plt.title(title, y=ymax+0.12*ymax)
    bp.text((tick//2)+1, ymax+0.2*ymax, title, horizontalalignment='center')
    ax_sec = ax.twinx()
    ax_sec.set_yticklabels([])
    ax_sec.yaxis.set_ticks_position('none')
    ax_sec.set_ylabel(ylabel2, color='b')
    if top=="all":
        plt.suptitle("All histogram differences sorted after median")
    else:
        plt.suptitle("Top " + str(top) + " histogram differences sorted after median")