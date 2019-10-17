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
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
from spimagine.models.imageprocessor import BlurProcessor
from spimagine.utils.quaternion import Quaternion

def spimagine_show_volume_numpy(numpy_array, stackUnits=(1, 1, 1), interpolation="nearest", cmap="grays"):
    # Spimagine OpenCL volume renderer.
    volfig()
    spim_widget = \
    volshow(numpy_array[::-1, ::-1, ::-1], stackUnits=stackUnits, interpolation=interpolation)
    spim_widget.set_colormap(cmap)
    #spim_widget.transform.setRotation(np.pi/8,-0.6,0.5,1)
    
    spim_widget.transform.setQuaternion(Quaternion(-0.005634209439510011,0.00790509382124309,-0.0013812284289010514,-0.9999519273706857))

def spimagine_show_mni_volume_numpy(numpy_array, stackUnits=(1, 1, 1), interpolation="nearest", cmap="grays"):
    # Spimagine OpenCL volume renderer.
    volfig()
    spim_widget = \
    volshow(numpy_array, stackUnits=stackUnits, interpolation=interpolation)
    spim_widget.set_colormap(cmap)
    #spim_widget.transform.setRotation(np.pi/8,-0.6,0.5,1)

    # Up
    spim_widget.transform.setQuaternion(Quaternion(0.0019763238787262496,4.9112439271825864e-05,0.9999852343690417,0.0050617341749588825))

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
    spimagine_show_mni_volume_numpy(heat_map, stackUnits=labels_dims, interpolation=interpolation, cmap=cmap)

def load_and_visualize_cbv(cbv_path, interpolation="linear", cmap="hot"):
    cbv_data_temp, cbv_dims_temp, cbv_hdr_temp = load_nifti(str(cbv_path))
    cbv_data_temp[np.isnan(cbv_data_temp)] = 0
    cbv_data_temp = xyz_to_zyx(cbv_data_temp)
    spimagine_show_mni_volume_numpy(cbv_data_temp, stackUnits=cbv_dims_temp, interpolation=interpolation, cmap=cmap)

