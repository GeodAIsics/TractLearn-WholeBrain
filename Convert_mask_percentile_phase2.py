from glob import glob
import numpy as np
from subprocess import call
import sys


file_name = glob("stat/*TDI_NoGaussian_Thr80.mif")
file_name.sort()
print(file_name)

ROI_name = []
for name in file_name:
	tmp = name.split("/")[-1].split("_TDI_NoGauss")[0]
	ROI_name.append('_'.join(tmp.split('_')[2:]))

ROI_name = np.unique(ROI_name).tolist()

#These exceptions are needed if the prefix name has "_"
try:
    ROI_name.remove("")
except:
    print("")
try:    
    ROI_name.remove("left")
except:
    print("")
try:
    ROI_name.remove("right")
except:
    print("")
try:
    for i in range(1,8):
        ROI_name.remove(str(i))
except:
    print("")
    
print(ROI_name)

for ROI in ROI_name:
	file_ROIs = glob("stat/*_"+ROI+"*NoGaussian_Thr80.mif")
	print(file_ROIs)
	cmd = ["mrmath"]+file_ROIs + ["product",  "stat/" + ROI+"_Mean_TDI_NoGaussian.nii", "-force"]
	print(cmd)
	call(cmd)
