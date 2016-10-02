import os
import pandas as pd
import numpy as np


""" This file loads a bids_events.csv file onto the sample attributes
    of a mvpa2.Dataset """
# NB currently csv is in use.

def read_tsv(path2event_file):
    """ reads BIDS_events.tsv into dataframe"""
    return pd.read_csv(path2event_file, sep = ',')


def get_sa_per_sample(ds, attr_name, path2event_file, padding=0):
    """ for a given attribute name, returns a list of sample attributes 
    whose length matches that of the dataset. each entry of the list
    corresponds to the value of that attribute observed for the corresponding
    sample in ds """

    events = read_tsv(path2event_file)
    onsets = events['onset']
    offsets = events['onset'] + events['duration']
    time_coords = ds.sa.time_coords

    # initialize list that will contain an event per sample
    sa_per_sample = [None] * len(ds)
    # loop through events dataframe
    for i in range(len(onsets)):
        # find index of samples where events onset/offset
        idx_onset = np.argwhere(time_coords >= onsets[i])[0,0] 
        idx_offset = np.argwhere(time_coords < offsets[i])[-1,0] + 1 + padding
        # populate list with appropriate attr
        for j in range(idx_onset,idx_offset+1):
            sa_per_sample[j] = events.iloc[i][attr_name]
            
    return sa_per_sample


def BIDSevents2sa_dict(ds, path2event_file, padding=0):
    """ returns a dict where keys are headers in BIDS_events.tsv (attributes)
    and values are a list, with the same length as ds where each entry
    is the attribute value for the corresponding sample """
    events = read_tsv(path2event_file)

    # take all cols from _events header not including 'onset' and 'duration'
    attr_list = [e for e in events.keys() if e not in ['onset','duration']]    

    sa_dict = {}
    # loop through header of _events.tsv, populate dict with sa's in events.tsv
    for attr_name in attr_list:
        sa_per_sample = get_sa_per_sample(ds,attr_name,path2event_file,padding)
        assert len(sa_per_sample) == len(ds)
        # populate dict
        sa_dict[attr_name] = sa_per_sample         
    return sa_dict


def BIDSevents2sa(ds, path2event_file, pading=0):
    """ populate DataSet with sample attributes found in BIDS_events.tsv"""
    sa_dict = BIDSevents2sa_dict(ds,path2event_file,pading)
    for sa_name in sa_dict.keys():    
        ds.sa[sa_name] = sa_dict[sa_name]
    return ds

