# TractLearn: The Manifold Learning toolbox for precision medicine. Whole Brain version.

TractLearn is an unified statistical framework for Diffusion-weighted MRI quantitative analyses by using geodesic learning as a data-driven learning task. It aims to increase the sensitivity in detecting voxels abnormalities in case-controlled and/or longitudinal medical studies. 

![alt text](https://geodaisics.files.wordpress.com/2020/11/tractlearnexample.png "Example of TractLearn application to localize brain abnormality in a trauma patient") 

TractLearn can detect global variation of voxels quantitative values, which means that all the voxels interaction in a brain bundle are considered rather than analyzing each voxel independently. The second advantage over usual voxelwise analysis is to take into account healthy volunteers variability as reference rather than using classical Euclidean mean. More details can be found here: https://www.medrxiv.org/content/10.1101/2020.05.27.20113027v1

While the code is mainly based on Python librairies, first steps can also be computed using Shell. We are then providing both Python and Shell scripts coming from MRtrix3 (https://www.mrtrix.org/). Here we propose to apply TractLearn based on a first step of brain bundles segmentation using TractSeg, a Deep Learning-based open source tool. For more information about TractSeg please refer to: https://github.com/MIC-DKFZ/TractSeg. We will then provide scripts starting from typical outputs of TractSeg, ie. tck files from 72 brain bundles, as stored in tractseg_output/TOM_tracking (though the pipeline also worked in case of incomplete execution of TractSeg, eg. with only 60 brain bundles). 

It is worthwhile to keep in mind that TractLearn can also be relevant on a unique anatomical region (either in the brain or not), for example after manual extraction using ROIs. The pipeline for Single Structure management will be soon published.

## Step 1: Subjects coregistration

As TractLearn requires an excellent matching between subjects, the first steps imply non-linear coregistration in a common template space. 
Here we assume that you have already created a template using for example population_template coming from MRtrix (https://www.mrtrix.org/).

We provide the Python code to coregister each subject Fiber Orientation Distribution (FOD) maps into the template space. The output will be the transformed FOD maps and the warp files (deformation fields). 

This script takes as input all the individual FOD maps. They need to be stored into a Data Directory (we assume that the Data directory includes all subjects before TractLearn execution and that the working directory is the location to execute TractLearn). The TractLearn directory should contain the template file (here named template_FOD.nii.gz) + Python scripts.

The Data directory needs to contain all your subjects as a collection of individual folders. Please also note that in case of case-controlled studies, you need to name your folders using a common prefix for controls (for example Control*) and for patients using a different prefix (eg. Patient*).
Each folder has to include the directory tractseg_output/TOM_tracking + FOD maps (same name for all FOD maps without prefix identification).

We provide on overview about the folders organization:

![alt text](https://geodaisics.files.wordpress.com/2020/12/tractlearn.png "TractLearn directory tree view") 

![alt text](https://geodaisics.files.wordpress.com/2020/12/data.png "Data directory tree view") 

You need to add the Data directory at the end of the line + the FOD image Name (eg. wmfod.mif)

```
python Register_fod2template.py ./DataDirectory/ FOD_image_Name
```

Input: One folder Data_directory/ containing the template file + Python scripts and one folder Data_directory/ containing all individual files (FOD maps +  tractseg_output/TOM_tracking).
Output: In the folder TractLearn_directory/transformed_template, all transformed FOD maps. In the folder TractLearn_directory/warp_template, all the warp files.


## Step 2: Track files registration in the template space

At this step, you need the inverse of the transformation previously required for images, so as to apply on track files (tck) for registration in the same space. 
The following python script will automatically invert all transformations using warpconvert and warpinvert (MRtrix commands). 

Just launch:

```
python Invert_warp.py
```

The next step is to use tcktransform command (always coming from MRtrix) on all tck files to coregister all the tck files into a common template space. Note that you need to add the Data directory at the end of the line, for example:
```
python Register_track.py ./DataDirectory/
```

## Step 3: Estimation of the different scalar coefficients in the template space

In the initial TractLearn paper, we have proposed to extract 4 biomarkers from each patient bundle:

1/The track-weighted contrast based on FOD amplitude (TW-FOD)
2/The track-weighted contrast based on FA amplitude (TW-FA)
3/Fractional Anisotropy (FA)
4/Apparent Fiber Density (AFD) coefficient) 

FA analysis does firstly require to coregister all individual FA maps (named FA_MNI.nii.gz as it is assumed to be in the MNI space for TractSeg)

```
python Register_FA.py ./DataDirectory/
```

The following script proposes to automatically convert track files into images files for TW-FOD, TW-FA and AFD using tckmap and afdconnectivity:

```
python Register_TWI_FOD.py
```

As the output will generate a high number of files, we propose to postprocess individuals by group of 10 using this nomenclature:

```
python Register_TWI_FOD.py 0
```

For processing Folder 1 to Folder 10 (alphabetical order!) 

```
python Register_TWI_FOD.py 1
```

For processing Folder 11 to Folder 20

In case you have for example 25 subjects to postprocess, you need to launch respectively:

```
python Register_TWI_FOD.py 0
```
```
python Register_TWI_FOD.py 1
```
```
python Register_TWI_FOD.py 2
```

## Step 4: Mask calculation for all subjects

For each bundle, 80% of maximum of the Track Density Imaging intensity is considered to perform a subject mask. The reason was given in the manuscript: Indeed, while the coregistration based on FOD symmetric diffeomorphic has allow to match major brain bundles, we have noticed that cortical variability made more difficult a perfect matching for the entire bundle. Absence of this step could potentially lead to false positive lesions on the bundles boundaries. 

In addition, as TractSeg tends to produce bundle overlaying (i.e some boundaries voxels can be linked to two different brain bundles), using a thresholding has allowed to precisely locate abnormalities.

The intersection of all individual masks corresponds to the mask of analysis. 2 scripts are successfully needed:

```
python Convert_mask_percentile.py 0
```
This first script processes bundles by series of 300. If for example you have 1400 bundles (20 subjects with 70 bundles each), you need to launch:

```
python Convert_mask_percentile.py 0
```
```
python Convert_mask_percentile.py 1
```
```
python Convert_mask_percentile.py 2
```
```
python Convert_mask_percentile.py 3
```
```
python Convert_mask_percentile.py 4
```

The second script doesn't require any additional argument.

```
python Convert_mask_percentile_phase2.py
```
You will obtain a new subfolder named "stat" where the Z-Score and/or t-test maps will be further saved.


## Step 5: Obtaining your quantitative analysis using a Riemaniann framework

At this step, you have to make an important choice: you can obtain from TractLearn either Z Score analysis in you want to compare ONE individual versus a group of controls or t-tests analysis if you want to compare two groups together. In both cases you will beneficiate from the high sensitivity of TractLearn to detect voxel abnormalities and its capability to limit false positive findings by taken into account the variability of your control group.

The first case (Z score) appears particularly relevant when:

1/You have a mismatch between your number of controls and patients
2/You have included patients with complex disease potentially including several subforms (eg. multiple sclerosis, frontotemporal dementia....)
3/You are interest by precision medicine / trajectories medicine for longitudinal studies

Obtaining separate analysis for each individual can for example help to identify imaging profile, longitudinal changes during therapy...

The second case (t-tests) is generally useful when you want to test a pathophysiological hypothesis at the group level with homogeneous population

Note that in both cases you need The Nadaraya-Watson kernel script (NW_regression.py) at the same folder level that either Z-Score or t-tests Python scripts.

## First possibility: Estimate z-score maps (individual vs group)

```
python zscore.py Patient_Prefix Control_Prefix Biomarker
```

Don't forget to precise the common prefix for patients then controls + the biomarker of your choice (among TW-FOD, TW-FA, AFD and Fractional for FA only)


## Second possibility: Estimate t-test maps (group vs group studies)

```
python ttest.py Patient_Prefix Control_Prefix Biomarker
```
This script will provide the p-values. The following script aims at creating the lesions maps in the template space + Radar plots to provide an overview of the number of altered voxels:

```
python RadarPlots_ttest.py
```
We also provide an alternative version for the last script providing a Bonferroni correction for multiple comparison. Please note that correction for mulitple comparison is not really adapted for applying on TractLearn, as we provide a global statistical test for which voxels are not analyzed independently. However, as the literature is still sparse on this subject in medicine, reviewers can ask for correction.

```
python Bonferroni_RadarPlots_ttest.py
```





