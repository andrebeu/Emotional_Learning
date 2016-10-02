import os
from os.path import join as opj 
from glob import glob 
import pandas as pd


# sort errors.csv file by sid
def debugger_sort(path2_BIDSdataset):
    path2_errors_csv = opj(path2_BIDSdataset, 'errors.csv')
    errors_csv = pd.read_csv(path2_errors_csv, header=None)
    errors_csv.sort_values(1).to_csv(path2_errors_csv, header=False, index=False)


# multi-purpose editing errors.csv
def debugger_errors(path2_BIDSdataset, sid, error_message):
    path2_errors_csv = opj(path2_BIDSdataset, "errors.csv")

    # make csv file if d/n exist
    if not os.path.isfile(path2_errors_csv): 
        with open(path2_errors_csv, 'w') as f:
            pass

    df_2append = pd.Series({sid:error_message})
    df_2append.to_csv(path2_errors_csv, mode='a', header = False)

# check for missing files
def debugger_missing(path2_BIDSdataset):
    bold_tasks = ['pain','brush','rest','funcloc']
    events_tasks = ['pain','brush','funcloc']

    ## loop through subjects
    missing_bold = {}; missing_events = {}; duplicate_events = {}
    for subj in glob(opj(path2_BIDSdataset,"raw_data","sub-???","func")):

        sid = subj.split('/')[-2].split('_')[0]

        subj_missing_bold = []
        subj_missing_events = []
        subj_duplicate_events = []

        ## check bold files
        for task in bold_tasks:
            subj_bold = glob(opj(subj, "*%s*_bold.nii.gz" % task))
            if not len(subj_bold):
                error_message="%s_missingBOLD" % (task)
                debugger_errors(path2_BIDSdataset, sid, error_message)

