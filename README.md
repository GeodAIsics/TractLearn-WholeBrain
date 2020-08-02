# TrackLearn

TrackLearn is a software to permit brain fascicules analysis. 

## Step 1: Registration of the subjects

All non linear deformations are estimated between each subject's FOD image  and the template FOD image.

## Step 2: Inversion of the transformation

All the transformations are the previous step are inverted.
We performed this manipulation to obtain accurate registration of suject FOD images in the template space.

## Step 3: Apply the transformation for all the bundles of TrackSeg for each patient

## Step 4: Estimate the different scalar coefficients of the bundles in the template space

For each bundle of each patient, the TDI, TW-FOD, TW-FA and AFD coefficients are estimated.

## Step 5: Estimate the mask of analysis for all the subjects

For each bundle, 80% of maximum of the TDI intensity is considered to perform a subject mask. 
The intersection of all the masks corresponds to the mask of analysis.

## Step 6: Estimate the z-score for all patients.
