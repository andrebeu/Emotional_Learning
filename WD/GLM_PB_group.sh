#!/usr/bin/env bash

GLMresults_dir=$1
# GLMresults_dir=${bids_dir}/deriv_data/GLMcbc-output_TASK-${task}_ROI-${roi}
task=$2
# task='pain'
roi=$3
# roi='global'


# paths and folders
main_dir=${GLMresults_dir%visser_replicate*}/visser_replicate
bids_dir=${main_dir}/BIDSdataset
wd_dir=${main_dir}/WD_visser_replicate


# group GLM folder
groupGLM_folder="${bids_dir}/deriv_data/GLMgroup_TASK-${task}_ROI${roi}"

if [ -d ${groupGLM_folder} ];then
    echo "rm existing group GLM dir? y/n"
    read rmGLM
fi
if [ ${rmGLM} == 'y' ];then
    rm -rf ${groupGLM_folder}
fi

mkdir -p ${groupGLM_folder}
cd ${groupGLM_folder}


# subject beta volumes (input for ttest)
all_betavolumes="${GLMresults_dir}/sub-???_TASK-${task}_ROI-${roi}_GLMresults-AFNIbucket+tlrc.HEAD"


echo
echo "RUNNING GROUP T-TEST"
echo


# ttest tcp2 - tcm2 (only later trials)
3dttest++ -paired -AminusB \
          -labelA "CSplus2"    \
          -setA "${all_betavolumes}[targetCSplus2#0_Coef]" \
          -labelB "CSminus2"   \
          -setB "${all_betavolumes}[targetCSminus2#0_Coef]" \
          -prefix "GLMgroup-bucket_TASK-${task}_ROI-${roi}"   



# ttest tcp - tcm (all trials)
# cd ${groupGLM_folder}
# 3dttest++ -paired -AminusB \
#           -labelA "CSplus"    \
#           -setA "${all_betavolumes}[targetCSplus#0_Coef]" \
#           -labelB "CSminus"   \
#           -setB "${all_betavolumes}[targetCSminus#0_Coef]" \
#           -prefix "GLMgroup-bucket_TASK-${task}_ROI-${roi}"   \

