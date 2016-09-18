#!/usr/bin/env bash

### ### DIRECTORY ### ### 
if [[ $(pwd) == *"srm254"* ]]; then
    main_dir="/home/fs01/srm254/visser_replicate"
fi
if [[ $(pwd) == *"andrebeukers"* ]];then
    main_dir="/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate"
fi

### ### INPUT OPTIONS ### ### 

# task : 'pain', 'brush'
task=$1
# ROI : 'amyg', 'hip', 'global' (i.e. no mask)
roi=$2
# 'tbt', 'cbc'
tbt_cbc=$3


## ## PATHS ## ##
bids_dir=${main_dir}/BIDSdataset
WD_dir=${main_dir}/WD_visser_replicate
stimes_dir=${bids_dir}/deriv_data/stimes-${tbt_cbc}
masks_dir=${bids_dir}/deriv_data/masks


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
    Rmodel='dmBLOCK'
    stimes_option=-stim_times_IM
else
    Rmodel='BLOCK(4,1)'
    stimes_option=-stim_times
fi

# MASK options
if [ ${roi} = "global" ]; then
    mask_option=" "
else
    mask_option=-mask ${masks_dir}/${roi}ROI_lowres+tlrc
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
    path2_motionfile1=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-roll.1D
    path2_motionfile2=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-pitch.1D
    path2_motionfile3=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-yaw.1D
    path2_motionfile4=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-dL.1D
    path2_motionfile5=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-dS.1D
    path2_motionfile6=${raw_sub_dir}/func/motion/sub-${subj_num}_task-${task}*_motion-dP.1D
    
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
    path2_tp_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-targetCSplus_stimes-${tbt_cbc}.csv
    path2_tm_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-targetCSminus_stimes-${tbt_cbc}.csv
    path2_cp_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-conditCSplus_stimes-${tbt_cbc}.csv
    path2_cm_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-conditCSminus_stimes-${tbt_cbc}.csv
    path2_us_stimes_file=${stimes_dir}/sub-${subj_num}_task-${task}_trial-US_stimes-${tbt_cbc}.csv

    
    # SUBJECT GLM ## SEP 1,2
    3dDeconvolve -input ${path2_boldfile} \
            -polort A -nofullf_atall -tout \
            ${mask_option} \
            \
            -gltsym 'SYM: targetCSplus2 -targetCSminus2'  \
            -glt_label 1 CSplus2_minus_CSminus2           \
            \
            -num_stimts 13 -local_times \
            \
            -stim_file 1 ${path2_motionfile1} -stim_base 1 -stim_label 1 mot_roll      \
            -stim_file 2 ${path2_motionfile2} -stim_base 2 -stim_label 2 mot_pitch     \
            -stim_file 3 ${path2_motionfile3} -stim_base 3 -stim_label 3 mot_yaw       \
            -stim_file 4 ${path2_motionfile4} -stim_base 4 -stim_label 4 mot_dS        \
            -stim_file 5 ${path2_motionfile5} -stim_base 5 -stim_label 5 mot_dL        \
            -stim_file 6 ${path2_motionfile6} -stim_base 6 -stim_label 6 mot_dP        \
            \
            -stim_label 7 targetCSplus1         \
            ${stimes_option} 7 ${path2_tp1_stimes_file} ${Rmodel} \
            -stim_label 8 targetCSplus2         \
            ${stimes_option} 8 ${path2_tp2_stimes_file} ${Rmodel} \
            -stim_label 9 targetCSminus1        \
            ${stimes_option} 9 ${path2_tm1_stimes_file} ${Rmodel} \
            -stim_label 10 targetCSminus2        \
            ${stimes_option} 10 ${path2_tm2_stimes_file} ${Rmodel} \
            \
            -stim_label 11 conditCSplus          \
            ${stimes_option} 11 ${path2_cp_stimes_file} ${Rmodel} \
            -stim_label 12 conditCSminus         \
            ${stimes_option} 12 ${path2_cm_stimes_file} ${Rmodel} \
            -stim_label 13 US                    \
            ${stimes_option} 13 ${path2_us_stimes_file} ${Rmodel} \
            \
            -x1D sub-${subj_num}_GLM-designmat.1D       \
            -xjpeg sub-${subj_num}_GLM-designmat.jpg    \
            -bucket "sub-${subj_num}_TASK-${task}_ROI-${roi}_GLMresults-AFNIbucket" 


            ## ORIGINAL sep t,c agg 1,2
            # -num_stimts 11 -local_times \
            # \
            # -stim_file 1 ${path2_motionfile}'[0]' -stim_base 1 -stim_label 3 mot_roll      \
            # -stim_file 2 ${path2_motionfile}'[1]' -stim_base 2 -stim_label 4 mot_pitch     \
            # -stim_file 3 ${path2_motionfile}'[2]' -stim_base 3 -stim_label 5 mot_yaw       \
            # -stim_file 4 ${path2_motionfile}'[3]' -stim_base 4 -stim_label 6 mot_dS        \
            # -stim_file 5 ${path2_motionfile}'[4]' -stim_base 5 -stim_label 7 mot_dL        \
            # -stim_file 6 ${path2_motionfile}'[5]' -stim_base 6 -stim_label 8 mot_dP        \
            # \
            # -stim_label 7 targetCSplus \
            # ${stimes_option} 7 ${path2_tp_stimes_file} ${Rmodel} \
            # -stim_label 8 targetCSminus \
            # ${stimes_option} 8 ${path2_tm_stimes_file} ${Rmodel} \
            # \
            # -stim_label 9 conditCSplus          \
            # ${stimes_option} 9 ${path2_cp_stimes_file} ${Rmodel} \
            # -stim_label 10 conditCSminus         \
            # ${stimes_option} 10 ${path2_cm_stimes_file} ${Rmodel} \
            # -stim_label 11 US                    \
            # ${stimes_option} 11 ${path2_us_stimes_file} ${Rmodel} \

            ## SEP 1,2
            # -num_stimts 13 -local_times \
            # \
            # -stim_file 1 ${path2_motionfile}'[0]' -stim_base 1 -stim_label 3 mot_roll      \
            # -stim_file 2 ${path2_motionfile}'[1]' -stim_base 2 -stim_label 4 mot_pitch     \
            # -stim_file 3 ${path2_motionfile}'[2]' -stim_base 3 -stim_label 5 mot_yaw       \
            # -stim_file 4 ${path2_motionfile}'[3]' -stim_base 4 -stim_label 6 mot_dS        \
            # -stim_file 5 ${path2_motionfile}'[4]' -stim_base 5 -stim_label 7 mot_dL        \
            # -stim_file 6 ${path2_motionfile}'[5]' -stim_base 6 -stim_label 8 mot_dP        \
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
            # ${stimes_option} 11 ${path2_cp_stimes_file} ${Rmodel} \
            # -stim_label 12 conditCSminus         \
            # ${stimes_option} 12 ${path2_cm_stimes_file} ${Rmodel} \
            # -stim_label 13 US                    \
            # ${stimes_option} 13 ${path2_us_stimes_file} ${Rmodel} \

            ## AGG t,c SEP 1,2
            # -num_stimts 11 -local_times \
            # \
            # -stim_file 1 ${path2_motionfile}'[0]' -stim_base 1 -stim_label 3 mot_roll      \
            # -stim_file 2 ${path2_motionfile}'[1]' -stim_base 2 -stim_label 4 mot_pitch     \
            # -stim_file 3 ${path2_motionfile}'[2]' -stim_base 3 -stim_label 5 mot_yaw       \
            # -stim_file 4 ${path2_motionfile}'[3]' -stim_base 4 -stim_label 6 mot_dS        \
            # -stim_file 5 ${path2_motionfile}'[4]' -stim_base 5 -stim_label 7 mot_dL        \
            # -stim_file 6 ${path2_motionfile}'[5]' -stim_base 6 -stim_label 8 mot_dP        \
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
            # ${stimes_option} 11 ${path2_us_stimes_file} ${Rmodel} \

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


