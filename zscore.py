#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:38:12 2020
"""
import sys

import pickle as pk 
from glob import glob
import nibabel as nib
import numpy as np
from umap import UMAP
from sklearn.metrics import pairwise_distances
from sklearn.model_selection import LeaveOneOut
from sklearn.neighbors import NearestNeighbors
from NW_regression import KernelRegression


Track_name = ['AF_left', 'AF_right', 'ATR_left', 'ATR_right', 'CC_1', 'CC_2', 'CC_3', 'CC_4', 'CC_5', 'CC_6', 'CC_7', 'CG_left', 'CG_right', 'CST_left', 'CST_right', 'FPT_left', 'FPT_right', 'ICP_left', 'ICP_right', 'IFO_left', 'IFO_right', 'ILF_left', 'ILF_right', 'MCP', 'MLF_left', 'MLF_right', 'OR_left', 'OR_right', 'POPT_left', 'POPT_right', 'SCP_left', 'SCP_right', 'SLF_III_left', 'SLF_III_right', 'SLF_II_left', 'SLF_II_right', 'SLF_I_left', 'SLF_I_right', 'STR_left', 'STR_right', 'ST_FO_left', 'ST_FO_right', 'ST_OCC_left', 'ST_OCC_right', 'ST_PAR_left', 'ST_PAR_right', 'ST_POSTC_left', 'ST_POSTC_right', 'ST_PREC_left', 'ST_PREC_right', 'ST_PREF_left', 'ST_PREF_right', 'ST_PREM_left', 'ST_PREM_right', 'T_OCC_left', 'T_OCC_right', 'T_PAR_left', 'T_PAR_right', 'T_POSTC_left', 'T_POSTC_right', 'T_PREC_left', 'T_PREC_right', 'T_PREF_left', 'T_PREF_right', 'T_PREM_left', 'T_PREM_right', 'UF_left', 'UF_right']
print(Track_name)

ROI_pb = []
modality = sys.argv[-1]
Patient_pattern = sys.argv[-2]
Control_pattern = sys.argv[-3]


for track in Track_name:
    print(track)
    #Load control
    #Ima1 = [glob("transformed_template/"+name+"*_"+track+"_*"+modality+"*.nii.gz")[0] for name in Control]
    Ima1 = glob("transformed_template/*"+ Control_pattern +"*_"+track+"_*"+modality+"*.nii.gz")
    Ima1.sort()
    name_Ima1 = [i.split("/")[-1].split(track)[0] for i in Ima1 ]
    print(name_Ima1)
    ima_index = nib.load(glob("stat/" + track+"*Mean_TDI*.nii")[0]).get_data()
    ind_mean = np.where(ima_index)
    Data1 = []
    for i in Ima1:
        Data1.append(nib.load(i).get_data()[ind_mean])
    if len(Data1) == 0:
        print(track + " is empty for control group")
        continue
    Data1 = np.array(Data1)

    #Load patient
    #Ima_pat =  [glob("transformed_template/"+name+"*_"+track+"_*"+modality+"*.nii.gz")[0] for name in Patient]
    Ima_pat = glob("transformed_template/*"+ Patient_pattern +"*_"+track+"_*"+modality+"*.nii.gz")
    Ima_pat.sort()
    name_pat = [i.split("/")[-1].split(track)[0] for i in Ima_pat ]
    print(name_pat)

    Data_pat = []
    for i in Ima_pat:
        Data_pat.append(nib.load(i).get_data()[ind_mean])
    
    if len(Data_pat) == 0:
        print(track + " is empty for patient group")
        continue
    Data_Pat = np.array(Data_pat)

    print("Start the Leave One Out procedure")
    X = Data1.copy()
    loo = LeaveOneOut()
    loo.get_n_splits(X)
    print(loo)
    #List to save the residuals of the controls
    error_loo = []
    #List to save the residuals of the patients
    error_mtbi =[]
    for train_index, test_index in loo.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
        try:
            #Learn the manifold
            mani = UMAP(n_components=3,n_neighbors=10,min_dist=0.5)
            mani.fit(X_train)
            #Estimate the projection on the reduced space
            Reg2mani = KernelRegression(kernel="rbf", gamma=np.logspace(-4, 3, 1000))
            Reg2mani.fit(X_train,mani.embedding_)
            X1 = Reg2mani.predict(X_train)
            X2 = Reg2mani.predict(X_test)
            #Check if there are some Nan values in the reconstruction
            if np.isnan(X2).any():
                nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(X_train)
                distances, ind_nearest_X2 = nbrs.kneighbors(X_test)
                X2 = X1[ind_nearest_X2]
            X_pat = Reg2mani.predict(Data_pat)
            if np.isnan(X_pat).any():
                ind_nan_pat = np.where(np.isnan(X_pat).any(axis=1))
                nbrs_pat = NearestNeighbors(n_neighbors=1, algorithm='ball_tree')
                nbrs_pat.fit(X_train)
                distance_nan_pat,ind_nearest_X1 = nbrs.kneighbors(Data_pat[ind_nan_pat])
                X_pat[ind_nan_pat[0]] = X1[ind_nearest_X1].reshape(X_pat[ind_nan_pat[0]].shape)
            #estimate the projection of reduced space on natural space 
            Reg2real = KernelRegression(kernel="rbf", gamma=np.logspace(-4, 3, 1000))
            Reg2real.fit(X1,X_train)
            Y2 = Reg2real.predict(X2)
            Y_pat = Reg2real.predict(X_pat)
            error_loo.append(X_test - Y2)
            error_pat.append(Data_Pat - Y_pat)
        except:
            print("ERROR TRAIN:", train_index, "TEST:", test_index)
    if Data1.shape[0] != np.array(error_loo).shape[0]:
    	ROI_pb.append(track)
    else:
    	Error_loo = np.array(error_loo).reshape(-1,Data1.shape[1])
    	Error_pat = np.array(error_pat)

    #Estimation of the zscore 

    	Zscore_pat = np.zeros(Data_Pat.shape)
    	Mean1 = np.mean(Error_loo,axis=0)
    	Std1 = np.std(Error_loo,axis=0)
    	Mean_error_pat = np.mean(Error_pat,axis=0)
    	for i in range(Data_Pat.shape[0]):
        	for j in range(Data_Pat.shape[1]):
            		Zscore_pat[i,j] = (Mean_error_pat[i,j] - Mean1[j])/Std1[j]        
    	IMA = nib.load(Ima_pat[0])
    	aff= IMA.get_affine()   
    	for i in range(Data_Pat.shape[0]):
    	    IMA_ = np.zeros(IMA.get_data().shape)
    	    IMA_[ind_mean] = Zscore_pat[i,:]
    	    IMA_nib = nib.Nifti1Image(IMA_,aff)
    	    nib.save(IMA_nib,"stat/zscore_"+track+"_"+name_pat[i]+"_"+modality+"_80.nii.gz")
