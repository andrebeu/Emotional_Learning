import os
import sys
from os.path import join as opj
import pandas as pd
import numpy as np
import csv

if 'andrebeukers' in os.getcwd().split('/'):
    path2_BIDS = '/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset'
elif 'srm254' in os.getcwd().split('/'):
    path2_BIDS = "/home/fs01/srm254/visser_replicate/BIDSdataset"

# PATHS
path2_errors = opj(path2_BIDS, "errors.csv")
errorsDF = pd.Series.from_csv(path2_errors, header=None)
path2_behave = opj(path2_BIDS, "behavioural.csv")
behaveDF = pd.read_csv(path2_behave)

## initialize exclusion.csv FILE
path2_exclusion = opj(path2_BIDS, "exclusion.csv")
if os.path.isfile(path2_exclusion):
    os.remove(path2_exclusion)

with open(path2_exclusion, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['exclusion criterion','subs'])
    pass

# append
def exclusion_file(sub_nums,criteria):
    df_2append = pd.DataFrame([criteria, sub_nums], index=None).transpose()
    df_2append.to_csv(path2_exclusion, mode='a', index=None, header=None)


def bymotion(th):
    global errorsDF
    th = float(th)
    print 'motion threshold at %.1fmm' % th
    sids = np.unique(errorsDF[errorsDF.str.find('%.1fmm'%th) != -1].index)
    sub_nums = map(lambda x: int(x.split('-')[-1]), sids)
    print "bymotion: ", sub_nums
    exclusion_file(sub_nums,"motion > %.1fmm" % th)
    return sub_nums

def bytask(task):
    print 'problem with %s trials' % task
    prob_task_bool = errorsDF.str.find(task) != -1
    not_motion_bool = errorsDF.str.find('exceeds') == -1
    sids = np.unique(errorsDF[not_motion_bool & prob_task_bool].index)
    sub_nums = map(lambda x: int(x.split('-')[-1]), sids)
    print "bytask: ", sub_nums
    exclusion_file(sub_nums,'missing files')
    return sub_nums

def bybehave(th):
    global behaveDF
    idx = (behaveDF['diff'] < -abs(th))
    sub_nums = map(lambda x: int(x.split('-')[-1]), behaveDF[idx]['sub'])
    print "bybehave :", sub_nums
    exclusion_file(sub_nums,'conditioning < %s' % th)
    return sub_nums