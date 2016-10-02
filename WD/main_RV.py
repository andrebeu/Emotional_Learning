import os
import sys;
from os.path import join as opj


if 'andrebeukers' in os.getcwd().split('/'):
    print 'main onmac'
    ## ON MAC ##
    path2_maindir = '/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate'
    path2_batch = opj(path2_maindir, "BATCH_4")
elif 'srm254' in os.getcwd().split('/'):
    print 'main onserv'
    ## SERVER ##
    path2_maindir = "/home/fs01/srm254/visser_replicate"
    path2_batch = opj(path2_maindir, 'BATCH_full_aug9')


## PATHS ##
os.chdir(path2_maindir)
path2_rawonsets = opj(path2_maindir, "rawonsets")
path2_BIDSdataset = opj(path2_maindir, "BIDSdataset")
path2_WD = opj(path2_maindir, 'WD_visser_replicate')
sys.path.append(path2_WD)


## IMPORTS ##
from batch2bids import batch2bids 
from bidsevents2stimtimes import bidsevents2stimtimes
from subprocess import call as subprocesscall


# # PARAMETER OPTIONS # # 

## TASK 'pain', 'brush'
TASK = 'pain'
## ROI 'global', 'left_amygdala', 'right_amygdala'
ROI = 'left_amygdala' 


# # DOING STUFF # #

## BIDSdataset
# import b2b_new

##  ANATOMICAL MASKS
# subprocesscall("masks_anat.sh", shell=True)

# # REMOVE PROBLEM SUBJECTS
import prob_subs
prob_subs_list = [4, 6, 19, 20, 335]
prob_subs_list.extend(prob_subs.bytask(task = 'pain'))
# prob_subs_list.extend(prob_subs.bybehave(th = 8))
# prob_subs_list.extend(prob_subs.bymotion(th = 2))
for subno in prob_subs_list:
    cmd_remove = "bash remove_subject.sh %s" % (subno)
    subprocesscall(cmd_remove, shell=True)

# ## GLM_PB
cmd_GLM_PBcbc = "bash GLM_PB.sh %s %s 'tbt'" % (TASK, ROI)
subprocesscall(cmd_GLM_PBcbc, shell=True)

## GLM_FL (no group GLM)
# cmd_GLM_FLcbc = "GLM_FL.sh %s" % (path2_maindir)
# subprocesscall(cmd_GLM_FLcbc, shell=True)

## run RSA
# run_RSA = "ipython -- WD_visser_replicate/visserRSA.py %s %s %s"\
#         % (TASK, ROI, path2_BIDSdataset)
# subprocesscall(run_RSA, shell=True)



## OLD
# batch2bids(path2_batch, path2_rawonsets)