#!/usr/bin/env bash

### ### INPUT OPTIONS ### ### 

# task : 'pain', 'brush'
task=$1
# ROI 'global', 'left_amygdala', 'right_amygdala'
roi=$2
# 'tbt', 'cbc'
tbt_cbc=$3


## ## PATHS ## ##
main_dir=$(bash get_maindir.sh)
bids_dir=${main_dir}/BIDSdataset
WD_dir=${main_dir}/WD_visser_replicate
stimes_dir=${bids_dir}/deriv_data/stimes-${tbt_cbc}
masks_dir=${bids_dir}/masks


# GLM output folder
GLMresults_dir=${bids_dir}/deriv_data/'GLM'${tbt_cbc}'-results_TASK-'${task}'_ROI-'${roi}

if [ -d ${GLMresults_dir} ];then
    echo "rm existing subject GLM dir? y/n"
    read rmGLM
fi
if [ ${rmGLM} == 'y' ];then
    rm -rf ${GLMresults_dir}
fi

mkdir -p ${GLMresults_dir}
cd ${GLMresults_dir}


### ### GLM OPTIONS ### ###

# TBT_CBC options 
if [ ${tbt_cbc} = "tbt" ]; then
    # dmBLOCK(p) ; p is peak value
    Rmodel='BLOCK(4,1)'
    stimes_option=-stim_times_IM
else
    Rmodel='BLOCK(4,1)'
    stimes_option=-stim_times
fi

# MASK options
if [ ${roi} = "global" ]; then
    mask_option=" "
else
    mask_option="-mask ${masks_dir}/${roi}ROI+tlrc"
fi


### ### SUBJECT GLMs ### ###

