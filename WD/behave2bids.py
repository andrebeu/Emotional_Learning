import os
from os.path import join as opj
from glob import glob
import pandas as pd
import csv
import debug_RV

## PATHS
if 'andrebeukers' in os.getcwd().split('/'):
    print 'behave onmac'
    path2_maindir = '/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate'
    path2_batch_folder = opj(path2_maindir, "BATCH_4")
elif 'srm254' in os.getcwd().split('/'):
    print 'behave onserv'
    path2_maindir = "/home/fs01/srm254/visser_replicate"
    path2_batch_folder = opj(path2_maindir, 'BATCH_full_aug9')

path2_BIDS = opj(os.path.split(path2_batch_folder)[0], "BIDSdataset")
path2_rawonsets_folder = opj(path2_maindir, 'rawonsets')


## initialize behavioural.csv FILE
path2_beahve_csv = opj(path2_BIDS, "behavioural.csv")
if os.path.isfile(path2_beahve_csv):
    os.remove(path2_beahve_csv)

with open(path2_beahve_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['sub','rating_CSplus','rating_CSminus', 'diff'])
    pass



## loop through BIDSevents, populate behavioural.csv
for path2_events in glob(opj(path2_BIDS,"raw_data",'sub-*','func','sub-*_task-pain_file-*_events.csv')):
    sub_num = int(path2_events.split('/')[-1].split('_')[0].split('-')[-1])
 
    try:
        # build DF from behavioural rawonsets
        path2_rating = glob(opj(path2_rawonsets_folder,'%i_scan*ratings*' % sub_num))
        ratingDF = pd.read_csv(path2_rating[0])[['rating.response','rating_2.response','face']].iloc[1:,:]
        assert len(path2_rating) == 1
        for s in range(6):
            # gets name of stim from path
            ratingDF['face'].iloc[s] = ratingDF['face'].str.split('\\').iloc[s][-1].split('.')[0]
        
        # label rows CS+ or CS-
        eventsDF = pd.read_csv(path2_events)
        CSplus = eventsDF[eventsDF['CS'] == 'CSplus']['stim_name'].unique()
        CSminus = eventsDF[eventsDF['CS'] == 'CSminus']['stim_name'].unique()

        # get mean ratings
        rate_plus = ratingDF[(ratingDF['face'] == CSplus[0]) | (ratingDF['face'] == CSplus[1])].mean().mean()
        rate_minus = ratingDF[ratingDF['face'] == CSminus[0]].mean().mean()
        diff = rate_plus - rate_minus

        # write to behavioural.csv
        df_2append = pd.DataFrame(["sub-%.3i" % sub_num, rate_plus, rate_minus, diff], index=None).transpose()
        df_2append.to_csv(path2_beahve_csv, mode='a', index=None, header=None)

    except: 
        debug_RV.debugger_errors(path2_BIDS, "sub-%.3i" % int(sub_num), "pain_missing_behave")



