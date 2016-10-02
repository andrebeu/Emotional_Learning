import os
from os.path import join as opj
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


def get_dsm_figpaths(dsm,group=False):
    # returns dict with paths for figs
    figpaths = dict()

    # paths
    if 'andrebeukers' in os.getcwd().split('/'):
        bids_dir = '/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset'
    elif 'srm254' in os.getcwd().split('/'):
        bids_dir = "/home/fs01/srm254/visser_replicate/BIDSdataset"

    # sample attributes
    task = np.unique(dsm.sa.task)[0]
    roi = np.unique(dsm.sa.roi)[0]
    if np.unique(dsm.sa.condit): cond = "conditioners"
    else: cond = "nonconditioners"

    # build dir
    RSAresults_folder = "RSA-results_TASK-%s_ROI-%s" % (task, roi)
    RSAresults_dir = opj(bids_dir, "deriv_data", RSAresults_folder)

    # group RSA
    if group==False:
        sub_num = np.unique(dsm.sa.sub_num)[0]
        figname_dsm = "sub-%.3i_ROI-%s_RSA-dsm" % (int(sub_num), roi)
        figpaths['dsm'] = opj(RSAresults_dir, figname_dsm)
        figname_dmchange = "sub-%.3i_ROI-%s_RSA-dmchange" % (int(sub_num), roi)
        figpaths['dmchange'] = opj(RSAresults_dir, figname_dmchange)
        return figpaths
    
    # subj RSA
    elif group==True:
        figname_dsm = "ROI-%s_RSA-%s_dsm" % (roi,cond)
        figpaths['dsm'] = opj(RSAresults_dir, figname_dsm)
        figname_dmchange = "ROI-%s_RSA-dmchange" % (roi)
        figpaths['dmchange'] = opj(RSAresults_dir, figname_dmchange)
        return figpaths


## dsms

def plot_dsm(dsm, title = 'Corr distance'):
    # figure
    fig = plt.figure(figsize=(10,8))
    plt.imshow(dsm, interpolation='nearest')
    plt.xticks(np.arange(len(dsm))+.5, dsm.sa.trial, rotation=-45)
    plt.yticks(range(len(dsm)), dsm.sa.trial)
    plt.title(title)
    plt.clim(-1, 1)
    plt.colorbar()

    ax = fig.add_subplot(111)
    for xy in [-.5,6.5,13.5]:
        ax.add_patch(mpl.patches.Rectangle((xy,xy),
            7,7,linewidth=3,color='black',fill=False))

    

def dsm_fig(dsm,group=False):
    plot_dsm(dsm, title='Corr distance')
    figpaths = get_dsm_figpaths(dsm,group)
    plt.savefig(figpaths['dsm'])
    plt.close('all')


## tbt change line plot

def get_dmchange(dsm, stim):

    idx_stim = dsm.sa.stim == stim
    stim_dsm = dsm[idx_stim,idx_stim]

    # index for off diagonal
    idx_diag = np.diag_indices(len(stim_dsm)-1)
    idx_rows = idx_diag[0]+1 
    idx_cols = idx_diag[1]

    # plot off diagonal for specified trial_type
    dm_change = stim_dsm.samples[(idx_rows,idx_cols)]

    return dm_change

def dmchange_fig(dsm,group=False):

    if np.unique(dsm.sa.condit): label='_condit'
    else: label='_noncondit'
    for stim in ['CS+','CS-']:

        # plot dissimilarity change
        dmchange = get_dmchange(dsm, stim)
        plt.plot(dmchange,label=stim)
        plt.legend()

        # labeling x
        trial_num = np.arange(len(dmchange)) + 1
        xlab = ["%i - %i" % (trial_num[i], trial_num[i]+1) 
                for i in range(len(trial_num))]
        plt.xticks(np.arange(len(dmchange)), xlab, rotation = -45)
        plt.xticks(np.arange(len(dmchange)), xlab, rotation = -45)

    # save
    figpath = get_dsm_figpaths(dsm,group=group)['dmchange']+label
    plt.title(figpath.split('/')[-1])
    plt.savefig(figpath)
    plt.close('all')

def dmchange_fig2(dsm_c,dsm_n,group=True):

    for stim in ['CS+']:

        # plot dissimilarity change
        dmchange_c = get_dmchange(dsm_c, stim)
        dmchange_n = get_dmchange(dsm_n, stim)

        plt.plot(dmchange_c,label="C "+stim)
        plt.legend()
        plt.plot(dmchange_n,label="N "+stim)
        plt.legend()

        # labeling x
        trial_num = np.arange(len(dmchange_c)) + 1
        xlab = ["%i - %i" % (trial_num[i], trial_num[i]+1) 
                for i in range(len(trial_num))]
        plt.xticks(np.arange(len(dmchange_c)), xlab, rotation = -45)
        plt.xticks(np.arange(len(dmchange_c)), xlab, rotation = -45)

    # save
    figpath = get_dsm_figpaths(dsm_c,group=group)['dmchange']+"_CvsN"
    plt.title(figpath.split('/')[-1])
    plt.savefig(figpath)
    plt.close('all')


def dmchange_diff_fig(dsm_c,dsm_n,group=True):

    # plot dissimilarity change
    dmchange_c = get_dmchange(dsm_c, 'CS+') - get_dmchange(dsm_c, 'CS-')
    dmchange_n = get_dmchange(dsm_n, 'CS+') - get_dmchange(dsm_n, 'CS-')
    
    plt.plot(dmchange_c, label='C: CS+ - CS-')
    plt.legend()
    plt.plot(dmchange_n, label='N: CS+ - CS-')
    plt.legend()

    # labeling x
    trial_num = np.arange(len(dmchange_c)) + 1
    xlab = ["%i - %i" % (trial_num[i], trial_num[i]+1) 
            for i in range(len(trial_num))]
    plt.xticks(np.arange(len(dmchange_c)), xlab, rotation = -45)
    plt.xticks(np.arange(len(dmchange_c)), xlab, rotation = -45)

    # save
    figpath = get_dsm_figpaths(dsm_c,group=group)['dmchange']+"_diff"
    plt.title(figpath.split('/')[-1])
    plt.savefig(figpath)
    plt.close('all')
