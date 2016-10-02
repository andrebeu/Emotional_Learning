#!/usr/bin/env bash

#### SUB 26 FL MOTION ARTEFACTS ####

FL_results=$1
# FL_results=/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset/deriv_data/GLMresults_task-funcloc

# FL_results=${bids_dir}/deriv_data/'GLMresults_task-funcloc'

main_dir="${FL_results%BIDSdataset*}"
deriv_dir="${main_dir}BIDSdataset/deriv_data"
masks_dir="${deriv_dir}/masks"
FLmasks_dir="${masks_dir}/FLmasks"

# output dir
mkdir -p ${FLmasks_dir}
cd ${FLmasks_dir}

path2_anat="${masks_dir}/fusiformROI_lowres+tlrc.HEAD"
# make anatomical FFA 
if [ ! -s ${path2_anat} ]; then
    bash masks_anat.sh ${main_dir}
fi

# make functionals and intersect
for sub in ${FL_results}/sub-???_TASK-funcloc_GLMresults-bucket+tlrc.BRIK; do
    
    sub_num=$(expr ${sub##*sub-} : '\([0-9][0-9][0-9]\)')
    echo 
    echo $sub_num
    echo

    ## functional mask
    echo "--FUNCTIONAL MASK--"
    3dmerge -dxyz=1 -1clust_order 1 40 -1thresh 3.25    \
            -prefix sub-${sub_num}_mask-tempfunc "${sub}"[face_minus_house_GLT#0_Tstat]

    echo "--INTERSECT--"
    3dcalc -a sub-${sub_num}_mask-tempfunc+tlrc.HEAD -b ${path2_anat} -expr 'and(a,b)'  \
           -prefix sub-${sub_num}_FFAmask
 
done




# useful code
# 3dmerge
#     converts suprathreshold clusters into mask dataset
#     -prefix
#     -1clip val: clips intensities < abs(val) to zero
#     -1thresh thr: use threshold data to threshold intensities
#     -1dindex j: use sub-brick j as data source
#     -1tindex k: use sub-brick k as threshold
# 3dcalc 
#     combines rois
# whereami -omask 
#     generates report of roi voxels
