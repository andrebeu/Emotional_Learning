import os
from os.path import join as opj
from glob import glob
import mvpa2.suite as mvpa
import numpy as np
import pandas as pd
import plots_RV; reload(plots_RV)


if 'andrebeukers' in os.getcwd().split('/'):
    bids_dir = '/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset'
elif 'srm254' in os.getcwd().split('/'):
    bids_dir = "/home/fs01/srm254/visser_replicate/BIDSdataset"
    
task = "pain"
roi = "left_amygdala"

# GLMresults_dir = opj(bids_dir, "deriv_data", GLMresults_folder)
# RSAresults_dir = opj(bids_dir, "deriv_data", RSAresults_folder)
# behave_file = pd.read_csv(opj(bids_dir,"behavioural.csv"))
GLMresults_folder = "GLMtbt-results_TASK-%s_ROI-%s" % (task, roi)
RSAresults_folder = "RSA-results_TASK-%s_ROI-%s" % (task, roi)

main_dir = "/Users/andrebeukers/Documents/fMRI/RVstudy/fromServ/RSA2"
GLMresults_dir = opj(main_dir, GLMresults_folder)
RSAresults_dir = opj(main_dir, RSAresults_folder)
behave_file = pd.read_csv(opj(main_dir,"behavioural.csv"))

if not os.path.isdir(RSAresults_dir):
    os.mkdir(RSAresults_dir)


## SAMPLE ATTRIBUTES ## 

# NOTE assume order of stim_times_IM in GLM file unchanged
t = lambda x,y: np.tile(x,y)
tn = lambda x: np.arange(x)+1
trialnum_list = np.concatenate((tn(7), tn(7), tn(7), 
    tn(12), tn(6), tn(12)))
trialtype_list = np.concatenate((t('tp',14), 
    t('tm',7), t('cp',12), t('cm',6), t('us',12)))
roi_list = t(roi,51)
task_list = t(task,51)


# unique for each beta
trial_list = np.chararray(len(trialnum_list), itemsize = 15)
stim_list = np.chararray(len(trialnum_list), itemsize = 15)
for i in range(len(trialnum_list)):
    if (i < 14) & (i%2 == 0): 
        trial_list[i] = 'CS+1 %.2i' % trialnum_list[i]
        stim_list[i] = 'CS+'
    elif (i < 14) & (i%2 == 1): 
        trial_list[i] = 'CS+1 %.2i' % trialnum_list[i]
        stim_list[i] = 'CS+'
    elif i < 14+7: 
        trial_list[i] = 'CS- %.2i' % trialnum_list[i]
        stim_list[i] = 'CS-'
    else:
        break


## RSA ANALYSIS ##

# prepare DSM 
dsm_measure = mvpa.measures.rsa.PDist(square=True)

# loop variables
ds_list = []; dsm_list = []

# loop beta volumes (GLM results), load fmri_dataset
GLMresults_list = glob(opj(GLMresults_dir,"*nifti*"))
for fpath in GLMresults_list:

    # file fpath and subject number
    sub_num = fpath.split('/')[-1].split('_')[0].split('-')[-1]
    print "RSAing subj: " + sub_num

    # behave score (needs improvement)
    try:
        behave_score = float( behave_file['diff']
            [behave_file['sub'].str.split('-').str[1] == sub_num])
        condit = sum([behave_score < -8])
    except: 
        behave_score = 0
        condit = 0

    # load beta volumes of single subject
    sub_ds = mvpa.fmri_dataset(fpath)
    assert sub_ds.shape == (51, 141120)
    
    # sample attributes
    sub_ds.sa['sub_num'] = \
        (np.ones(sub_ds.nsamples)*int(sub_num)).astype(int)
    sub_ds.sa['trialtype'] = trialtype_list
    sub_ds.sa['trialnum'] = trialnum_list
    sub_ds.sa['roi'] = roi_list
    sub_ds.sa['task'] = task_list
    sub_ds.sa['stim'] = stim_list
    sub_ds.sa['trial'] = trial_list
    sub_ds.sa['behave'] = np.tile(behave_score,51)
    sub_ds.sa['condit'] = np.tile(condit,51)

    # get target trials only
    idx_tp = (sub_ds.sa.trialtype == 'tp')
    idx_tm = (sub_ds.sa.trialtype == 'tm')
    sub_ds = sub_ds[idx_tp | idx_tm]
    assert sub_ds.shape == (21, 141120)

    # grouping CS+1 CS+2 CS-
    t = [0,8,2,10,4,12,6]
    t.extend([7,1,9,3,11,5,13])
    t.extend(range(14,21))
    temp = []
    for i in t:
        temp.extend(sub_ds[i,:])
    sub_ds = mvpa.vstack(temp,a=0)

    # subject similarity matrix
    sub_dsm = dsm_measure(sub_ds)
    sub_dsm.samples = sub_dsm.samples * (-1) + 1

    # save
    ds_fpath = opj(RSAresults_dir,"sub-%s_RSA-dataset" % sub_num)
    dsm_fpath = opj(RSAresults_dir,"sub-%s_RSA-dsm" % sub_num)
    # sub_ds.save(ds_fpath, compression = 9)
    # sub_dsm.save(dsm_fpath, compression = 9)

    # figures
    # plots_RV.dsm_fig(sub_dsm)
    # plots_RV.dmchange_fig(sub_dsm)

    # list of DSMs and DSs of each subject
    if np.unique(sub_ds.sa.sub_num) not in [4, 6, 19, 20, 335]:
        dsm_list.append(sub_dsm)
        ds_list.append(sub_ds)



# prob_subs = [4, 6, 19, 20, 335]
# dsm_list = [s for s in dsm_list if not np.unique(s.sa.sub_num) in prob_subs]

full_stack = mvpa.vstack(dsm_list, a=0) 
mgs = mvpa.mean_group_sample(["trial"],order='occurrence')

## group analysis

condit_idx = full_stack.sa.behave < -8
noncondit_idx = full_stack.sa.behave > -8

condit_stack = full_stack[condit_idx]
noncondit_stack = full_stack[noncondit_idx]

condit_dsm = mgs(condit_stack)
noncondit_dsm = mgs(noncondit_stack)
full_dsm = mgs(full_stack)

reload(plots_RV)
plots_RV.dmchange_fig(condit_dsm,group=True)
plots_RV.dmchange_fig(noncondit_dsm,group=True)
plots_RV.dmchange_fig2(condit_dsm,noncondit_dsm,group=True)
plots_RV.dmchange_diff_fig(condit_dsm,noncondit_dsm,group=True)




# dsm_stack = full_stack[bool_array]


# group_dsm = mgs(dsm_stack)

# group_dsm.a['N'] = len(np.unique(dsm_stack.sa.sub_num))

# plots_RV.dsm_fig(group_dsm, group=True)
# plots_RV.dmchange_fig(group_dsm, group=True)

