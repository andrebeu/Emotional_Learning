import os
from os.path import join as opj
from os.path import split as ops
import pandas as pd
from glob import glob 
from shutil import copyfile
from rawonsets2bidsevents import rawonsets2bidsevents
from bidsevents2stimtimes import bidsevents2stimtimes
import debug_RV

## PATHS
if 'andrebeukers' in os.getcwd().split('/'):
    print 'b2b onmac'
    path2_maindir = '/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate'
    path2_batch_folder = opj(path2_maindir, "BATCH_4")
elif 'srm254' in os.getcwd().split('/'):
    print 'b2b onserv'
    path2_maindir = "/home/fs01/srm254/visser_replicate"
    path2_batch_folder = opj(path2_maindir, 'BATCH_full_aug9')


path2_BIDS = opj(ops(path2_batch_folder)[0], "BIDSdataset")
path2_rawonsets_folder = opj(path2_maindir, 'rawonsets')


# HELPER FUNCTION
def get_run_task(path2_run):
    """ reads scinfo file and returns task """
    try:
        scinfo = open(path2_scinfo).read()
        if 'Func Loc' in scinfo: return 'funcloc'
        if 'Brush' in scinfo: return 'brush'
        if 'Pain' in scinfo: return 'pain'
        if 'Resting' in scinfo: return 'rest'
        if 'Morph' in scinfo: return 'morph'
    except:
        print 'Error reading scanner info: ', path2_scinfo
        return 'error'
    else: return 'na'


## == B2B == ##

# error when dir already exists
try:
    os.makedirs(opj(path2_BIDS,"deriv_data"))
    os.makedirs(opj(path2_BIDS,"prob_subj"))
except: pass

# loop through subjects
for sub in glob(opj(path2_batch_folder,"S*")):
    
    sub_num = int(sub.split('/')[-1][1:])
    print "sub %.3i" % sub_num

    # make sub folders
    path2_func = opj(path2_BIDS,"raw_data","sub-%.3i" % sub_num, "func") 
    path2_anat = opj(path2_BIDS,"raw_data","sub-%.3i" % sub_num, "anat") 
    try:
        os.makedirs(path2_func)
        os.makedirs(path2_anat)
    except: pass
    
    # anat
    anat_old = opj(sub,"medata","anat.nii")
    fname_anat = "sub-%.3i_anat.nii" % sub_num
    try: copyfile(anat_old, opj(path2_anat,fname_anat) )
    except: debug_RV.debugger_errors(path2_BIDS, "sub-%.3i" % sub_num, "anat")
    
    # rawonsets 
    for trial in ['pain','brush','FL']:
        path2_rawonsets_file = glob(opj(path2_rawonsets_folder, "%i_%s*.csv" % (sub_num, trial))) 
        
        try: 
            assert len(path2_rawonsets_file) == 1
            rawonsets2bidsevents(path2_rawonsets_file[0], path2_BIDS)
        except: 
            debug_RV.debugger_errors(path2_BIDS, 
                "sub-%.3i" % sub_num, "%s_rawonsets" % trial)

    # loop through runs
    for old_bold_path in glob(opj(sub,"medata","run??.e0123_medn.nii.gz")):

        # run info 
        run_num = int(old_bold_path.split('/')[-1].split('.')[0][3:])
        path2_scinfo = opj(old_bold_path.split('medata')[0], "scannerinfo", "scan_%i" % run_num)
        task = get_run_task(path2_scinfo)

        # bold 
        fname_bold = "sub-%.3i_task-%s_run-%.2i_bold.nii.gz" % (sub_num, task, run_num)
        try: copyfile(old_bold_path,opj(path2_func,fname_bold))
        except: debug_RV.debugger_errors(path2_BIDS, "sub-%.3i" % sub_num, "%s_bold" % task)

        # motion
        fname_motion = "sub-%.3i_task-%s_run-%.2i_motion.1D" % (sub_num, task, run_num)
        old_motion_path = opj(ops(old_bold_path)[0], "meica.run%.2i.e0123" % run_num, "motion.1D")
        try: copyfile(old_motion_path,opj(path2_func,fname_motion))
        except: debug_RV.debugger_errors(path2_BIDS, "sub-%.3i" % sub_num, "%s_motion" % task)


# behavioural file
import behave2bids

# stimtimes
import events2stimes_PB

# motion files for AFNI
import motion_files

# masks
from subprocess import call as subprocesscall
subprocesscall("bash masks_anat.sh", shell=True)

# check for missing bold and events files
debug_RV.debugger_sort(path2_BIDS)
