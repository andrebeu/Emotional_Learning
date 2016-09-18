import os
import sys; sys.path.append('WD_visser_replicate')

## SERVER ##
# os.chdir('/home/fs01/srm254/visser_replicate')
# path2_BIDSdataset = 'BIDSdataset'

## MAC ##
# os.chdir('/Users/andrebeukers/Documents/fMRI/RVstudy')
# path2_BIDSdataset = 'miniDS/BIDSdataset'
# ROI='hip'
# TASK='pain'

## IMPORTS ##

import numpy as np
from mvpa2.suite import *
from RV_plots import *


## PARAMETER OPTIONS ##

TASK = sys.argv[1]
ROI = sys.argv[2]
path2_BIDSdataset = sys.argv[3]


## SAMPLE ATTRIBUTES ## 

# NOTE assume order of stim_times_IM in GLM file unchanged
t = lambda x,y: np.tile(x,y)
trialtype_list = np.concatenate((t('cm',6), t('cp',12), t('tm',7), t('tp',14)))
tn = lambda x: np.arange(x)+1
trialnum_list = np.concatenate((tn(6), tn(12), tn(7), tn(14)))

trial_list = np.chararray(len(trialnum_list), itemsize = 15)
for i in range(len(trialnum_list)):
    if i < 6: 
        trial_list[i] = 'CS_minus %.2i' % trialnum_list[i]
    elif i < 6+12: 
        trial_list[i] = 'CS_plus %.2i' % trialnum_list[i]
    elif i < 6+12+7: 
        trial_list[i] = 'CS_minus %.2i' % trialnum_list[i]
    else: 
        trial_list[i] = 'CS_plus %.2i' % trialnum_list[i]


## RSA ANALYSIS ##

# prepare DSM 
dsm = measures.rsa.PDist(square = True)

# loop variables
list_DSs = []; list_DSMs = []
path2_GLMresults = os.path.join(path2_BIDSdataset,
    'deriv_data/GLM-results_ROI-%s_task-%s') % (ROI, TASK)

# loop through filenames of beta volumes (GLM results)
for fname_sub_bv in os.listdir(path2_GLMresults):

    # file path and subject number
    fpath = os.path.join(path2_GLMresults, fname_sub_bv)
    sub_num = fname_sub_bv.split('-')[1].split('_')[0]

    print "RSAing subj: " + sub_num

    # load beta volumes of single subject
    sub_bv = fmri_dataset(fpath)

    # sample attributes
    sub_bv.sa['trialtype'] = trialtype_list
    sub_bv.sa['trialnum'] = trialnum_list
    sub_bv.sa['trial'] = trial_list
    sub_bv.sa['sub_num'] = np.ones(sub_bv.nsamples)*int(sub_num)

    # get target trials only
    idx_tp = (sub_bv.sa.trialtype == 'tp')
    idx_tm = (sub_bv.sa.trialtype == 'tm')
    sub_bv = sub_bv[idx_tp | idx_tm]

    # subject dissimilarity matrix
    sub_dsm = dsm(sub_bv)

    # list of DSMs and DSs of each subject
    list_DSMs.append(sub_dsm)
    list_DSs.append(sub_bv)


## GROUP ANALYSIS
print "begining group analysis"

# group dataset
DSs = mvpa2.suite.vstack(list_DSs, a=0)
DSMs = mvpa2.suite.vstack(list_DSMs, a=0)

# subject 23has a problem
select_bool = (DSs.sa.sub_num != 13) & (DSs.sa.sub_num != 22) &\
            (DSs.sa.sub_num != 23) & (DSs.sa.sub_num != 33) &\
            (DSs.sa.sub_num != 32) & (DSs.sa.sub_num != 34) &\
            (DSs.sa.sub_num >= 300) & (DSs.sa.sub_num < 10) 


DSs = DSs[DSs.sa.sub_num != 23]
DSMs = DSMs[DSMs.sa.sub_num != 23]


# mean DSM
mgs = mean_group_sample(['trial'])
group_DSM = mgs(DSMs)



## FIGURES ##
print "saving figures"

# prepare RSA results directory
path2_RSAresults = os.path.join(path2_BIDSdataset,
    "deriv_data/RSA-results_task-%s_ROI-%s") % (TASK, ROI)
if not os.path.isdir(path2_RSAresults): 
    os.mkdir(path2_RSAresults)

# saving figures
def save_RSAfig(figname):
    global path2_RSAresults
    fpath_fig = os.path.join(path2_RSAresults, figname)
    plt.savefig(fpath_fig)
    plt.close('all')


# figures
import matplotlib
import matplotlib.pyplot as plt

figname = "RSA-groupDSM_task-%s_ROI-%s" % (TASK, ROI)
plot_DSM(group_DSM, title = 'Group DSM')
save_RSAfig(figname)
plt.close("all")

figname = "RSA-dmchangeCSplus_task-%s_ROI-%s" % (TASK, ROI)
dmchange = plot_CSplus_dmchange(group_DSM,ROI)
save_RSAfig(figname)
plt.close("all")


