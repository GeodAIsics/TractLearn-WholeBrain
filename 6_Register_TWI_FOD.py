#python Register_TWI_FOD.py argument 0 (postprocess patient 1 to 10) or 1 (11 to 20)

from glob import glob
from subprocess import call
import sys

file_name = glob("transformed_template/*.mif.gz")
#print(file_name)
file_name.sort()
print(file_name)
print(sys.argv)

s = int(sys.argv[-1])

for name in file_name[s*10:(s+1)*10]:
#for name in file_name:
	tmp = name.split("/")[-1].split("_transformed.")[0]
	tmp_track = glob("transformed_template/"+tmp+"*.tck")
	print(tmp)
	print(tmp_track)
	for track in tmp_track:
		track_tmp = track.split(".")[0]
		cmd = "tckmap "+track+" -stat_tck gaussian -fwhm_tck 8 -template template_FOD.nii.gz -contrast fod_amp -force -image "+name+" -stat_vox mean "+track_tmp+"_TWI_Gaussian.nii.gz"
		print(cmd)
		call(cmd.split(" "))
		cmd = "tckmap "+track+" "+track_tmp+"_TDI_NoGaussian.nii.gz -template template_FOD.nii.gz -force"
		call(cmd.split(" "))
		cmd = "tckmap "+track+" -stat_tck gaussian -fwhm_tck 8 -template template_FOD.nii.gz -contrast scalar_map -image transformed_template/"+tmp+"_FA_template.nii.gz -force -stat_vox mean "+track_tmp+"_TWI2_FA_Gaussian.nii.gz"
		print(cmd)
		call(cmd.split(" "))
		cmd = "mrcalc -force "+track_tmp+"_TWI_Gaussian.nii.gz 0 -gt transformed_template/"+tmp+"_FA_template.nii.gz -mult "+track_tmp+"_TWI_FA_Gaussian.nii.gz"
		print(cmd)
		call(cmd.split(" "))
		cmd = "afdconnectivity -afd_map "+tmp+"_"+track_tmp+"_AFD_Gaussian.nii.gz "+name+" "+track
		print(cmd)
		call(cmd.split(" "))
