import os
from os.path import join as opj
import pandas as pd
import numpy as np
from glob import glob
import debug_RV

if 'andrebeukers' in os.getcwd().split('/'):
    bids_dir = "/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset"
elif 'srm254' in os.getcwd().split('/'):
    bids_dir = "/home/fs01/srm254/visser_replicate/BIDSdataset"

# # general helper

def get_output_dir(bids_dir, tbt_or_cbc):
    # assemble path
    path2_outputfolder = opj(bids_dir, 
        "deriv_data", "stimes-%s" % tbt_or_cbc)
    # make folder
    if not os.path.isdir(path2_outputfolder): 
        os.mkdir(path2_outputfolder)
    return path2_outputfolder

def parse_events_fpath(events_fpath):
    L = events_fpath.split('/')[-1].split('_')
    D = dict()
    for i in L[:-1]:
        D[i.split('-')[0]] = i.split('-')[1]
    return D


def get_stimes_fpath(bids_dir, events_fpath, trial_name, tbt_or_cbc):
    
    # get info
    sub_num = parse_events_fpath(events_fpath)['sub']
    task = parse_events_fpath(events_fpath)['task']

    # assemble path
    output_dir = get_output_dir(bids_dir,tbt_or_cbc)
    fname = "sub-%s_task-%s_trial-%s_stimes-%s.csv"\
        % (sub_num, task, trial_name, tbt_or_cbc)
    
    fpath = opj(output_dir, fname)
    return fpath

# # dict of onsets

def get_onsets_dict(events_fpath):

    events_df = pd.read_csv(events_fpath, sep = ',')

    # indexing trials of a given condition
    bool_t = events_df['tc'] == 'target'
    bool_p = events_df['CS'] == 'CSplus'

    bool_tp = bool_t & bool_p
    bool_tm = bool_t &~ bool_p
    bool_cp = ~ bool_t & bool_p
    bool_cm = ~ bool_t &~ bool_p

    # appplying index
    trial_onsets = {}
    trial_onsets['targetCSplus1'] = events_df[bool_tp]['onsets'].iloc[:4]
    trial_onsets['targetCSplus2'] = events_df[bool_tp]['onsets'].iloc[4:]
    trial_onsets['targetCSminus1'] = events_df[bool_tm]['onsets'].iloc[:2]
    trial_onsets['targetCSminus2'] = events_df[bool_tm]['onsets'].iloc[2:]

    trial_onsets['CSplus1'] = events_df[bool_p]['onsets'].iloc[:8]
    trial_onsets['CSplus2'] = events_df[bool_p]['onsets'].iloc[8:]
    trial_onsets['CSminus1'] = events_df[~bool_p]['onsets'].iloc[:4]
    trial_onsets['CSminus2'] = events_df[~bool_p]['onsets'].iloc[4:]
    
    trial_onsets['targetCSplus'] = events_df[bool_tp]['onsets']
    trial_onsets['targetCSminus'] = events_df[bool_tm]['onsets']
    trial_onsets['conditCSplus'] = events_df[bool_cp]['onsets']
    trial_onsets['conditCSminus'] = events_df[bool_cm]['onsets']
    trial_onsets['US'] = events_df[bool_cp]['onsets'] + 2

    return trial_onsets


# # makes stimes given single path

def get_stimes_array(onsets_dict, trial_name, tbt_or_cbc):

    stimes = onsets_dict[trial_name]

    if tbt_or_cbc == 'tbt':    
        duration_col = np.ones(len(stimes)) * 4
        stimes_array = np.vstack([stimes.values,duration_col])
        stimes_array = pd.DataFrame(stimes_array)
    elif tbt_or_cbc == 'cbc':
        pass

    return stimes_array.iloc[0,:]


# # loop through events file folders
events_fpath_list = glob(opj(bids_dir, 
    "raw_data", "sub-???", "func", "*task-pain*_events.csv"))
events_fpath_list.extend(glob(opj(bids_dir, 
    "raw_data", "sub-???", "func", "*task-brush*_events.csv")))
for events_fpath in events_fpath_list:

    onsets_dict = get_onsets_dict(events_fpath)

    # # tbt
    for trial_name in onsets_dict.keys():

        # tbt
        stimes_array = get_stimes_array(onsets_dict, trial_name, 'tbt')
        stimes_fpath = get_stimes_fpath(bids_dir, events_fpath, trial_name, 'tbt')
        pd.DataFrame(stimes_array).transpose().to_csv(stimes_fpath, sep=' ', index=False, header=False)
