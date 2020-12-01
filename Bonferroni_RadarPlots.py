#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 09:11:56 2020

@author: felixrenard@gmail.com
"""

from scipy import ndimage
import scipy.stats as st
import nibabel as nib
from glob import glob
import numpy as np
from scipy.ndimage import label, generate_binary_structure
import pandas as pd
import sys

rep = sys.argv[-2]  # type: str
name_modality = sys.argv[-1]  # modality

# constant definition
cross = generate_binary_structure(3, 1)

# Different kind of threshold for the zscore and the corresponding p-value
# It is for one tailed zscore.
# threshold = -1.65 # 1.65 zscore -> 0.95 p-val
# threshold = -2.33 # 2.33 zscore -> 0.99 p-val
threshold = -4.8  # 3.09 zscore -> 0.999 p-val


def filter_isolated_cells(array, struct):
    """ Return array with completely isolated single cells removed
    :param array: Array with completely isolated single cells
    :param struct: Structure array for generating unique regions
    :return: Array with minimum region size > 1
    """
    filtered_array = np.copy(array)
    id_regions, num_ids = ndimage.label(filtered_array, structure=struct)
    id_sizes = np.array(ndimage.sum(array, id_regions, range(num_ids + 1)))
    area_mask = (id_sizes == 1)
    filtered_array[area_mask[id_regions]] = 0
    return filtered_array


# Get the name of the different patient
# We check on the CC_3 track since it is really robust Using TractSeg

file_name = glob(rep + "/zscore_CC_3*" + name_modality + "*.nii.gz")
file_name.sort()
name_patient = [name.split("CC_3_")[1].split("_")[0] for name in file_name]
nb_patient = len(file_name)

ROI_name = ['AF_left', 'AF_right', 'ATR_left', 'ATR_right', 'CC_1', 'CC_2', 'CC_3', 'CC_4', 'CC_5',
            'CC_6', 'CC_7', 'CG_left', 'CG_right', 'CST_left', 'CST_right', 'FPT_left', 'FPT_right',
            'ICP_left', 'ICP_right', 'IFO_left', 'IFO_right', 'ILF_left', 'ILF_right', 'MCP',
            'MLF_left', 'MLF_right', 'OR_left', 'OR_right', 'POPT_left', 'POPT_right', 'SCP_left', 'SCP_right',
            'SLF_III_left', 'SLF_III_right', 'SLF_II_left', 'SLF_II_right', 'SLF_I_left', 'SLF_I_right',
            'STR_left', 'STR_right', 'ST_FO_left', 'ST_FO_right', 'ST_OCC_left', 'ST_OCC_right',
            'ST_PAR_left', 'ST_PAR_right', 'ST_POSTC_left', 'ST_POSTC_right',
            'ST_PREC_left', 'ST_PREC_right', 'ST_PREF_left', 'ST_PREF_right', 'ST_PREM_left', 'ST_PREM_right',
            'T_OCC_left', 'T_OCC_right', 'T_PAR_left', 'T_PAR_right',
            'T_POSTC_left', 'T_POSTC_right', 'T_PREC_left', 'T_PREC_right', 'T_PREF_left',
            'T_PREF_right', 'T_PREM_left', 'T_PREM_right', 'UF_left', 'UF_right']

# Load one image of the zscore to get the affine parameter
ima = nib.load(file_name[0])
IMA = ima.get_data()
aff = ima.get_affine()
Zscore_all = np.zeros(ima.shape)

###########
############ Estimate the number of damaged voxels with Bonferroni correction
############

data = np.zeros([nb_patient, len(ROI_name), 4])

for k in range(nb_patient):
    for i in range(len(ROI_name)):
        ima_name = "zscore_" + ROI_name[i] + "_" + name_patient[k] + "_" + name_modality + "_80.nii.gz"
        print(ima_name)
        IMA_ = nib.load(ima_name).get_data()
        size_track = float(len(np.where(IMA_)[0]))
        IMA_bin = np.zeros(IMA_.shape)
        # estimate the Bonferroni correction
        threshold = st.norm.ppf(.05 / size_track)
        # Clean the zscore image
        IMA_bin[np.where(IMA_ < threshold)] = 1
        IMA_bin = filter_isolated_cells(IMA_bin, cross)
        # Save the cleaned image
        IMA_nib = nib.Nifti1Image(IMA_bin, aff)
        nib.save(IMA_nib, "zscore_maskBonf_" + ROI_name[i] + "_" + name_patient[k] + "_" + name_modality + ".nii.gz")
        # estimate the different quantitative measures
        # the label function determines the number of lesions
        A, B = label(IMA_bin)
        size_les = []
        for j in range(1, B + 1):
            size_les.append(len(np.where(A == j)[0]))
        #To estimate not the percentage but the number of voxels, remove the /size_track
        data[k, i, 0] = len(np.where(IMA_bin)[0]) / size_track
        data[k, i, 1] = B
        if B > 1:
        #To estimate not the percentage but the number of voxels, remove the /size_track
            data[k, i, 2] = np.max(size_les) / size_track
            data[k, i, 3] = len(np.where(np.array(size_les) > 5)[0])
        else:
            data[k, i, 2] = 0
            data[k, i, 3] = 0
    # create a dataframe to save the quantitative measures
    df = pd.DataFrame(data=data[k, :, :], columns=['all_voxels', 'nb lesions', 'max lesions', 'nb_lesions_large'])
    df.index = ROI_name
    df.to_excel(rep + "xls_" + name_patient[k] + "_" + name_modality + ".xls")

####RADAR plot
# Libraries
import matplotlib.pyplot as plt
from math import pi
import numpy as np


# ------- PART 1: Create background
N = len(ROI_name)
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]


for i in range(nb_patient):
    #data_tmp corresponds to the data to display
    data_tmp = data[i,:,0]
    # Initialise the spider plot
    fig = plt.figure(figsize=(20, 10))
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rmax(15)
    ax.set_rticks([])

    # Draw one axe per variable + add labels labels yet
    # plt.xticks(angles, ROI_name)

    ax.set_xticks(angles)
    ax.set_xticklabels(ROI_name, fontsize=10)
    plt.gcf().canvas.draw()

    labels = []
    for label_, angle in zip(ax.get_xticklabels(), np.rad2deg(angles)):
        x, y = label_.get_position()
        lab = ax.text(x, y - .35, label_.get_text(), transform=label_.get_transform(),
                      ha=label_.get_ha(), va=label_.get_va())
        if 0 <= angle < 180:
            lab.set_rotation(-angle + 90)
        if 180 <= angle < 360:
            lab.set_rotation(-angle - 90)
        labels.append(label_)
    ax.set_xticklabels([])

    plt.subplots_adjust(top=0.68, bottom=0.32, left=0.05, right=0.95)

    # Draw ylabels
    ax.set_rlabel_position(0)
    #Correspond to the percentage
    plt.yticks([15, 10, 5, 3], ["15", "10", "5", "3"], color="grey", size=10)
    plt.ylim(0, 20)

    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable

    # Multiply by 100 because it is in percentage / Remove *100 if you are not in percentage anymore
    values = data_tmp * 100
    values = values.flatten().tolist()
    values += values[:1]
    #you can change the label of the radar plot here in label
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=name_modality)
    ax.fill(angles, values, 'b', alpha=0.1)

    plt.legend(loc='upper right', bbox_to_anchor=(-0.5, 0.1))
    plt.title(name_patient[i])
    plt.show()
    #Here we give the name all voxels lesion since we regard data[i,:,0]
    plt.savefig(name_patient[i] + '_radarplot_allvoxels_lesion_' + name_modality + '.png')
    plt.close('all')
