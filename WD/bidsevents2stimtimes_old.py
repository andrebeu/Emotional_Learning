import os
from os.path import join as opj
import pandas as pd
import numpy as np
from glob import glob
import debug_RV


""" This file outputs stim_time files for stim_times_IM or stim_times
    specify tbt or cbc 
    
    Maybe: don't require tbt cbc options, always do both, improve naming
    """

path2_eventfile = "/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset/raw_data/sub-024/func/sub-024_task-pain_file-1609_events.csv"
path2_output_folder = "/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset/deriv_data/stimes-tbt"
# path2_eventfile = "/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset/raw_data/sub-026/func/sub-026_task-funcloc_file-1525_events.csv"




def get_path2_outputfolder(tbt_or_cbc):

    if 'andrebeukers' in os.getcwd().split('/'):
        main_dir = '/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate'
        bids_dir = opj(main_dir, "BIDSdataset")
    elif 'srm254' in os.getcwd().split('/'):
        main_dir = "/home/fs01/srm254/visser_replicate"
        bids_dir = opj(main_dir, "BIDSdataset")

    path2_outputfolder = opj(bids_dir, "deriv_data", "stimes-%s" % tbt_or_cbc)
    if not os.path.isdir(path2_outputfolder): os.mkdir(path2_outputfolder)

    return path2_outputfolder



""" get_trial functions, returns dicts indexed by trial_name """

def get_trial_onsets_PB(path2_eventfile):

    events_df = pd.read_csv(path2_eventfile, sep = ',')

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

def get_onsets_FL(path2_eventfile):

    events_df = pd.read_csv(path2_eventfile, sep = ',')
    blocks = events_df.iloc[range(0,60,5)]

    # boolean for trials of given condition
    bool_face_blocks = blocks['face_or_house'] == "face"
    bool_house_blocks = ~bool_face_blocks

    # dict indexed by block name
    block_onsets = {}
    block_onsets['face'] = blocks[bool_face_blocks]['onsets']
    block_onsets['house'] = blocks[bool_house_blocks]['onsets']

    ## OLD: event related
    # indexing trials of given condition
    # bool_face_trials = events_df['face_or_house'] == "face"
    # bool_house_trials = ~bool_face_trials

    # dict indexed by trial_name
    # trial_onsets = {}
    # trial_onsets['face'] = events_df[bool_face_trials]['onsets']
    # trial_onsets['house'] = events_df[bool_house_trials]['onsets']

    return block_onsets


""" formats onsets as expected by tbt or cbc and calls saveing function """


def make_stimes_tbt(path2_eventfile):

    # dict onset times indexed by trial name
    taskid = path2_eventfile.split('/')[-1].split('_')[1]
    if (taskid == "task-brush") | (taskid == "task-pain"):
        onsets_dict = get_trial_onsets_PB(path2_eventfile)
    else:
        error_message = "unsupported task for trial-by-trial"
        assert False

    # loop through trials, make stimes
    for trial_name in ['targetCSplus','targetCSminus','conditCSplus','conditCSminus']:
        stimes = onsets_dict[trial_name]
        duration = np.ones(len(stimes)) * 4
        stimes_IM = np.vstack([stimes.values,duration]).transpose()
        save_tbt(stimes_IM)

    

def save_tbt(stimes_IM, trial_name):

    fname = "%s_%s_trial-%s_stimes-%s.csv" % (subid, taskid, trial_name, tbt_or_cbc)
    fpath = opj(path2_output_folder, fname)


# loop through contents of dict
for trial_name, trial_onsets in onsets_dict.iteritems():

    # format for stim_times_IM
    stimes_IM = trial_onsets.astype(str) + " 4"
    # call save function
    # save_stimes(stimes_IM, trial_name, path2_eventfile, path2_output_folder)





        
