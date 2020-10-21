# TractLearn: The Manifold Learning toolbox for precision medicine

TractLearn is unified statistical framework for Diffusion-weighted MRI quantitative analyses by using geodesic learning as a data-driven learning task. It aims to increase the sensitivity in detecting voxels abnormalities in case-controlled medical studies. 

TractLearn can detect global variation of voxels quantitative values, which means that all the voxels interaction in a brain bundle are considered rather than analyzing each voxel independently. More details can be found here: https://www.medrxiv.org/content/10.1101/2020.05.27.20113027v1

While the code is mainly based on Python librairies, first steps can also be computed using Shell command lines. We are then providing both Python and Unix scripts.
Here the TractLearn use implies a first step of major brain bundles segmentation using TractSeg. For more information about TractSeg please refer to:

https://github.com/MIC-DKFZ/TractSeg

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

At this step, you need the inverse of the transformation required for images for track files (tck) registration. The following python script will automatically invert all transformations using warpconvert and warpinvert (MRtrix commandlines). Keep in mind that you need to have already two folders: /transformed_template including the coregistered WM files and /warped_template including the warps files

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

The following script propose to automatically convert track files into images files for these coefficients using tckmap and afdconnectivity from MRtrix 

```
python 5_Register_FA.py
```



## Step 5: Mask calculation for all the subjects

For each bundle, 80% of maximum of the TDI intensity is considered to perform a subject mask. 
The intersection of all the masks corresponds to the mask of analysis.

## Step 6: Estimate z-score maps (group versus individuals)

## Step 7: Estimate t-test maps (group vs group studies)
