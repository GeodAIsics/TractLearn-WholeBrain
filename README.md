# TractLearn

TractLearn is unified statistical framework for Diffusion-weighted MRI quantitative analyses by using geodesic learning as a data-driven learning task. It aims to increase the sensitivity in detecting voxels abnormalities in case-controlled medical studies. 

TractLearn can detect global variation of voxels quantitative values, which means that all the voxels interaction in a brain bundle are considered rather than analyzing each voxel independently. More details can be found here: https://www.medrxiv.org/content/10.1101/2020.05.27.20113027v1

While the code is mainly based on Python librairies, first steps can also be computed using Shell command lines. We are then providing both Python and Unix scripts.
Here the TractLearn use implies a first step of major brain bundles segmentation using TractSeg. For more information about TractSeg please refer to:

## Step 1: Subjects coregistration

As TractLearn requires an excellent matching between subjects, the first steps imply non linear coregistration in a common template space. Here deformations are estimated between each subject Fiber Orientation Distribution (FOD) image  and the template.

## Step 2: Inversion of the transformation for tck files registration

All the transformations of the previous step are inverted.

## Step 3: Transformation application for all TractSeg bundles

## Step 4: Estimation of the different scalar coefficients in the template space

For each bundle of each patient, the TDI, TW-FOD, TW-FA and AFD coefficients are estimated.

## Step 5: Mask calculation for all the subjects

For each bundle, 80% of maximum of the TDI intensity is considered to perform a subject mask. 
The intersection of all the masks corresponds to the mask of analysis.

## Step 6: Estimate z-score maps (group versus individuals)

## Step 7: Estimate t-test maps (group vs group studies)
