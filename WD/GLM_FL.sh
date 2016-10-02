#!/usr/bin/env bash


## ## PATHS ## ##

if [[ $(pwd) == *"srm254"* ]]; then
    main_dir="/home/fs01/srm254/visser_replicate"
fi
if [[ $(pwd) == *"andrebeukers"* ]];then
    main_dir="/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate"
fi

bids_dir=${main_dir}/BIDSdataset
wd_dir=${main_dir}/WD_visser_replicate
stimes_dir=${bids_dir}/deriv_data/stimes-cbc
masks_dir=${bids_dir}/deriv_data/masks

# GLMresults folder
GLMresults_dir=${bids_dir}/deriv_data/'GLMresults_TASK-funcloc'
if [ -d ${GLMresults_dir} ];then
    echo "rm existing GLM dir? y/n"
    read rmGLM
fi
if [ ${rmGLM} == 'y' ];then
    rm -rf ${GLMresults_dir}
fi

mkdir -p ${GLMresults_dir}
cd ${GLMresults_dir}


## ## SUBJECT GLMS ## ##

# Basis function for GLM convolution
Rmodel='BLOCK(18,1)'
# order of null model polynomial
poly_ord="A"

for raw_sub_dir in ${bids_dir}/raw_data/sub-???; do
    
    subj_num="${raw_sub_dir##*-}"
    echo " "
    echo "*****__***** subject: "${subj_num}" *****__*****"
    echo "*****__***** subject: funcloc GLM *****__*****"
    echo " "

    # BOLD file
    path2_func_folder=${raw_sub_dir}/func
    path2_boldfile=${path2_func_folder}/sub-${subj_num}_task-funcloc*_bold.nii.gz

    # stim_times csv files
    path2_face_stimes_file=${stimes_dir}/sub-${subj_num}_task-funcloc_trial-face_stimes-cbc.csv
    path2_house_stimes_file=${stimes_dir}/sub-${subj_num}_task-funcloc_trial-house_stimes-cbc.csv

    # motion files
    path2_motionfile1=${raw_sub_dir}/func/motion/sub-${subj_num}_task-funcloc*_motion-roll.1D
    path2_motionfile2=${raw_sub_dir}/func/motion/sub-${subj_num}_task-funcloc*_motion-pitch.1D
    path2_motionfile3=${raw_sub_dir}/func/motion/sub-${subj_num}_task-funcloc*_motion-yaw.1D
    path2_motionfile4=${raw_sub_dir}/func/motion/sub-${subj_num}_task-funcloc*_motion-dL.1D
    path2_motionfile5=${raw_sub_dir}/func/motion/sub-${subj_num}_task-funcloc*_motion-dS.1D
    path2_motionfile6=${raw_sub_dir}/func/motion/sub-${subj_num}_task-funcloc*_motion-dP.1D

    ## make GLMoutput_dir/sub-??? 
    # GLMoutput_subj_folder=${GLMoutput_dir}/sub-${subj_num}
    # mkdir -p ${GLMoutput_subj_folder}
    # cd ${GLMoutput_subj_folder}

    # SUBJECT GLM 
    3dDeconvolve -input ${path2_boldfile} \
        -polort ${poly_ord} \
        -num_stimts 8 -local_times \
        -stim_label 1 face \
        -stim_times 1 ${path2_face_stimes_file} ${Rmodel} \
        -stim_label 2 house \
        -stim_times 2 ${path2_house_stimes_file} ${Rmodel} \
        \
        -stim_file 3 ${path2_motionfile1} -stim_base 3 -stim_label 3 mot_roll      \
        -stim_file 4 ${path2_motionfile2} -stim_base 4 -stim_label 4 mot_pitch     \
        -stim_file 5 ${path2_motionfile3} -stim_base 5 -stim_label 5 mot_yaw       \
        -stim_file 6 ${path2_motionfile4} -stim_base 6 -stim_label 6 mot_dS        \
        -stim_file 7 ${path2_motionfile5} -stim_base 7 -stim_label 7 mot_dL        \
        -stim_file 8 ${path2_motionfile6} -stim_base 8 -stim_label 8 mot_dP        \
        \
        -x1D sub-${subj_num}_GLM-designmat.1D \
        -xjpeg sub-${subj_num}_GLM-designmat.jpg \
        -gltsym 'SYM: face -house'     \
        -glt_label 1 face_minus_house   \
        -tout -nofullf_atall \
        -bucket "sub-${subj_num}_TASK-funcloc_GLMresults-bucket" 
done 

# masks_FLsubject.sh ${GLMresults_dir}

## GROUP GLM ##
# cd ${WD_dir}
# GLM_FL_group.sh ${GLMoutput_dir}