for raw_sub_dir in ${bids_dir}/raw_data/sub-???; do
    
    subj_num=${raw_sub_dir##*sub-}
    echo " "
    echo "*****__***** subject: "${subj_num}" *****__*****"
    echo " "

    ## path2 task*.nii.gz files in func folder
    path2_boldfile=${raw_sub_dir}/func/sub-${subj_num}_task-${task}*_bold.nii.gz

    ## path2 motion files
    motion_files1=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-roll.1D
    motion_files2=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-pitch.1D
    motion_files3=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-yaw.1D
    motion_files4=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-dL.1D
    motion_files5=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-dS.1D
    motion_files6=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-dP.1D
    
    ## path2 stim_times files 
    # sep 1,2 
    path2_tp1_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-targetCSplus1_stimes-${tbt_cbc}.csv
    path2_tp2_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-targetCSplus2_stimes-${tbt_cbc}.csv
    path2_tm1_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-targetCSminus1_stimes-${tbt_cbc}.csv
    path2_tm2_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-targetCSminus2_stimes-${tbt_cbc}.csv
    # agg t,c
    path2_p1_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-CSplus1_stimes-${tbt_cbc}.csv
    path2_p2_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-CSplus2_stimes-${tbt_cbc}.csv
    path2_m1_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-CSminus1_stimes-${tbt_cbc}.csv
    path2_m2_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-CSminus2_stimes-${tbt_cbc}.csv
    # original
    tp_stimes_files=${stimes_dir}/sub-${subj_num}_task-${task}_trial-targetCSplus_stimes-${tbt_cbc}.csv
    tm_stimes_files=${stimes_dir}/sub-${subj_num}_task-${task}_trial-targetCSminus_stimes-${tbt_cbc}.csv
    cp_stimes_files=${stimes_dir}/sub-${subj_num}_task-${task}_trial-conditCSplus_stimes-${tbt_cbc}.csv
    cm_stimes_files=${stimes_dir}/sub-${subj_num}_task-${task}_trial-conditCSminus_stimes-${tbt_cbc}.csv
    us_stimes_files=${stimes_dir}/sub-${subj_num}_task-${task}_trial-US_stimes-${tbt_cbc}.csv

    
    # SUBJECT GLM ## original
    3dDeconvolve -input ${path2_boldfile} \
            -polort A  \
            ${mask_option} \
            \
            -num_stimts 11 -local_times \
            \
            -stim_file 1 ${motion_files1} -stim_base 1 -stim_label 1 mot_roll      \
            -stim_file 2 ${motion_files2} -stim_base 2 -stim_label 2 mot_pitch     \
            -stim_file 3 ${motion_files3} -stim_base 3 -stim_label 3 mot_yaw       \
            -stim_file 4 ${motion_files4} -stim_base 4 -stim_label 4 mot_dL        \
            -stim_file 5 ${motion_files5} -stim_base 5 -stim_label 5 mot_dS        \
            -stim_file 6 ${motion_files6} -stim_base 6 -stim_label 6 mot_dP        \
            \
            -stim_label 7 targetCSplus \
            ${stimes_option} 7 ${tp_stimes_files} ${Rmodel} \
            -stim_label 8 targetCSminus \
            ${stimes_option} 8 ${tm_stimes_files} ${Rmodel} \
            \
            -stim_label 9 conditCSplus          \
            ${stimes_option} 9 ${cp_stimes_files} ${Rmodel} \
            -stim_label 10 conditCSminus         \
            ${stimes_option} 10 ${cm_stimes_files} ${Rmodel} \
            -stim_label 11 US                    \
            ${stimes_option} 11 ${us_stimes_files} ${Rmodel} \
            \
            -nofullf_atall \
            -x1D sub-${subj_num}_GLM-designmat.1D       \
            -xjpeg sub-${subj_num}_GLM-designmat.jpg    \
            -bucket "sub-${subj_num}_TASK-${task}_ROI-${roi}_GLMresults-AFNIbucket" 


            ## ORIGINAL sep t,c agg 1,2
            # -num_stimts 11 -local_times \
            # \
            # -stim_file 1 ${motion_files1} -stim_base 1 -stim_label 1 mot_roll      \
            # -stim_file 2 ${motion_files2} -stim_base 2 -stim_label 2 mot_pitch     \
            # -stim_file 3 ${motion_files3} -stim_base 3 -stim_label 3 mot_yaw       \
            # -stim_file 4 ${motion_files4} -stim_base 4 -stim_label 4 mot_dL        \
            # -stim_file 5 ${motion_files5} -stim_base 5 -stim_label 5 mot_dS        \
            # -stim_file 6 ${motion_files6} -stim_base 6 -stim_label 6 mot_dP        \
            # \
            # -stim_label 7 targetCSplus \
            # ${stimes_option} 7 ${tp_stimes_files} ${Rmodel} \
            # -stim_label 8 targetCSminus \
            # ${stimes_option} 8 ${tm_stimes_files} ${Rmodel} \
            # \
            # -stim_label 9 conditCSplus          \
            # ${stimes_option} 9 ${cp_stimes_files} ${Rmodel} \
            # -stim_label 10 conditCSminus         \
            # ${stimes_option} 10 ${cm_stimes_files} ${Rmodel} \
            # -stim_label 11 US                    \
            # ${stimes_option} 11 ${us_stimes_files} ${Rmodel} \

            ## SEP 1,2
            # -gltsym 'SYM: targetCSplus2 -targetCSminus2'  \
            # -glt_label 1 CSplus2_minus_CSminus2           \
            # -num_stimts 13 -local_times \
            # \
            # -stim_file 1 ${motion_files1} -stim_base 1 -stim_label 1 mot_roll      \
            # -stim_file 2 ${motion_files2} -stim_base 2 -stim_label 2 mot_pitch     \
            # -stim_file 3 ${motion_files3} -stim_base 3 -stim_label 3 mot_yaw       \
            # -stim_file 4 ${motion_files4} -stim_base 4 -stim_label 4 mot_dL        \
            # -stim_file 5 ${motion_files5} -stim_base 5 -stim_label 5 mot_dS        \
            # -stim_file 6 ${motion_files6} -stim_base 6 -stim_label 6 mot_dP        \
            # \
            # -stim_label 7 targetCSplus1         \
            # ${stimes_option} 7 ${path2_tp1_stimes_file} ${Rmodel} \
            # -stim_label 8 targetCSplus2         \
            # ${stimes_option} 8 ${path2_tp2_stimes_file} ${Rmodel} \
            # -stim_label 9 targetCSminus1        \
            # ${stimes_option} 9 ${path2_tm1_stimes_file} ${Rmodel} \
            # -stim_label 10 targetCSminus2        \
            # ${stimes_option} 10 ${path2_tm2_stimes_file} ${Rmodel} \
            # \
            # -stim_label 11 conditCSplus          \
            # ${stimes_option} 11 ${cp_stimes_files} ${Rmodel} \
            # -stim_label 12 conditCSminus         \
            # ${stimes_option} 12 ${cm_stimes_files} ${Rmodel} \
            # -stim_label 13 US                    \
            # ${stimes_option} 13 ${us_stimes_files} ${Rmodel} \
            # -tout \

            ## AGG t,c SEP 1,2
            # -num_stimts 11 -local_times \
            # \
            # -stim_file 1 ${motion_files1} -stim_base 1 -stim_label 1 mot_roll      \
            # -stim_file 2 ${motion_files2} -stim_base 2 -stim_label 2 mot_pitch     \
            # -stim_file 3 ${motion_files3} -stim_base 3 -stim_label 3 mot_yaw       \
            # -stim_file 4 ${motion_files4} -stim_base 4 -stim_label 4 mot_dL        \
            # -stim_file 5 ${motion_files5} -stim_base 5 -stim_label 5 mot_dS        \
            # -stim_file 6 ${motion_files6} -stim_base 6 -stim_label 6 mot_dP        \
            # \
            # -stim_label 7 CSplus1 \
            # ${stimes_option} 7 ${path2_p1_stimes_file} ${Rmodel} \
            # -stim_label 8 CSplus2 \
            # ${stimes_option} 8 ${path2_p2_stimes_file} ${Rmodel} \
            # -stim_label 9 CSminus1         \
            # ${stimes_option} 9 ${path2_m1_stimes_file} ${Rmodel} \
            # -stim_label 10 CSminus2         \
            # ${stimes_option} 10 ${path2_m2_stimes_file} ${Rmodel} \
            # -stim_label 11 US                    \
            # ${stimes_option} 11 ${us_stimes_files} ${Rmodel} \
            # -tout \

    # converting to .nii.gz
    AFNIbucket_fname="sub-${subj_num}_TASK-${task}_ROI-${roi}_GLMresults-AFNIbucket+tlrc.BRIK"
    GLMresults_fname="sub-${subj_num}_TASK-${task}_ROI-${roi}_GLMresults-nifti.nii.gz"
    3dAFNItoNIFTI -prefix ${GLMresults_fname} ${AFNIbucket_fname}

done


### GROUP GLM ### 

cd ${WD_dir}
if [ ${tbt_cbc} = "cbc" ]; then
    GLM_PB_group.sh ${GLMresults_dir} ${task} ${roi}
fi