def make_stimes_file_cbc(path2_eventfile, path2_output_folder):

    # get task id to decide what trial_onsets function to call
    taskid = path2_eventfile.split('/')[-1].split('_')[1]
    if (taskid == "task-brush") | (taskid == "task-pain"):
        onsets_dict = get_trial_onsets_PB(path2_eventfile)
    elif taskid == "task-funcloc":
        onsets_dict = get_onsets_FL(path2_eventfile)
        assert len(onsets_dict['face']) == len(onsets_dict['house']) == 6

    # loop through trial types
    for trial_name, trial_onsets in onsets_dict.iteritems():
        # format for stim_times
        stimes = pd.DataFrame(trial_onsets).T
        # call save function
        save_stimes(stimes, trial_name, path2_eventfile, path2_output_folder)



""" saving function """

def save_stimes(stimes, trial_name, path2_eventfile, path2_output_folder):

    subid = path2_eventfile.split('/')[-1].split('_')[0]
    taskid = path2_eventfile.split('/')[-1].split('_')[1]
    
    # determine cbc or tbt based on shape of stimes
    if stimes.ndim == 1: tbt_or_cbc = "tbt"
    elif stimes.ndim == 2: tbt_or_cbc = "cbc"

    # file names and paths
    fname = "%s_%s_trial-%s_stimes-%s.csv" % (subid, taskid, trial_name, tbt_or_cbc)
    fpath = opj(path2_output_folder, fname)
    stimes.to_csv(fpath, index=False, header=False, sep=' ')



""" wrappers specific for tbt or cbc
    loop through subjects """

def bidsevents2stimtimes_tbt(path2_BIDSdataset, task_name):

    # make folder if does not exist
    path2_stimes_folder = opj(path2_BIDSdataset, 'deriv_data', "stimes-tbt")
    if not os.path.isdir(path2_stimes_folder): os.mkdir(path2_stimes_folder)

    # loop through subject folders
    for sub_folder in glob(opj(path2_BIDSdataset, "raw_data", "sub-???")):
        
        # get path2_eventfile
        subid = sub_folder.split('/')[-1]
        temp = glob(opj(sub_folder,'func', 
            "%s_task-%s*_events.csv" % (subid, task_name)))
        
        # check if only one events file, if not error log
        if len(temp) == 1:
            # call make_stimes_file_tbt
            path2_eventfile = temp[0]
            make_stimes_file_tbt(path2_eventfile, path2_stimes_folder)
        else:
            error_message = "check events file: %s task-%s" % (subid, task_name)
            # print error_message
            # RV_debug.debugger_errors(path2_BIDSdataset, error_message)


def bidsevents2stimtimes_cbc(path2_BIDSdataset, task_name):

    # make folder if does not exist
    path2_stimes_folder = opj(path2_BIDSdataset, 'deriv_data', "stimes-cbc")
    if not os.path.isdir(path2_stimes_folder): os.mkdir(path2_stimes_folder)

    # loop through subject folders
    for sub_folder in glob(opj(path2_BIDSdataset, "raw_data", "sub-???")):

        # path2_events file
        subid = sub_folder.split('/')[-1]
        temp = glob(opj(sub_folder,'func', 
            "%s_task-%s*_events.csv" % (subid, task_name)))

        # check if only one events file, if not error log
        if len(temp) == 1:
            # call make_stimes_file_cbc
            path2_eventfile = temp[0]
            make_stimes_file_cbc(path2_eventfile, path2_stimes_folder)
        else:
            error_message = "check events file: %s task-%s" % (subid, task_name)
            # print error_message
            # RV_debug.debugger_errors(path2_BIDSdataset, error_message)


        
""" final wrapper """

def bidsevents2stimtimes(path2_BIDSdataset, task_name, tbt_or_cbc):

    if tbt_or_cbc == "cbc":
        bidsevents2stimtimes_cbc(path2_BIDSdataset, task_name)
    elif tbt_or_cbc == "tbt":
        bidsevents2stimtimes_tbt(path2_BIDSdataset, task_name)



