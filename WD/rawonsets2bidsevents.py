import os
from os.path import join as opj
from os.path import split as ops
from glob import glob 
import pandas as pd

import debug_RV

""" The final function of this file is rawonsets2bidsevents(fpath).
    it takes as input the file path to the csv file as outputed the scanner
    and saves a csv file in the format specified by BIDS 
    
    It also returns a list of the paths to the names of the files
    it had trouble with """


# path2_rawonsets_file = opj("/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/rawonsets","15_FL_2016_May_06_1327.csv")
# path2_rawonsets_file = opj("/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/rawonsets","14_pain_final2_2016_May_24_1527.csv")

## FNAME INFO

def get_sid(path2_rawonsets_file): 
    fname = path2_rawonsets_file.split('/')[-1]
    return 'sub-%.3i' % float(fname.split('_')[0])

def get_task(path2_rawonsets_file): 
    fname = path2_rawonsets_file.split('/')[-1]
    return fname.split('_')[1] 

def get_fileno(path2_rawonsets_file): 
    fname = path2_rawonsets_file.split('/')[-1]
    return fname.split('_')[-1].split('.')[0]


## LOAD

def get_rawonsets_df_FL(path2_rawonsets_file):
    full_df = pd.read_csv(path2_rawonsets_file)
    validrows_df = full_df.iloc[full_df.iloc[:,1].dropna().index,:]
    assert len(validrows_df) == 60
    return validrows_df

def get_rawonsets_df_PB(path2_rawonsets_file):
    full_df = pd.read_csv(path2_rawonsets_file)
    validrows_df = full_df.iloc[full_df.iloc[:,0].dropna().index,:]
    assert len(validrows_df) == 39
    return validrows_df


## CORRECTION

def get_correction_FL(path2_rawonsets_file):

    full_df = pd.read_csv(path2_rawonsets_file)
    correction = full_df['key_resp_3.rt'].dropna().iloc[0]
    
    return correction

def get_correction_PB(path2_rawonsets_file):

    full_df = pd.read_csv(path2_rawonsets_file)
    correction = full_df['key_resp_3.rt'].dropna().iloc[0]
    
    return correction

## ONSETS

def get_onsets_FL(path2_rawonsets_file):
    validrows_df = get_rawonsets_df_FL(path2_rawonsets_file)
    onsets = validrows_df['image_3Start']

    correction = onsets.iloc[0] 
    # correction = get_correction_FL(path2_rawonsets_file)

    corrected_onsets = onsets - correction 
    assert len(corrected_onsets) == 60
    return corrected_onsets

def get_onsets_PB(path2_rawonsets_file):
    validrows_df = get_rawonsets_df_PB(path2_rawonsets_file)
    onsets = validrows_df['imageStart']

    correction = onsets.iloc[0] 
    # correction = get_correction_PB(path2_rawonsets_file)

    corrected_onsets = onsets - correction 
    assert len(corrected_onsets) == 39
    return corrected_onsets



## TRIAL TYPE

def get_stimname_PB(rawonsets_df):
    stim_path = rawonsets_df['face']
    stim_fname = stim_path.str.split('\\').str[-1]
    stim_name = stim_fname.str.split('.').str[0]

    assert (stim_name.str.len()<=3).all()
    return stim_name


## returns dict with stim names of CSplus and CSminus


def get_CS_stimname(rawonsets_df):
    stim_col = get_stimname_PB(rawonsets_df)
    CSplus_stimname = stim_col[rawonsets_df.iloc[:,2] > 0].unique()
    CSminus_stimname = stim_col[rawonsets_df.iloc[:,2] == 0].unique()
    CS_stimnames = {'CSplus':CSplus_stimname, 'CSminus':CSminus_stimname}

    assert len(CS_stimnames['CSplus']) == 2
    assert len(CS_stimnames['CSminus']) == 1
    return CS_stimnames


## determine condition of each trial

# PB
def get_CS(rawonsets_df):
    stimnames = get_stimname_PB(rawonsets_df)
    CS_stimnames = get_CS_stimname(rawonsets_df)

    CS = pd.Series(index = rawonsets_df.index)
    CSplus1_idx = stimnames == CS_stimnames['CSplus'][0]
    CSplus2_idx = stimnames == CS_stimnames['CSplus'][1]
    CSminus_idx = stimnames == CS_stimnames['CSminus'][0]

    CS[CSplus1_idx | CSplus2_idx] = 'CSplus'
    CS[CSminus_idx] = 'CSminus'

    assert not CS.isnull().any()
    assert CS.value_counts()['CSplus'] == 26
    return CS

