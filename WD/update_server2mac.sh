#!/usr/bin/env bash


SERV_maindir=srm254@hd-hni.cac.cornell.edu:/home/fs01/srm254/visser_replicate
MAC_target_folder=~/Documents/fMRI/RVstudy/fromServ
mkdir -p ${MAC_target_folder}

if [ ${1} = "exclusion" ]; then
    echo "PULLING EXCLUSION FROM SERV"
    rsync -vam --update ${SERV_maindir}/BIDSdataset/exclusion.csv ${MAC_target_folder}
# elif [ ${1} = "RSA" ]; then
#     echo "RSA RESULTS"
#     SERV_deriv=${SERV_maindir}/BIDSdataset/deriv_data
#     rsync -vam --update --include='*' ${SERV_deriv}/RSA* ${MAC_target_folder}
else
    if [ ${1} = "behave" ]; then
        echo "PULLING BEHAVIOURAL FROM SERV"
        rsync -vam --update ${SERV_maindir}/BIDSdataset/behavioural.csv ${MAC_target_folder}
    elif [ ${1} = "errors" ]; then
        echo "PULLING ERROR LOG FROM SERV"
        rsync -vam --update ${SERV_maindir}/BIDSdataset/errors.csv ${MAC_target_folder}
    else
        echo "PULLING RESULTS FROM SERV"
        SERV_results=${SERV_maindir}/BIDSdataset/results
        SERV_deriv=${SERV_maindir}/BIDSdataset/deriv_data
        rsync -vam --update --include='*' ${SERV_deriv}/GLM* ${MAC_target_folder}
    fi
fi