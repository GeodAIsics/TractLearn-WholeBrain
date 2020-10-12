# TractLearn: The Manifold Learning toolbox for precision medicine

TractLearn is unified statistical framework for Diffusion-weighted MRI quantitative analyses by using geodesic learning as a data-driven learning task. It aims to increase the sensitivity in detecting voxels abnormalities in case-controlled medical studies. 

TractLearn can detect global variation of voxels quantitative values, which means that all the voxels interaction in a brain bundle are considered rather than analyzing each voxel independently. More details can be found here: https://www.medrxiv.org/content/10.1101/2020.05.27.20113027v1

While the code is mainly based on Python librairies, first steps can also be computed using Shell command lines. We are then providing both Python and Unix scripts.
Here the TractLearn use implies a first step of major brain bundles segmentation using TractSeg. For more information about TractSeg please refer to:

## Step 1: Subjects coregistration

As TractLearn requires an excellent matching between subjects, the first steps imply non linear coregistration in a common template space. 
Here we assume that you have already created a template using for example population_template coming from MRtrix.
We provide the python code to coregister each subject Fiber Orientation Distribution (FOD) into the template space, saving in the same time the warp files (deformation fields) into a folder named warped_template. All the registered FODs will be saved into a folder named transformed_template.

Please note that the folders warped_template and transformed_template need to be created before launching this python script (at the same level). The working directory should also contain the template file, here named template_FOD.nii.gz.

https://github.com/GeodAIsics/TractLearn/blob/master/2_Register_fod2template_nomask.py

## Step 2: Track files registration in the common template space

At this step, you need the inverse of the transformation required for images 

## Step 3: Transformation application for all TractSeg bundles

## Step 4: Estimation of the different scalar coefficients in the template space

For each bundle of each patient, the TDI, TW-FOD, TW-FA and AFD coefficients are estimated.

## Step 5: Mask calculation for all the subjects

For each bundle, 80% of maximum of the TDI intensity is considered to perform a subject mask. 
The intersection of all the masks corresponds to the mask of analysis.

## Step 6: Estimate z-score maps (group versus individuals)

## Step 7: Estimate t-test maps (group vs group studies)