# PB
def get_tc(rawonsets_df):
    tc = pd.Series(index = rawonsets_df.index)
    tc[rawonsets_df.iloc[:,2]>=0] = 'condit'
    tc[rawonsets_df.iloc[:,2].isnull()] = 'target'

    assert tc.value_counts()['target'] == 21
    assert tc.value_counts()['condit'] == 18
    return tc

# funcloc
def get_FH(rawonsets_df):
    FH = rawonsets_df['file'].str.split('_').apply(lambda x:x[0][:-1])
    assert FH.value_counts()['house'] == FH.value_counts()['face'] == 30
    return FH

""" task specific helpers for final wrapper"""

## reassemble and save 

def rawonsets2bidsevents_PB(path2_rawonsets_file, path2_BIDSdataset):
    
    try:
        # extract info
        rawonsets_df = get_rawonsets_df_PB(path2_rawonsets_file)
        onsets = get_onsets_PB(path2_rawonsets_file)
        stim_name = get_stimname_PB(rawonsets_df)
        CS = get_CS(rawonsets_df)
        tc = get_tc(rawonsets_df)

        # assemble df with info
        rawonsets = {'stim_name': stim_name, 'onsets':onsets, 'CS':CS, 'tc':tc }
        bidsevents = pd.DataFrame(rawonsets, columns = ['stim_name','onsets','CS','tc'])

        # call pd.to_csv function
        save_bidsevents(bidsevents, path2_rawonsets_file, path2_BIDSdataset)

    except:
        sid = get_sid(path2_rawonsets_file)
        task = get_task(path2_rawonsets_file)
        error_message = "%s_assembling_events" % task
        print "%s %s" % (sid, error_message)
        debug_RV.debugger_errors(path2_BIDSdataset, sid, error_message)


def rawonsets2bidsevents_FL(path2_rawonsets_file, path2_BIDSdataset):
    try:
        # extract info
        rawonsets_df = get_rawonsets_df_FL(path2_rawonsets_file)
        onsets = get_onsets_FL(path2_rawonsets_file)
        FH = get_FH(rawonsets_df)

        #assemble df with info
        rawonsets = {'face_or_house' : FH, "onsets" : onsets}
        bidsevents = pd.DataFrame(rawonsets, columns = ['face_or_house','onsets'])
    
        # call pd.to_csv function
        save_bidsevents(bidsevents, path2_rawonsets_file, path2_BIDSdataset)

    except:
        sid = get_sid(path2_rawonsets_file)
        task = get_task(path2_rawonsets_file)
        error_message = "%s_assembling_events" % task
        print "%s %s" % (sid, error_message)
        debug_RV.debugger_errors(path2_BIDSdataset, sid, error_message)



""" final wrapper """

def rawonsets2bidsevents(path2_rawonsets_file, path2_BIDSdataset):
    task = get_task(path2_rawonsets_file)

    if (task == "pain") | (task == "brush"):
        rawonsets2bidsevents_PB(path2_rawonsets_file, path2_BIDSdataset)
    elif task == "FL":
        rawonsets2bidsevents_FL(path2_rawonsets_file, path2_BIDSdataset)

    else:
        sid = get_sid(path2_rawonsets_file)
        error_message = "ro2be unknown trial type" 
        print "%s %s %s" % (sid, error_message, task)
        debug_RV.debugger_errors(path2_BIDSdataset, sid, error_message)


# takes the dataframe assembled by rawonsets2bidsevents and saves it
# as a csv file in BIDSdataset/sub-??/func/
def save_bidsevents(bidsevents, path2_rawonsets_file, path2_BIDSdataset):

    sid = get_sid(path2_rawonsets_file)
    task = get_task(path2_rawonsets_file)
    fid = '_file-' + get_fileno(path2_rawonsets_file)
    if task == "FL": taskid = '_task-funcloc'
    else: taskid = '_task-' + task
    fname = sid + taskid + fid + '_events.csv'
    fpath = opj(path2_BIDSdataset,'raw_data',sid,'func',fname)
    
    bidsevents.to_csv(fpath)

