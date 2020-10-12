#python Register_fod2template.py working_direction file_name
#The working directory being the directory where all your individuals are stored + two folders named warped_template and transformed template respectively + the template named template_FOD.nii.gz
#The file name corresponds to the common pattern name of each individual FOD map, for example *_wmfod_norm_average.mif

from glob import glob
import numpy as np
from subprocess import call
import sys

rep =  sys.argv[-2]
name_fod = sys.argv[-1]
file_name = glob(rep + "/*/"+name_fod)
print(file_name)

for name in file_name:
	tmp = name.split("/")[-2]
	file_mask = "/".join(name.split("/")[:-1]) + "/mask_MNI.nii"
	cmd = "mrregister -force -transformed transformed_template/"+tmp+"_transformed.mif.gz -nl_warp_full warped_template/"+tmp+"_warp.mif.gz "+name+" template_FOD.nii.gz"
	print(cmd)
	call(cmd.split(" "))
