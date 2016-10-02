import os
from os.path import join as opj
from os.path import split as ops
from glob import glob 
from shutil import copyfile

import debug_RV
from rawonsets2bidsevents import rawonsets2bidsevents
from bidsevents2stimtimes import bidsevents2stimtimes


""" Get paths """

def get_batchpaths(main_dir):
    """ input dir where batch folders are """
    return glob(opj(main_dir,'BATCH_*'))

def get_subj_batchpaths(path2_batch_folder):
    """ input batch folder"""
    return glob(opj(path2_batch_folder,'S*'))

def get_anat_batchpath(subj_batchpath):
    """ gets paths to medn files"""
    return glob(opj(subj_batchpath, 'medata', 'anat.nii'))[0]

def get_run_batchpaths(subj_batchpath):
    """ input: path/to/subj """
    return glob(opj(subj_batchpath, 'medata', 'run*medn*'))


""" get ids """

# returns subj number as ???
def get_subj_id(subj_batchpath):
    return "sub-%.3i" % int( ops(subj_batchpath)[-1][1:] )

# returns run number
def get_run_id(run_batchpath):
    return ops(run_batchpath)[-1][len('run'):len('run')+2]


""" read scaninfo file """ 

def get_scinfo_batchpath(run_batchpath):
    """ input: path/to/*medn*file 
        output: path/to/scannerinfo/scan_* """
    subj_batchpath = ops(ops(run_batchpath)[0])[0]
    subj_run_no = "%s" % int(ops(run_batchpath)[-1].split('.')[0][len("run"):])
    return opj(subj_batchpath,'scannerinfo','scan_' + subj_run_no)


def get_run_task(run_batchpath):
    """ reads scinfo file and returns task """
    scinfo_path = get_scinfo_batchpath(run_batchpath)
    try:
        scinfo = open(scinfo_path).read()
        if 'Func Loc' in scinfo: return 'funcloc'
        if 'Brush' in scinfo: return 'brush'
        if 'Pain' in scinfo: return 'pain'
        if 'Resting' in scinfo: return 'rest'
        if 'Morph' in scinfo: return 'morph'
    except:

        print 'Error reading scanner info: ', scinfo_path
        return 'error'

    else: return 'na'


""" Setting up BIDS folder structure"""


# loop through subj_batchpaths
# make BIDS folder for each subject 
def make_bidsdir(path2_batch_folder):

    # make main folder
    path2_BIDSdataset = opj( ops(path2_batch_folder)[0], 'BIDSdataset' )
    if not os.path.isdir(path2_BIDSdataset):
        os.mkdir(path2_BIDSdataset)

        # deriv_data folders
        os.makedirs(opj( path2_BIDSdataset, 'prob_subj'))
        os.makedirs(opj( path2_BIDSdataset, 'deriv_data'))
        os.makedirs(opj( path2_BIDSdataset, 'deriv_data', 'masks'))
    
        # subject specific folders
        for subj_batchpath in get_subj_batchpaths(path2_batch_folder):
            sid = get_subj_id(subj_batchpath)
            
            os.makedirs(opj( path2_BIDSdataset, 'raw_data', sid, 'func' ))
            os.makedirs(opj( path2_BIDSdataset, 'raw_data', sid, 'anat' ))
            


    return path2_BIDSdataset


""" copy and rename files """


# rawonsets_folder_path = "/Users/andrebeukers/Documents/fMRI/RVstudy/miniDS/rawonsets"
# find path to rawonsets for given subject
def get_path2_rawonsets_files(subj_batchpath, path2_rawonsets_folder, path2_BIDSdataset):
    
    sid = get_subj_id(subj_batchpath)
    sub_no = int(sid.split('-')[-1])

    path2_rawonsets_files = {}
    tasks = ["brush","pain","FL"]
    for t in tasks:
        
        temp = glob(opj( path2_rawonsets_folder, "%i*%s*" % (sub_no,t) ))

        if len(temp) == 0:
            error_message = '%s missing %s rawonset file' % (sid,t)
            print error_message
            debug_RV.debugger_errors(path2_BIDSdataset, sid, error_message)

        elif len(temp) > 1:
            error_message = '%s too many %s rawonset files' % (sid,t)
            print error_message
            debug_RV.debugger_errors(path2_BIDSdataset, sid, error_message)

        elif len(temp) == 1:
            path2_rawonsets_files[t] = temp[0]
        
    return path2_rawonsets_files


