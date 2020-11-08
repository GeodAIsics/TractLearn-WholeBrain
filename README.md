# TractLearn: The Manifold Learning toolbox for precision medicine

TractLearn is unified statistical framework for Diffusion-weighted MRI quantitative analyses by using geodesic learning as a data-driven learning task. It aims to increase the sensitivity in detecting voxels abnormalities in case-controlled and/or longitudinal medical studies. 

TractLearn can detect global variation of voxels quantitative values, which means that all the voxels interaction in a brain bundle are considered rather than analyzing each voxel independently. More details can be found here: https://www.medrxiv.org/content/10.1101/2020.05.27.20113027v1

While the code is mainly based on Python librairies, first steps can also be computed using Shell command lines. We are then providing both Python and Unix scripts.
As the prior paper use TractLearn based on a first step of major brain bundles segmentation using TractSeg, we will provide scripts starting from typical outputs of TractSeg, ie. tck files generation using Deep Learning. For more information about TractSeg please refer to:

https://github.com/MIC-DKFZ/TractSeg

It is worthwhile to keep in mind that TractLearn can also be relevant on a unique anatomical region, for example after manual extraction using ROIs. In this case, you can start directly with the Step 4 in the template space.

## Step 1: Subjects coregistration

As TractLearn requires an excellent matching between subjects, the first steps imply non-linear coregistration in a common template space. 
Here we assume that you have already created a template using for example population_template coming from MRtrix (https://www.mrtrix.org/).
We provide the python code to coregister each subject Fiber Orientation Distribution (FOD) maps into the template space, saving in the same time the warp files (deformation fields) into a folder named warped_template. All the registered FODs will be saved into a folder named transformed_template.

Please note that the folders warped_template and transformed_template need to be created before launching this python script (the folders should be created in the same directory than the script). The working directory should also contain the template file, here named template_FOD.nii.gz.

You need to launch:
```
python 2_Register_fod2template_nomask.py
```

## Step 2: Track files registration in the common template space

At this step, you need the inverse of the transformation required for images for track files (tck) registration. The following python script will automatically invert all transformations using warpconvert and warpinvert (MRtrix commandlines). Keep in mind that you need to have already created two folders: /transformed_template including the coregistered WM files and /warped_template including the warps files/

Just launch:

```
python 3_Invert_warp.py
```

## Step 3: Transformation application for all TractSeg bundles

The next step is to use tcktransform command (always coming from MRtrix) on all tck files using:
```
python 4_Register_track.py
```

Note that you need to add the working directory at the end of the line, for example:

python 4_Register_track.py ./MyData/

## Step 4: Estimation of the different scalar coefficients in the template space

In the initial TractLearn paper, we have proposed to extract 4 biomarkers from each patient bundle:
1/The track-weighted contrast based on FOD amplitude (TW-FOD)
2/The track-weighted contrast based on FA amplitude (TW-FA)
3/Fractional Anisotropy (FA)
4/Apparent Fiber Density (AFD) coefficient) 

The following script proposes to automatically convert track files into images files for these coefficients using tckmap and afdconnectivity from MRtrix 

```
python 5_Register_FA.py
```

## Step 5: Mask calculation for all the subjects

For each bundle, 80% of maximum of the TDI intensity is considered to perform a subject mask. The reason was given in the manuscript: Indeed, while the coregistration based on FOD symmetric diffeomorphic has allow to match major brain bundles, we have noticed that cortical variability made more difficult a perfect matching for the entire bundle. Absence of this step could potentially lead to false positive lesions on the bundles boundaries. 

In addition, as TractSeg tends to produce bundle overlaying (i.e some boundaries voxels can be linked to two different bundles), using a thresholding has allowed to precisely locate abnormalities.

The intersection of all the masks corresponds to the mask of analysis.

```
python 5_Register_FA.py
```

At this step, you have to make an important choice: you can obtain from TractLearn either Z Score analysis in you want to compare ONE individual versus a group fo controls or t tests analysis if you want to compare two groups together. In both cases you will beneficiate from the high sensitivity of TractLearn to detect voxel abnormalities and its capability to limit false positive findings by taken into account the variability of your control group.

The first case (Z score) appears particularly relevant when:

1/You have a mismatch between your number of controls and patients
2/You have included patients with complex disease potentially including several subforms (eg. multiple sclerosis, frontotemporal dementia....)
3/You are interest by precision medicine / trajectories medicine for longitudinal studies

Obtaining separate analysis for each individual can for example help to identify imaging profile, longitudinal changes during therapy...

The second case (t tests) is generally useful when you want to test a pathophysiological hypothesis at the group level with homogeneous population

## Step 6: Estimate z-score maps (group versus individuals)




## Step 7: Estimate t-test maps (group vs group studies)
