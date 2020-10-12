#python 3_Invert_warp.py
#Need to have already two folders: /transformed_template including the coregistered WM files and /warped_template including the warps files

from glob import glob
from subprocess import call
import sys

tmp = sys.argv[-1]
file_name = glob("warped_template/*")
file_name.sort()

print(file_name)

for name in file_name:
	name_tmp = name.split("_warp.")[0]
	cmd = "warpconvert "+name+" warpfull2deformation -template template_FOD.nii.gz "+name_tmp+"_warpfull2deformation.mif.gz"
	print(cmd)
	call(cmd.split(" "))
	cmd2 = "warpinvert "+name_tmp+"_warpfull2deformation.mif.gz "+name_tmp+"_warpfull2deformation_invert.mif.gz"
	print(cmd2)
	call(cmd2.split(" "))