def load_and_visualize_labels(labels_path, interpolation="nearest", cmap="grays"):
    labels_data_temp, labels_dims_temp, labels_hdr_temp = load_nifti(str(labels_path))
    labels_data_temp = xyz_to_zyx(labels_data_temp)
    spimagine_show_mni_volume_numpy(labels_data_temp, stackUnits=labels_dims_temp, interpolation=interpolation, cmap=cmap)

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
                          index=region_values, \
                          columns=hist_edges[0][:-1])
    raw_e1_prep = preprocess_histograms(raw_e1, two_tail_fraction=two_tail_fraction)

    raw_e2 = pd.DataFrame(\
                        data=raw_e2_CBV_region_histograms[subject_number], \
                        index=region_values, \
                        columns=hist_edges[0][:-1])
    raw_e2_prep = preprocess_histograms(raw_e2, two_tail_fraction=two_tail_fraction)

    topup_e1 = pd.DataFrame(\
                        data=topup_e1_CBV_region_histograms[subject_number], \
                        index=region_values, \
                        columns=hist_edges[0][:-1])
    topup_e1_prep = preprocess_histograms(topup_e1, two_tail_fraction=two_tail_fraction)

    topup_e2 = pd.DataFrame(\
                        data=topup_e2_CBV_region_histograms[subject_number], \
                        index=region_values, \
                        columns=hist_edges[0][:-1])
    topup_e2_prep = preprocess_histograms(topup_e2, two_tail_fraction=two_tail_fraction)

    epic_e1 = pd.DataFrame(\
                        data=epic_e1_CBV_region_histograms[subject_number], \
                        index=region_values, \
                        columns=hist_edges[0][:-1])
    epic_e1_prep = preprocess_histograms(epic_e1, two_tail_fraction=two_tail_fraction)

    epic_e2 = pd.DataFrame(\
                        data=epic_e2_CBV_region_histograms[subject_number], \
                        index=region_values, \
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
                          index=region_values, \
                          columns=hist_edges[0][:-1])
    cbv_hists_e1_prep = preprocess_histograms(cbv_hists_e1, two_tail_fraction=two_tail_fraction)

    cbv_hists_e2 = pd.DataFrame(\
                          data=eval(correction_method + "_e2_CBV_region_histograms")[subject_number], \
                          index=region_values, \
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

def sorted_boxplot_histogram_distances(all_distances_df, all_relative_rcbv_df, ax, region_values, region_names, region_names_to_exclude, ylabel2="Sorted Box Plot", ylabel="Hellinger distance", title="", xlabel="", top=20):
    # Drop excluded regions
    all_distances_df = \
    all_distances_df.drop([str(region_values[np.where(region_names == region_name)[0][0]]) for region_name in region_names_to_exclude], axis=1)
    all_relative_rcbv_df = \
    all_relative_rcbv_df.drop([str(region_values[np.where(region_names == region_name)[0][0]]) for region_name in region_names_to_exclude], axis=1)    
    # --for distances
    # Calculate medians
    all_distances_medians_df = all_distances_df.median()
    # Sort the medians
    all_distances_medians_df.sort_values(ascending=False, inplace=True)
    # Show the data according to the sorted medians
    all_distances_sorted_df = all_distances_df[all_distances_medians_df.index]
    # --for relative rcbv
    # Calculate medians
    all_relative_rcbv_medians_df = all_relative_rcbv_df.median()
    
    if top=="all":
        selected_data = all_distances_sorted_df
    else:
        # Pick top top highest columns after descending median
        selected_data = all_distances_sorted_df[all_distances_sorted_df.keys()[0:top]]
    
    # ymax used later for correct placement of title text
    _, ymax = ax.get_ylim()
    this_ymax = selected_data.max().max()
    if ymax == 1 :
        # Replace the default value
        ax.set_ylim(top=this_ymax)
    _, ymax = ax.get_ylim()
        
    # Create boxplot
    bp = selected_data.boxplot(rot=-90, ax=ax, grid=False)
    #bp = selected_data.boxplot(rot=-55, ax=ax, grid=False)
    # A list that is used give x placement of number of observations text
    x = np.arange(selected_data.shape[1])
    # Count the number of observations in each column
    noofobs = selected_data.notna().sum()
    # Write the number of observations above each box in the plot
    #for tick, label in zip(x, bp.get_xticklabels()):
    #    bp.text(tick+1, ymax+0.05*ymax, noofobs[tick], horizontalalignment='center')

    # Add number of observations to xticklabels
    xticklabels = []
    for tick, label in zip(x, bp.get_xticklabels()):
        #xticklabels += [label.get_text() + " (n=" + str(noofobs[tick]) + ")"]
        
        region_name = region_names[np.where(region_values == np.int64(label.get_text()))[0][0]]
        
        region_median_relative_rcbv_change = all_relative_rcbv_medians_df.loc[label.get_text()]
        
        region_text_space = [" " for s in range(30)] # 36
        
        if len(region_name) > len(region_text_space):
            region_name = region_name[0:len(region_text_space)]
            region_text_space[0:len(region_name)] = region_name
            region_text_space[-3:] = "..."
        else:
            region_text_space[0:len(region_name)] = region_name
        region_text = "".join(region_text_space)
        description_text = str(tick+1) + ". (n=" + format(noofobs[tick], '02d') + ") " + region_text #+ " {0:.3f}".format(region_median_relative_rcbv_change)
        #print(description_text + "|")
        
        xticklabels += [description_text]
    # Update the histogram plot with the new xticklabels
    bp.set_xticklabels(xticklabels)
    
    plt.xlabel(xlabel)
    #bp.set_ylabel(ylabel, rotation=-90)
    plt.ylabel(ylabel, rotation=-90, labelpad=11)
    # Used as a placement for title
    bp.text((tick//2)+1, ymax+0.2*ymax, title, horizontalalignment='center')
    # Second twin y axis
    ax_sec = ax.twinx()
    ax_sec.set_yticklabels([])
    ax_sec.yaxis.set_ticks_position('none')
    ax_sec.set_ylabel(ylabel2, color='b')
    
    # Return top medians df for further analysis
    to_return = selected_data.median()
    
    # Set the index elements 
    # (here the region values originally being string) 
    # to uint64 for compatibility with visualize_regions()
    to_return.index = to_return.index.astype(np.uint64)
    return to_return

def sorted_boxplot_relative_rcbv_change(all_total_rcbv_df, ax, region_values, region_names, region_names_to_exclude, ascending=False, ylabel2="Sorted Box Plot", ylabel="Hellinger distance", title="", xlabel="", top=20):
    all_total_rcbv_df = \
    all_total_rcbv_df.drop([str(region_values[np.where(region_names == region_name)[0][0]]) for region_name in region_names_to_exclude], axis=1)    
    # --for relative rcbv
    # Calculate medians
    all_total_rcbv_medians_df = all_total_rcbv_df.median()
    all_total_rcbv_medians_df.sort_values(ascending=ascending, inplace=True)
    # Show the data according to the sorted medians
    all_total_rcbv_sorted_df = all_total_rcbv_df[all_total_rcbv_medians_df.index]
    
    if top=="all":
        selected_data = all_total_rcbv_sorted_df
    else:
        # Pick top top highest columns after descending median
        selected_data = all_total_rcbv_sorted_df[all_total_rcbv_sorted_df.keys()[0:top]]
    
    # ymax used later for correct placement of title text
    _, ymax = ax.get_ylim()
    this_ymax = selected_data.max().max()
    if ymax == 1 :
        # Replace the default value
        ax.set_ylim(top=this_ymax)
    _, ymax = ax.get_ylim()
    
    # Create boxplot
    bp = selected_data.boxplot(rot=-90, ax=ax, grid=False)
    #bp = selected_data.boxplot(rot=-55, ax=ax, grid=False)
    # A list that is used give x placement of number of observations text
    x = np.arange(selected_data.shape[1])
    # Count the number of observations in each column
    noofobs = selected_data.notna().sum()
    # Write the number of observations above each box in the plot
    #for tick, label in zip(x, bp.get_xticklabels()):
    #    bp.text(tick+1, ymax+0.05*ymax, noofobs[tick], horizontalalignment='center')
    
    # Add number of observations to xticklabels
    xticklabels = []
    for tick, label in zip(x, bp.get_xticklabels()):
        #xticklabels += [label.get_text() + " (n=" + str(noofobs[tick]) + ")"]
        
        region_name = region_names[np.where(region_values == np.int64(label.get_text()))[0][0]]
        
        region_text_space = [" " for s in range(36)]
        
        if len(region_name) > len(region_text_space):
            region_name = region_name[0:len(region_text_space)]
            region_text_space[0:len(region_name)] = region_name
            region_text_space[-3:] = "..."
        else:
            region_text_space[0:len(region_name)] = region_name
        region_text = "".join(region_text_space)
        description_text = str(tick+1) + ". (n=" + format(noofobs[tick], '02d') + ") " + region_text
        #print(description_text + "|")
        
        xticklabels += [description_text]
    # Update the histogram plot with the new xticklabels
    bp.set_xticklabels(xticklabels)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel, rotation=-90, labelpad=11)
    # Used as a placement for title
    bp.text((tick//2)+1, ymax+0.2*ymax, title, horizontalalignment='center')
    # Second twin y axis
    ax_sec = ax.twinx()
    ax_sec.set_yticklabels([])
    ax_sec.yaxis.set_ticks_position('none')
    ax_sec.set_ylabel(ylabel2, color='b')
    
    # Return top medians df for further analysis
    to_return = selected_data.median()
    
    # Set the index elements 
    # (here the region values originally being string) 
    # to uint64 for compatibility with visualize_regions()
    to_return.index = to_return.index.astype(np.uint64)
    return to_return

def sorted_medians(df, \
                   region_values, \
                   region_names, \
                   region_names_to_exclude, \
                   ascending=False, \
                   top=20):
    # Drop excluded regions
    df = \
    df.drop([str(region_values[np.where(region_names == region_name)[0][0]]) for region_name in region_names_to_exclude], axis=1)
    # Calculate medians
    medians_df = df.median()
    # Sort the medians
    medians_df.sort_values(ascending=ascending, inplace=True)
    # Show the data according to the sorted medians
    sorted_df = df[medians_df.index]
    
    if top=="all":
        selected_data = sorted_df
    else:
        # Pick top top highest columns after descending median
        selected_data = sorted_df[sorted_df.keys()[0:top]]
    
    # Return top medians df for further analysis
    to_return = selected_data.median()
    
    # Set the index elements 
    # (here the region values originally being string) 
    # to uint64 for compatibility with visualize_regions()
    to_return.index = to_return.index.astype(np.uint64)
    return to_return

def sorted_means(df, \
                   region_values, \
                   region_names, \
                   region_names_to_exclude, \
                   ascending=False, \
                   top=20):
    # Drop excluded regions
    df = \
    df.drop([str(region_values[np.where(region_names == region_name)[0][0]]) for region_name in region_names_to_exclude], axis=1)
    # Calculate medians
    means_df = df.mean()
    # Sort the medians
    means_df.sort_values(ascending=ascending, inplace=True)
    # Show the data according to the sorted medians
    sorted_df = df[means_df.index]
    
    if top=="all":
        selected_data = sorted_df
    else:
        # Pick top top highest columns after descending median
        selected_data = sorted_df[sorted_df.keys()[0:top]]
    
    # Return top medians df for further analysis
    to_return = selected_data.mean()
    
    # Set the index elements 
    # (here the region values originally being string) 
    # to uint64 for compatibility with visualize_regions()
    to_return.index = to_return.index.astype(np.uint64)
    return to_return

def render_regions_set_to_pngs(regions_df, \
                               labels_data, \
                               labels_dims, \
                               output_rel_dir, \
                               png_prefix="", \
                               interpolation="nearest", \
                               cmap="hot", \
                               windowMin=0, \
                               windowMax=1, \
                               blur_3d=False, \
                               blur_3d_sigma=1):
    
    # The regions data is visualized as a 3D heat map
    heat_map = labels_data.copy()
    
    # Fill regions in the the heat volume by 
    # corresponding values in regions_df
    # Set a region to 0 if it is not in regions_df
    for region_value in np.array(np.unique(heat_map)):
        if region_value not in regions_df.index:
            heat_map[heat_map == region_value] = 0
        else:
            heat_map[heat_map == region_value] = regions_df.loc[region_value]
    
    # Three views are rendered to file with names:
    png_file_1 = output_rel_dir + "/" + png_prefix + "-axial-inferior-superior.png"
    png_file_2 = output_rel_dir + "/" + png_prefix + "-sagittal-r-l.png"
    png_file_3 = output_rel_dir + "/" + png_prefix + "-mixed-r-l-anterior-posterior.png"
    
    # Create a spimagine instance, then save three views to separate pngs
    volfig()
    spim_widget = \
    volshow(heat_map, autoscale=False, stackUnits=labels_dims, interpolation=interpolation)
    #volshow(heat_map[::-1, ::-1, ::-1], autoscale=False, stackUnits=labels_dims, interpolation=interpolation)
    
    # A hack to enable blur. Currently not working, so should be disabled.
    if blur_3d:
        # Add a blur module with preferred sigma
        spim_widget.impListView.add_image_processor(BlurProcessor(blur_3d_sigma))
        # Animate click for enabling the blur
        spim_widget.impListView.impViews[-1].children()[0].animateClick()
    
    # Set colormap
    spim_widget.set_colormap(cmap)
    
    # Windowing
    #spim_widget.transform.setValueScale(regions_df.min(), regions_df.max())
    #spim_widget.transform.setValueScale(0, regions_df.max())
    spim_widget.transform.setValueScale(windowMin, windowMax)
    
    # Set interpolation directly
    #spim_widget.transform.setInterpolate(1)
    
    # Set bounding box not visible
    spim_widget.transform.setBox(False)
    
    # Zoom
    spim_widget.transform.setZoom(1.4)
    
    # NB: The rotations are not adding up.
    # each spim_widget.transform.setRotation call
    # rotates from original orientation given by volshow()
    
    # First view
    #spim_widget.transform.setRotation(np.pi/2,0,1,0)
    #spim_widget.transform.setQuaternion(Quaternion(-0.005634209439510011,0.00790509382124309,-0.0013812284289010514,-0.9999519273706857))
    # Up rightwards
    spim_widget.transform.setQuaternion(Quaternion(-0.018120594789136298,0.708165522710642,0.7057824278204939,0.006663271093062176))
    # Take snapshot
    spim_widget.saveFrame(png_file_1)
    
    # Second view
    #spim_widget.transform.setRotation(np.pi/4,0,1,0)
    #spim_widget.transform.setQuaternion(Quaternion(0.007638906066214874,-0.7092538697232732,-0.004760086014776442,0.7048956918250604))
    # Sagittal
    spim_widget.transform.setQuaternion(Quaternion(-0.0020183487063897406,0.7073151860516024,-0.0032067927203972405,0.7068881584667737))
    # Take snapshot
    spim_widget.saveFrame(png_file_2)
    
    # Third view
    #spim_widget.transform.setRotation(np.pi/8,-0.6,0.5,1)
    #spim_widget.transform.setQuaternion(Quaternion(-0.3228904671232426,-0.8924886253708287,-0.28916944161613134,0.12484724075684332))
    # Fancy
    spim_widget.transform.setQuaternion(Quaternion(0.15439557175611332,0.7306565059064623,0.5147772256894417,0.4210789500980262))
    # Take snapshot
    spim_widget.saveFrame(png_file_3)
    
    # Close spimagine
    spim_widget.closeMe()
    
    #spim_widget.minSlider.value()
    #spim_widget.maxSlider.value()
    #spim_widget.maxSlider.onChanged(500 + (500/16) * regions_df.max())
    #spim_widget.maxSlider.onChanged(1000)
    #spim_widget.minSlider.onChanged(500 + (500/16) * regions_df.min())
    #spim_widget.minSlider.onChanged(0)
    
    return png_file_1, png_file_2, png_file_3

def sorted_boxplot_heatmap_figure(df_1, \
                                  df_1_rcbv, \
                                  df_2, \
                                  df_2_rcbv, \
                                  df_3, \
                                  df_3_rcbv, \
                                  df_4, \
                                  df_4_rcbv, \
                                  ylabel_1, \
                                  ylabel_2, \
                                  ylabel_3, \
                                  ylabel_4, \
                                  distance_name, \
                                  labels_data, \
                                  labels_dims, \
                                  CBV_out_dir, \
                                  rendered_image_files_list, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  top = "all", \
                                  render_pngs = True, \
                                  windowMin = 0, \
                                  windowMax = 1*0.8, \
                                  interpolation = "nearest", \
                                  cmap = "hot", \
                                  blur_3d = False, \
                                  blur_3d_sigma = 1, \
                                  method_comparison = False):
    
    fig = plt.figure(figsize=np.array([9, 10]))
    
    gs1 = gridspec.GridSpec(4, 3)
    gs1.update(left=0.08, right=0.48, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    ax1 = plt.subplot(gs1[0, :])
    medians_df_1 = sorted_boxplot_histogram_distances(df_1, \
                                                      df_1_rcbv, \
                                       ax1, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2=ylabel_1, \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", 
                                       top=top)
    ax2 = plt.subplot(gs1[1, :])
    medians_df_2 = sorted_boxplot_histogram_distances(df_2, \
                                                      df_2_rcbv, \
                                       ax2, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2=ylabel_2, \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", \
                                       top=top)

    ax3 = plt.subplot(gs1[2, :])
    medians_df_3 = sorted_boxplot_histogram_distances(df_3, \
                                                      df_3_rcbv, \
                                       ax3, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2=ylabel_3, \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", \
                                       top=top)

    ax4 = plt.subplot(gs1[3, :])
    medians_df_4 = sorted_boxplot_histogram_distances(df_4, \
                                                      df_4_rcbv, \
                                       ax4, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2=ylabel_4, \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", \
                                       top=top)
    
    gs2 = gridspec.GridSpec(4, 2)
    gs2.update(left=0.52, right=0.99, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    
    if render_pngs:
        rendered_image_files_list = []
    
    
    # Render pngs for raw_vs_topup_e1_hellinger_medians_df
    if render_pngs:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        render_regions_set_to_pngs(medians_df_1, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r1", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r1_png_file_1]
        rendered_image_files_list += [r1_png_file_2]
        rendered_image_files_list += [r1_png_file_3]
    else:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        rendered_image_files_list[0], \
        rendered_image_files_list[1], \
        rendered_image_files_list[2]
        
    ax5 = plt.subplot(gs2[0, 0])
    png_1=mpimg.imread(r1_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    
    ax6 = plt.subplot(gs2[0, 1])
    png_2=mpimg.imread(r1_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax7 = plt.subplot(gs2[0, 2])
    png_3=mpimg.imread(r1_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    # Render pngs for raw_vs_epic_e1_hellinger_medians_df
    if render_pngs:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        render_regions_set_to_pngs(medians_df_2, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r2", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r2_png_file_1]
        rendered_image_files_list += [r2_png_file_2]
        rendered_image_files_list += [r2_png_file_3]
    else:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        rendered_image_files_list[3], \
        rendered_image_files_list[4], \
        rendered_image_files_list[5]
    
    ax8 = plt.subplot(gs2[1, 0])
    png_1=mpimg.imread(r2_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    
    ax9 = plt.subplot(gs2[1, 1])
    png_2=mpimg.imread(r2_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax10 = plt.subplot(gs2[1, 2])
    png_3=mpimg.imread(r2_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for raw_vs_topup_e2_hellinger_medians_df
    if render_pngs:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        render_regions_set_to_pngs(medians_df_3, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r3", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r3_png_file_1]
        rendered_image_files_list += [r3_png_file_2]
        rendered_image_files_list += [r3_png_file_3]
    else:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        rendered_image_files_list[6], \
        rendered_image_files_list[7], \
        rendered_image_files_list[8]
    
    ax11 = plt.subplot(gs2[2, 0])
    png_1=mpimg.imread(r3_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    
    ax12 = plt.subplot(gs2[2, 1])
    png_2=mpimg.imread(r3_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax13 = plt.subplot(gs2[2, 2])
    png_3=mpimg.imread(r3_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for raw_vs_epic_e2_hellinger_medians_df
    if render_pngs:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        render_regions_set_to_pngs(medians_df_4, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r4", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r4_png_file_1]
        rendered_image_files_list += [r4_png_file_2]
        rendered_image_files_list += [r4_png_file_3]
    else:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        rendered_image_files_list[9], \
        rendered_image_files_list[10], \
        rendered_image_files_list[11]
    
    ax14 = plt.subplot(gs2[3, 0])
    png_1=mpimg.imread(r4_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.title("axial \ninferior-superior", y=-0.4)
    
    ax15 = plt.subplot(gs2[3, 1])
    png_2=mpimg.imread(r4_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    plt.title("sagittal \nright-left", y=-0.4)
    """
    ax16 = plt.subplot(gs2[3, 2])
    png_3=mpimg.imread(r4_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    plt.title("mixed \nright-left \nanterior-posterior", y=-0.4)
    """
    # Common x axis
    #fig.text(0.5, 0.04, 'common X', ha='center')
    # Common y axis
    #fig.text(0.01, 0.5, distance_name + " distance", va="center", rotation="vertical")
    # Box plots supertitle
    #fig.text(0.135, 0.975, "Top " + str(top) + " changing regions")
    # Images supertitle
    #if method_comparison:
    #    fig.text(0.6, 0.95, "Regions most different between correction \nmethods. Based on all median values")
    #else:
    #    fig.text(0.6, 0.95, "Regions most affected \nby correction. Based on all median values")
    
    # Supertitle
    #fig.suptitle("rCBV change between TOPUP and EPIC corrections")
    #fig.suptitle("rCBV change between corrections according to " + distance_name + " distance")
    #plt.subplots_adjust(wspace=0)
    #fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
    #fig.subplots_adjust(left=0.3, bottom=0.3, right=0.3, top=0.3, wspace=0.3, hspace=0.3)
    #fig.tight_layout()
    
    return rendered_image_files_list

def sorted_boxplot_heatmap_figure_distances(df_1, \
                                    df_1_rcbv, \
                                    df_2, \
                                    df_2_rcbv, \
                                    df_3, \
                                    df_3_rcbv, \
                                    df_4, \
                                    df_4_rcbv, \
                                  ylabel_1, \
                                  ylabel_2, \
                                  ylabel_3, \
                                  ylabel_4, \
                                  distance_name, \
                                  labels_data, \
                                  labels_dims, \
                                  CBV_out_dir, \
                                  rendered_image_files_list, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  top = "all", \
                                  render_pngs = True, \
                                  windowMin = 0, \
                                  windowMax = 1*0.8, \
                                  interpolation = "nearest", \
                                  cmap = "hot", \
                                  blur_3d = False, \
                                  blur_3d_sigma = 1, \
                                  method_comparison = False):
    
    fig = plt.figure(figsize=np.array([9, 10]))
    
    gs1 = gridspec.GridSpec(4, 3)
    gs1.update(left=0.08, right=0.48, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    ax1 = plt.subplot(gs1[0, :])
    medians_df_1 = sorted_boxplot_histogram_distances(df_1, \
                                                      df_1_rcbv, \
                                       ax1, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2="", \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", 
                                       top=top)
    if method_comparison:
        ax1.set_ylabel("Hellinger distance", rotation=-90, labelpad=11)
    else:
        ax1.set_ylabel(distance_name + " distance", rotation=-90, labelpad=11)
    
    #ax2 = plt.subplot(gs1[1, :])
    medians_df_2 = sorted_medians(df_2, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  top=top)
    
    ax3 = plt.subplot(gs1[2, :])
    medians_df_3 = sorted_boxplot_histogram_distances(df_3, \
                                                      df_3_rcbv, \
                                       ax3, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2="", \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", \
                                       top=top)
    if method_comparison:
        ax3.set_ylabel("Wasserstein distance", rotation=-90, labelpad=11)
    else:
        ax3.set_ylabel(distance_name + " distance", rotation=-90, labelpad=11)

    #ax4 = plt.subplot(gs1[3, :])
    medians_df_4 = sorted_medians(df_4, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  top=top)
    
    
    gs2 = gridspec.GridSpec(4, 2)
    gs2.update(left=0.52, right=0.99, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    
    if render_pngs:
        rendered_image_files_list = []
    
    
    # Render pngs for medians_df_1
    if render_pngs:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        render_regions_set_to_pngs(medians_df_1, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r1", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r1_png_file_1]
        rendered_image_files_list += [r1_png_file_2]
        rendered_image_files_list += [r1_png_file_3]
    else:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        rendered_image_files_list[0], \
        rendered_image_files_list[1], \
        rendered_image_files_list[2]
        
    ax5 = plt.subplot(gs2[0, 0])
    png_1=mpimg.imread(r1_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_1, rotation=-90, color="blue", fontsize="medium")
    
    ax6 = plt.subplot(gs2[0, 1])
    png_2=mpimg.imread(r1_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax7 = plt.subplot(gs2[0, 2])
    png_3=mpimg.imread(r1_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    # Render pngs for medians_df_2
    if render_pngs:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        render_regions_set_to_pngs(medians_df_2, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r2", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r2_png_file_1]
        rendered_image_files_list += [r2_png_file_2]
        rendered_image_files_list += [r2_png_file_3]
    else:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        rendered_image_files_list[3], \
        rendered_image_files_list[4], \
        rendered_image_files_list[5]
    
    ax8 = plt.subplot(gs2[1, 0])
    png_1=mpimg.imread(r2_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_2, rotation=-90, color="blue", fontsize="medium")
    
    ax9 = plt.subplot(gs2[1, 1])
    png_2=mpimg.imread(r2_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax10 = plt.subplot(gs2[1, 2])
    png_3=mpimg.imread(r2_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for medians_df_3
    if render_pngs:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        render_regions_set_to_pngs(medians_df_3, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r3", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r3_png_file_1]
        rendered_image_files_list += [r3_png_file_2]
        rendered_image_files_list += [r3_png_file_3]
    else:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        rendered_image_files_list[6], \
        rendered_image_files_list[7], \
        rendered_image_files_list[8]
    
    ax11 = plt.subplot(gs2[2, 0])
    png_1=mpimg.imread(r3_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_3, rotation=-90, color="blue", fontsize="medium")
    
    ax12 = plt.subplot(gs2[2, 1])
    png_2=mpimg.imread(r3_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax13 = plt.subplot(gs2[2, 2])
    png_3=mpimg.imread(r3_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for medians_df_4
    if render_pngs:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        render_regions_set_to_pngs(medians_df_4, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r4", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r4_png_file_1]
        rendered_image_files_list += [r4_png_file_2]
        rendered_image_files_list += [r4_png_file_3]
    else:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        rendered_image_files_list[9], \
        rendered_image_files_list[10], \
        rendered_image_files_list[11]
    
    ax14 = plt.subplot(gs2[3, 0])
    png_1=mpimg.imread(r4_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.title("axial \ninferior-superior", y=-0.4)
    plt.text(x=-150, y=772 + 772//10, s=ylabel_4, rotation=-90, color="blue", fontsize="medium")
    
    ax15 = plt.subplot(gs2[3, 1])
    png_2=mpimg.imread(r4_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    plt.title("sagittal \nright-left", y=-0.4)
    """
    ax16 = plt.subplot(gs2[3, 2])
    png_3=mpimg.imread(r4_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    plt.title("mixed \nright-left \nanterior-posterior", y=-0.4)
    """
    # Common x axis
    #fig.text(0.5, 0.04, 'common X', ha='center')
    # Common y axis
    #fig.text(0.01, 0.5, distance_name + " distance", va="center", rotation="vertical")
    # Box plots supertitle
    #fig.text(0.135, 0.975, "Top " + str(top) + " changing regions")
    # Images supertitle
    #if method_comparison:
    #    fig.text(0.6, 0.95, "Regions most different between correction \nmethods. Based on all median values")
    #else:
    #    fig.text(0.6, 0.95, "Regions most affected \nby correction. Based on all median values")
    
    # Supertitle
    #fig.suptitle("rCBV change between TOPUP and EPIC corrections")
    #fig.suptitle("rCBV histogram distance between corrections according to " + distance_name + " distance")
    #plt.subplots_adjust(wspace=0)
    #fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
    #fig.subplots_adjust(left=0.3, bottom=0.3, right=0.3, top=0.3, wspace=0.3, hspace=0.3)
    #fig.tight_layout()
    
    return rendered_image_files_list

def sorted_boxplot_heatmap_figure_distances_all(df_1, \
                                    df_1_rcbv, \
                                    df_2, \
                                    df_2_rcbv, \
                                    df_3, \
                                    df_3_rcbv, \
                                    df_4, \
                                    df_4_rcbv, \
                                  ylabel_1, \
                                  ylabel_2, \
                                  ylabel_3, \
                                  ylabel_4, \
                                  distance_name, \
                                  labels_data, \
                                  labels_dims, \
                                  CBV_out_dir, \
                                  rendered_image_files_list, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  top = "all", \
                                  render_pngs = True, \
                                  windowMin = 0, \
                                  windowMax = 1*0.8, \
                                  interpolation = "nearest", \
                                  cmap = "hot", \
                                  blur_3d = False, \
                                  blur_3d_sigma = 1, \
                                  method_comparison = False):
    
    fig = plt.figure(figsize=np.array([9, 10*4]))
    
    gs1 = gridspec.GridSpec(4, 3)
    gs1.update(left=0.08, right=0.48, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    ax1 = plt.subplot(gs1[0, :])
    medians_df_1 = sorted_boxplot_histogram_distances(df_1, \
                                                      df_1_rcbv, \
                                       ax1, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2="", \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", 
                                       top=top)
    if method_comparison:
        ax1.set_ylabel("Hellinger distance", rotation=-90, labelpad=11)
    else:
        ax1.set_ylabel(distance_name + " distance", rotation=-90, labelpad=11)
    
    ax2 = plt.subplot(gs1[1, :])
    """
    medians_df_2 = sorted_medians(df_2, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  top=top)
    """
    medians_df_2 = sorted_boxplot_histogram_distances(df_2, \
                                                      df_2_rcbv, \
                                       ax2, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2="", \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", 
                                       top=top)
    if method_comparison:
        ax2.set_ylabel("Hellinger distance", rotation=-90, labelpad=11)
    else:
        ax2.set_ylabel(distance_name + " distance", rotation=-90, labelpad=11)
    
    ax3 = plt.subplot(gs1[2, :])
    medians_df_3 = sorted_boxplot_histogram_distances(df_3, \
                                                      df_3_rcbv, \
                                       ax3, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2="", \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", \
                                       top=top)
    if method_comparison:
        ax3.set_ylabel("Wasserstein distance", rotation=-90, labelpad=11)
    else:
        ax3.set_ylabel(distance_name + " distance", rotation=-90, labelpad=11)
    
    ax4 = plt.subplot(gs1[3, :])
    """
    medians_df_4 = sorted_medians(df_4, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  top=top)
    """
    medians_df_4 = sorted_boxplot_histogram_distances(df_4, \
                                                      df_4_rcbv, \
                                       ax4, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ylabel2="", \
                                       ylabel="", \
                                       title="", \
                                       xlabel="", \
                                       top=top)
    if method_comparison:
        ax4.set_ylabel("Wasserstein distance", rotation=-90, labelpad=11)
    else:
        ax4.set_ylabel(distance_name + " distance", rotation=-90, labelpad=11)
    
    gs2 = gridspec.GridSpec(4, 2)
    gs2.update(left=0.52, right=0.99, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    
    if render_pngs:
        rendered_image_files_list = []
    
    
    # Render pngs for medians_df_1
    if render_pngs:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        render_regions_set_to_pngs(medians_df_1, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r1", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r1_png_file_1]
        rendered_image_files_list += [r1_png_file_2]
        rendered_image_files_list += [r1_png_file_3]
    else:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        rendered_image_files_list[0], \
        rendered_image_files_list[1], \
        rendered_image_files_list[2]
        
    ax5 = plt.subplot(gs2[0, 0])
    png_1=mpimg.imread(r1_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_1, rotation=-90, color="blue", fontsize="medium")
    
    ax6 = plt.subplot(gs2[0, 1])
    png_2=mpimg.imread(r1_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax7 = plt.subplot(gs2[0, 2])
    png_3=mpimg.imread(r1_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    # Render pngs for medians_df_2
    if render_pngs:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        render_regions_set_to_pngs(medians_df_2, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r2", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r2_png_file_1]
        rendered_image_files_list += [r2_png_file_2]
        rendered_image_files_list += [r2_png_file_3]
    else:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        rendered_image_files_list[3], \
        rendered_image_files_list[4], \
        rendered_image_files_list[5]
    
    ax8 = plt.subplot(gs2[1, 0])
    png_1=mpimg.imread(r2_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_2, rotation=-90, color="blue", fontsize="medium")
    
    ax9 = plt.subplot(gs2[1, 1])
    png_2=mpimg.imread(r2_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax10 = plt.subplot(gs2[1, 2])
    png_3=mpimg.imread(r2_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for medians_df_3
    if render_pngs:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        render_regions_set_to_pngs(medians_df_3, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r3", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r3_png_file_1]
        rendered_image_files_list += [r3_png_file_2]
        rendered_image_files_list += [r3_png_file_3]
    else:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        rendered_image_files_list[6], \
        rendered_image_files_list[7], \
        rendered_image_files_list[8]
    
    ax11 = plt.subplot(gs2[2, 0])
    png_1=mpimg.imread(r3_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_3, rotation=-90, color="blue", fontsize="medium")
    
    ax12 = plt.subplot(gs2[2, 1])
    png_2=mpimg.imread(r3_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax13 = plt.subplot(gs2[2, 2])
    png_3=mpimg.imread(r3_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for medians_df_4
    if render_pngs:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        render_regions_set_to_pngs(medians_df_4, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r4", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r4_png_file_1]
        rendered_image_files_list += [r4_png_file_2]
        rendered_image_files_list += [r4_png_file_3]
    else:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        rendered_image_files_list[9], \
        rendered_image_files_list[10], \
        rendered_image_files_list[11]
    
    ax14 = plt.subplot(gs2[3, 0])
    png_1=mpimg.imread(r4_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.title("axial \ninferior-superior", y=-0.4)
    plt.text(x=-150, y=772 + 772//10, s=ylabel_4, rotation=-90, color="blue", fontsize="medium")
    
    ax15 = plt.subplot(gs2[3, 1])
    png_2=mpimg.imread(r4_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    plt.title("sagittal \nright-left", y=-0.4)
    """
    ax16 = plt.subplot(gs2[3, 2])
    png_3=mpimg.imread(r4_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    plt.title("mixed \nright-left \nanterior-posterior", y=-0.4)
    """
    # Common x axis
    #fig.text(0.5, 0.04, 'common X', ha='center')
    # Common y axis
    #fig.text(0.01, 0.5, distance_name + " distance", va="center", rotation="vertical")
    # Box plots supertitle
    #fig.text(0.135, 0.975, "Top " + str(top) + " changing regions")
    # Images supertitle
    #if method_comparison:
    #    fig.text(0.6, 0.95, "Regions most different between correction \nmethods. Based on all median values")
    #else:
    #    fig.text(0.6, 0.95, "Regions most affected \nby correction. Based on all median values")
    
    # Supertitle
    #fig.suptitle("rCBV change between TOPUP and EPIC corrections")
    #fig.suptitle("rCBV histogram distance between corrections according to " + distance_name + " distance")
    #plt.subplots_adjust(wspace=0)
    #fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
    #fig.subplots_adjust(left=0.3, bottom=0.3, right=0.3, top=0.3, wspace=0.3, hspace=0.3)
    #fig.tight_layout()
    
    return rendered_image_files_list

def sorted_boxplot_heatmap_figure_rcbv(df_1_rcbv, \
                                    df_2_rcbv, \
                                    df_3_rcbv, \
                                    df_4_rcbv, \
                                  ylabel_1, \
                                  ylabel_2, \
                                  ylabel_3, \
                                  ylabel_4, \
                                  distance_name, \
                                  labels_data, \
                                  labels_dims, \
                                  CBV_out_dir, \
                                  rendered_image_files_list, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  ascending1=False, \
                                  ascending2=False, \
                                  ascending3=False, \
                                  ascending4=False, \
                                  top = "all", \
                                  render_pngs = True, \
                                  windowMin = 0, \
                                  windowMax = 1*0.8, \
                                  interpolation = "nearest", \
                                  cmap = "hot", \
                                  blur_3d = False, \
                                  blur_3d_sigma = 1, \
                                  method_comparison = False):
    
    fig = plt.figure(figsize=np.array([9, 10]))
    
    gs1 = gridspec.GridSpec(4, 3)
    gs1.update(left=0.08, right=0.48, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    ax1 = plt.subplot(gs1[0, :])
    medians_df_1 = sorted_boxplot_relative_rcbv_change(df_1_rcbv, \
                                       ax1, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ascending=ascending1, \
                                       ylabel2="", \
                                       ylabel="rCBV change", \
                                       title="", \
                                       xlabel="", 
                                       top=top)
    
    #ax2 = plt.subplot(gs1[1, :])
    medians_df_2 = sorted_medians(df_2_rcbv, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  ascending=ascending2, \
                                  top=top)
    
    ax3 = plt.subplot(gs1[2, :])
    medians_df_3 = sorted_boxplot_relative_rcbv_change(df_3_rcbv, \
                                       ax3, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ascending=ascending3, \
                                       ylabel2="", \
                                       ylabel="rCBV change", \
                                       title="", \
                                       xlabel="", \
                                       top=top)
    #ax4 = plt.subplot(gs1[3, :])
    medians_df_4 = sorted_medians(df_4_rcbv, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  ascending=ascending4, \
                                  top=top)
    
    
    if ascending1:
        medians_df_1 = 1/medians_df_1
    if ascending2:
        medians_df_2 = 1/medians_df_2
    if ascending3:
        medians_df_3 = 1/medians_df_3
    if ascending4:
        medians_df_4 = 1/medians_df_4
    
    gs2 = gridspec.GridSpec(4, 2)
    gs2.update(left=0.52, right=0.99, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    
    if render_pngs:
        rendered_image_files_list = []
    
    
    # Render pngs for medians_df_1
    if render_pngs:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        render_regions_set_to_pngs(medians_df_1, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r1", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r1_png_file_1]
        rendered_image_files_list += [r1_png_file_2]
        rendered_image_files_list += [r1_png_file_3]
    else:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        rendered_image_files_list[0], \
        rendered_image_files_list[1], \
        rendered_image_files_list[2]
        
    ax5 = plt.subplot(gs2[0, 0])
    png_1=mpimg.imread(r1_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_1, rotation=-90, color="blue", fontsize="medium")
    
    ax6 = plt.subplot(gs2[0, 1])
    png_2=mpimg.imread(r1_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax7 = plt.subplot(gs2[0, 2])
    png_3=mpimg.imread(r1_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    # Render pngs for medians_df_2
    if render_pngs:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        render_regions_set_to_pngs(medians_df_2, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r2", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r2_png_file_1]
        rendered_image_files_list += [r2_png_file_2]
        rendered_image_files_list += [r2_png_file_3]
    else:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        rendered_image_files_list[3], \
        rendered_image_files_list[4], \
        rendered_image_files_list[5]
    
    ax8 = plt.subplot(gs2[1, 0])
    png_1=mpimg.imread(r2_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_2, rotation=-90, color="blue", fontsize="medium")
    
    ax9 = plt.subplot(gs2[1, 1])
    png_2=mpimg.imread(r2_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax10 = plt.subplot(gs2[1, 2])
    png_3=mpimg.imread(r2_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for medians_df_3
    if render_pngs:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        render_regions_set_to_pngs(medians_df_3, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r3", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r3_png_file_1]
        rendered_image_files_list += [r3_png_file_2]
        rendered_image_files_list += [r3_png_file_3]
    else:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        rendered_image_files_list[6], \
        rendered_image_files_list[7], \
        rendered_image_files_list[8]
    
    ax11 = plt.subplot(gs2[2, 0])
    png_1=mpimg.imread(r3_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_3, rotation=-90, color="blue", fontsize="medium")
    
    ax12 = plt.subplot(gs2[2, 1])
    png_2=mpimg.imread(r3_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax13 = plt.subplot(gs2[2, 2])
    png_3=mpimg.imread(r3_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for medians_df_4
    if render_pngs:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        render_regions_set_to_pngs(medians_df_4, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r4", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r4_png_file_1]
        rendered_image_files_list += [r4_png_file_2]
        rendered_image_files_list += [r4_png_file_3]
    else:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        rendered_image_files_list[9], \
        rendered_image_files_list[10], \
        rendered_image_files_list[11]
    
    ax14 = plt.subplot(gs2[3, 0])
    png_1=mpimg.imread(r4_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.title("axial \ninferior-superior", y=-0.4)
    plt.text(x=-150, y=772 + 772//10, s=ylabel_4, rotation=-90, color="blue", fontsize="medium")
    
    ax15 = plt.subplot(gs2[3, 1])
    png_2=mpimg.imread(r4_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    plt.title("sagittal \nright-left", y=-0.4)
    """
    ax16 = plt.subplot(gs2[3, 2])
    png_3=mpimg.imread(r4_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    plt.title("mixed \nright-left \nanterior-posterior", y=-0.4)
    """
    # Common x axis
    #fig.text(0.5, 0.04, 'common X', ha='center')
    # Common y axis
    #fig.text(0.01, 0.5, distance_name + " distance", va="center", rotation="vertical")
    # Box plots supertitle
    #fig.text(0.135, 0.975, "Top " + str(top) + " changing regions")
    # Images supertitle
    #if method_comparison:
    #    fig.text(0.6, 0.95, "Regions most different between correction \nmethods. Based on all median values")
    #else:
    #    fig.text(0.6, 0.95, "Regions most affected \nby correction. Based on all median values")
    """
    # Supertitle
    if ascending1 and ascending2 and ascending3 and ascending4:
        fig.suptitle("rCBV decrease by corrections")
    else:
        fig.suptitle("rCBV increase by corrections")
    if method_comparison:
        fig.suptitle("rCBV increase and decrease between TOPUP and EPIC corrections")
    """
    #plt.subplots_adjust(wspace=0)
    #fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
    #fig.subplots_adjust(left=0.3, bottom=0.3, right=0.3, top=0.3, wspace=0.3, hspace=0.3)
    #fig.tight_layout()
    
    return rendered_image_files_list

def sorted_boxplot_heatmap_figure_rcbv_all(df_1_rcbv, \
                                    df_2_rcbv, \
                                    df_3_rcbv, \
                                    df_4_rcbv, \
                                  ylabel_1, \
                                  ylabel_2, \
                                  ylabel_3, \
                                  ylabel_4, \
                                  distance_name, \
                                  labels_data, \
                                  labels_dims, \
                                  CBV_out_dir, \
                                  rendered_image_files_list, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  ascending1=False, \
                                  ascending2=False, \
                                  ascending3=False, \
                                  ascending4=False, \
                                  top = "all", \
                                  render_pngs = True, \
                                  windowMin = 0, \
                                  windowMax = 1*0.8, \
                                  interpolation = "nearest", \
                                  cmap = "hot", \
                                  blur_3d = False, \
                                  blur_3d_sigma = 1, \
                                  method_comparison = False):
    
    fig = plt.figure(figsize=np.array([9, 10*4]))
    
    gs1 = gridspec.GridSpec(4, 3)
    gs1.update(left=0.08, right=0.48, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    ax1 = plt.subplot(gs1[0, :])
    medians_df_1 = sorted_boxplot_relative_rcbv_change(df_1_rcbv, \
                                       ax1, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ascending=ascending1, \
                                       ylabel2="", \
                                       ylabel="rCBV change", \
                                       title="", \
                                       xlabel="", 
                                       top=top)
    
    ax2 = plt.subplot(gs1[1, :])
    """
    medians_df_2 = sorted_medians(df_2_rcbv, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  ascending=ascending2, \
                                  top=top)
    """
    medians_df_2 = sorted_boxplot_relative_rcbv_change(df_2_rcbv, \
                                       ax2, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ascending=ascending2, \
                                       ylabel2="", \
                                       ylabel="rCBV change", \
                                       title="", \
                                       xlabel="", 
                                       top=top)
    
    ax3 = plt.subplot(gs1[2, :])
    medians_df_3 = sorted_boxplot_relative_rcbv_change(df_3_rcbv, \
                                       ax3, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ascending=ascending3, \
                                       ylabel2="", \
                                       ylabel="rCBV change", \
                                       title="", \
                                       xlabel="", \
                                       top=top)
    ax4 = plt.subplot(gs1[3, :])
    """
    medians_df_4 = sorted_medians(df_4_rcbv, \
                                  region_values, \
                                  region_names, \
                                  region_names_to_exclude, \
                                  ascending=ascending4, \
                                  top=top)
    """
    medians_df_4 = sorted_boxplot_relative_rcbv_change(df_4_rcbv, \
                                       ax4, \
                                       region_values, \
                                       region_names, \
                                       region_names_to_exclude, \
                                       ascending=ascending4, \
                                       ylabel2="", \
                                       ylabel="rCBV change", \
                                       title="", \
                                       xlabel="", \
                                       top=top)
    
    
    if ascending1:
        medians_df_1 = 1/medians_df_1
    if ascending2:
        medians_df_2 = 1/medians_df_2
    if ascending3:
        medians_df_3 = 1/medians_df_3
    if ascending4:
        medians_df_4 = 1/medians_df_4
    
    gs2 = gridspec.GridSpec(4, 2)
    gs2.update(left=0.52, right=0.99, bottom=0.07, top=0.92, hspace=0.5, wspace=0)
    
    
    if render_pngs:
        rendered_image_files_list = []
    
    
    # Render pngs for medians_df_1
    if render_pngs:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        render_regions_set_to_pngs(medians_df_1, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r1", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r1_png_file_1]
        rendered_image_files_list += [r1_png_file_2]
        rendered_image_files_list += [r1_png_file_3]
    else:
        r1_png_file_1, \
        r1_png_file_2, \
        r1_png_file_3 = \
        rendered_image_files_list[0], \
        rendered_image_files_list[1], \
        rendered_image_files_list[2]
        
    ax5 = plt.subplot(gs2[0, 0])
    png_1=mpimg.imread(r1_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_1, rotation=-90, color="blue", fontsize="medium")
    
    ax6 = plt.subplot(gs2[0, 1])
    png_2=mpimg.imread(r1_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax7 = plt.subplot(gs2[0, 2])
    png_3=mpimg.imread(r1_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    # Render pngs for medians_df_2
    if render_pngs:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        render_regions_set_to_pngs(medians_df_2, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r2", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r2_png_file_1]
        rendered_image_files_list += [r2_png_file_2]
        rendered_image_files_list += [r2_png_file_3]
    else:
        r2_png_file_1, \
        r2_png_file_2, \
        r2_png_file_3 = \
        rendered_image_files_list[3], \
        rendered_image_files_list[4], \
        rendered_image_files_list[5]
    
    ax8 = plt.subplot(gs2[1, 0])
    png_1=mpimg.imread(r2_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_2, rotation=-90, color="blue", fontsize="medium")
    
    ax9 = plt.subplot(gs2[1, 1])
    png_2=mpimg.imread(r2_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax10 = plt.subplot(gs2[1, 2])
    png_3=mpimg.imread(r2_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for medians_df_3
    if render_pngs:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        render_regions_set_to_pngs(medians_df_3, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r3", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r3_png_file_1]
        rendered_image_files_list += [r3_png_file_2]
        rendered_image_files_list += [r3_png_file_3]
    else:
        r3_png_file_1, \
        r3_png_file_2, \
        r3_png_file_3 = \
        rendered_image_files_list[6], \
        rendered_image_files_list[7], \
        rendered_image_files_list[8]
    
    ax11 = plt.subplot(gs2[2, 0])
    png_1=mpimg.imread(r3_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.text(x=-150, y=772 + 772//10, s=ylabel_3, rotation=-90, color="blue", fontsize="medium")
    
    ax12 = plt.subplot(gs2[2, 1])
    png_2=mpimg.imread(r3_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    """
    ax13 = plt.subplot(gs2[2, 2])
    png_3=mpimg.imread(r3_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    """
    
    # Render pngs for medians_df_4
    if render_pngs:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        render_regions_set_to_pngs(medians_df_4, \
                                   labels_data, \
                                   labels_dims, \
                                   CBV_out_dir, \
                                   png_prefix=distance_name + "-r4", \
                                   interpolation=interpolation, \
                                   cmap=cmap, \
                                   windowMin=windowMin, \
                                   windowMax=windowMax, \
                                   blur_3d=blur_3d, \
                                   blur_3d_sigma=blur_3d_sigma)
        
        rendered_image_files_list += [r4_png_file_1]
        rendered_image_files_list += [r4_png_file_2]
        rendered_image_files_list += [r4_png_file_3]
    else:
        r4_png_file_1, \
        r4_png_file_2, \
        r4_png_file_3 = \
        rendered_image_files_list[9], \
        rendered_image_files_list[10], \
        rendered_image_files_list[11]
    
    ax14 = plt.subplot(gs2[3, 0])
    png_1=mpimg.imread(r4_png_file_1)
    plt.imshow(png_1, aspect="equal")
    plt.axis("off")
    plt.title("axial \ninferior-superior", y=-0.4)
    plt.text(x=-150, y=772 + 772//10, s=ylabel_4, rotation=-90, color="blue", fontsize="medium")
    
    ax15 = plt.subplot(gs2[3, 1])
    png_2=mpimg.imread(r4_png_file_2)
    plt.imshow(png_2, aspect="equal")
    plt.axis("off")
    plt.title("sagittal \nright-left", y=-0.4)
    """
    ax16 = plt.subplot(gs2[3, 2])
    png_3=mpimg.imread(r4_png_file_3)
    plt.imshow(png_3, aspect="equal")
    plt.axis("off")
    plt.title("mixed \nright-left \nanterior-posterior", y=-0.4)
    """
    # Common x axis
    #fig.text(0.5, 0.04, 'common X', ha='center')
    # Common y axis
    #fig.text(0.01, 0.5, distance_name + " distance", va="center", rotation="vertical")
    # Box plots supertitle
    #fig.text(0.135, 0.975, "Top " + str(top) + " changing regions")
    # Images supertitle
    #if method_comparison:
    #    fig.text(0.6, 0.95, "Regions most different between correction \nmethods. Based on all median values")
    #else:
    #    fig.text(0.6, 0.95, "Regions most affected \nby correction. Based on all median values")
    """
    # Supertitle
    if ascending1 and ascending2 and ascending3 and ascending4:
        fig.suptitle("rCBV decrease by corrections")
    else:
        fig.suptitle("rCBV increase by corrections")
    if method_comparison:
        fig.suptitle("rCBV increase and decrease between TOPUP and EPIC corrections")
    """
    #plt.subplots_adjust(wspace=0)
    #fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
    #fig.subplots_adjust(left=0.3, bottom=0.3, right=0.3, top=0.3, wspace=0.3, hspace=0.3)
    #fig.tight_layout()
    
    return rendered_image_files_list
