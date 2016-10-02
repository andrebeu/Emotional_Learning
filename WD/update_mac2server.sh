#!/usr/bin/env bash

## DIRECTORIES
MAC_maindir=~/Documents/fMRI/RVstudy/visser_replicate
SERV_maindir=srm254@hd-hni.cac.cornell.edu:/home/fs01/srm254/visser_replicate

## WD 
SERV_WD=${SERV_maindir}/WD_visser_replicate/
MAC_WD=${MAC_maindir}/WD_visser_replicate/
echo 
echo "updating WD"
echo
rsync -vam --update --exclude='*pyc' ${MAC_WD}/* ${SERV_WD}


## ONSET FILES
MAC_rawonsets_folder=${MAC_maindir}/rawonsets
SERV_rawonsets_folder=${SERV_maindir}/rawonsets
echo
echo "updating onset files"
echo
# rsync -vam --update ${MAC_rawonsets_folder}/* ${SERV_rawonsets_folder}


# # chmod status # #
echo
echo "updating CHMOD of bash files"
echo
# ssh srm254@hd-hni.cac.cornell.edu 'bash -s' < update_chmod serv
 