# copy func and anat from BATCH to BIDSdataset/sub-
# helper for batch2bids
def batch2bids_subj(subj_batchpath, path2_BIDSdataset):

    # path to BIDSdataset/raw_data/sub-???
    sid = get_subj_id(subj_batchpath)
    subj_bids_path = opj(path2_BIDSdataset, "raw_data", sid)

    ## anat
    try:
        anat_batch_fpath = get_anat_batchpath(subj_batchpath)
        anat_bids_fpath = opj(subj_bids_path ,'anat', sid + '_anat.nii')

        ### copy and rename anat 
        # #copyfile(anat_batch_fpath, anat_bids_fpath)

    except:
        error_message = "%s b2b problem copying anat" % sid
        print error_message
        # debug_RV.debugger_errors(path2_BIDSdataset, sid, error_message)

    ## BOLDs
    for run_batchpath in get_run_batchpaths(subj_batchpath):
        
        try: 
            # assemble bids_bold_path
            task = get_run_task(run_batchpath)
            rid = get_run_id(run_batchpath)
            bids_func_path = opj(subj_bids_path,'func')
            bids_bold_fname = sid + '_task-' + task + '_run-' + rid + '_bold.nii.gz' 
            bids_bold_fpath = opj(bids_func_path, bids_bold_fname)

            ### copy and rename BOLD files
            copyfile(run_batchpath, bids_bold_fpath)

            # MOTION FILE
            try: 
                bids_motion_fname = sid + '_task-' + task + '_run-' + rid + '_motion.1D' 
                bids_motion_fpath = opj(bids_func_path, bids_motion_fname)
                batch_motion_fpath = opj(ops(run_batchpath)[0], "meica.run%s.e0123" % rid, "motion.1D")
                copyfile(batch_motion_fpath, bids_motion_fpath)
            except:
                error_message = "%s b2b problem copying motion files" % sid
                print error_message
                debug_RV.debugger_errors(path2_BIDSdataset, sid, error_message)

        except:
            error_message = "%s b2b problem copying BOLD files" % sid
            print error_message
            debug_RV.debugger_errors(path2_BIDSdataset, sid, error_message)


    return sid + ' is now in the BIDSdataset folder'


""" Final wrapper"""

# loop through subj_batchpaths copying and renaming 
# anat, func and onset files
# calls rawonsets2bidsevents
def batch2bids(path2_batch_folder, path2_rawonsets_folder):

    # make BIDSdataset folder if one d/n exist
    path2_BIDSdataset = make_bidsdir(path2_batch_folder)

    rawonsets_tasks = ["pain","brush","FL"]
    
    for subj_batchpath in get_subj_batchpaths(path2_batch_folder):
        
        sid = get_subj_id(subj_batchpath)
        print
        print 'working on subj: %s' % sid

        ## call batch2bids_subj on each subj_batchpath
        batch2bids_subj(subj_batchpath, path2_BIDSdataset)

        # dict of all rawonset files
        rawonsets_files = get_path2_rawonsets_files(subj_batchpath, 
            path2_rawonsets_folder, path2_BIDSdataset)

        # call rawonsets2bidsevents on each path2_rawonsets_file
        for t in rawonsets_tasks:
            try:
                path2_rawonsets_file = rawonsets_files[t]
                rawonsets2bidsevents(path2_rawonsets_file, path2_BIDSdataset)
            except:
                pass
                
    ## STIM TIMES
    for task_name in ["pain", "brush"]:
        bidsevents2stimtimes(path2_BIDSdataset, task_name, "tbt")
    for task_name in ["funcloc", "pain", "brush"]:
        bidsevents2stimtimes(path2_BIDSdataset, task_name, "cbc")

    # make motion files for AFNI
    print os.getcwd()
    import motion_files

    # check for missing bold and events files
    debug_RV.debugger_missing(path2_BIDSdataset)
    debug_RV.debugger_sort(path2_BIDSdataset)

    return path2_BIDSdataset


