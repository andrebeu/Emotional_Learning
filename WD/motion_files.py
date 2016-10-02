import os
from os.path import join as opj
from os.path import split as ops
import pandas as pd
import numpy as np
from glob import glob

import debug_RV


if 'andrebeukers' in os.getcwd().split('/'):
    print 'motion onmac'
    ## ON MAC ##
    path2_maindir = '/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate'
    path2_batch = opj(path2_maindir, "BATCH_4")
    path2_BIDSdataset = opj(path2_maindir,"BIDSdataset")
elif 'srm254' in os.getcwd().split('/'):
    print 'motion onserv'
    ## SERVER ##
    path2_maindir = "/home/fs01/srm254/visser_replicate"
    path2_batch = opj(path2_maindir, 'BATCH_full_aug9')
    path2_BIDSdataset = opj(path2_maindir,"BIDSdataset")


path2_motion_files = glob(opj(path2_maindir,"BIDSdataset/raw_data/sub-???/func/sub-???*motion.1D"))


## MAKE INDIVIDUAL MOTION FILES FOR AFNI
for motion_file in path2_motion_files:

    DF = pd.DataFrame.from_csv(motion_file, header = None, sep = ' ')

    path2_motion_new = opj(ops(motion_file)[0],'motion')
    task = motion_file.split('/')[-1].split('_')[1]
    sid = motion_file.split('/')[-1].split('_')[0]
 
    # DOCUMENTING EXCEEDING THRESHOLDS
    motion_thresh = [0.5,1,1.5,2,2.5]
    for m in motion_thresh:
        # number count number of TRs that exceed motion param
        count = np.sum(np.sum( abs(DF) > m ))
        error_message = "%s: %i TRs exceeds %.1fmm" % (task,count,m)
        if count: 
            print sid, error_message
            debug_RV.debugger_errors(path2_BIDSdataset, sid, error_message)

    
    # NEW MOTION FILE 4AFNI
    # results directory
    if not os.path.isdir(path2_motion_new):
        os.mkdir(path2_motion_new)
    
    # one file per motion param
    col = -1
    for motion_param in ['roll','pitch','yaw','dS','dL','dP']:
        col += 1
    
        # new motion file
        fname = motion_file.split('/')[-1].split('.')[0] + "-%s.1D" % motion_param
        fpath = opj(path2_motion_new,fname)
        DF.iloc[:,col].to_csv(fpath, header = False, index = False)
        
        
    

