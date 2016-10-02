#!/usr/bin/env bash

# paths
main_dir=$(bash get_maindir.sh)
bids_dir=${main_dir}/BIDSdataset
masks_dir=${bids_dir}/masks
WD_dir=${main_dir}/WD_visser_replicate
temp_dir=${WD_dir}/temp_dir

mkdir -p ${masks_dir}
mkdir -p ${temp_dir}
cd ${temp_dir}


sample_subj="${bids_dir}/raw_data/sub-024/func/sub-024_task-pain_run-08_bold.nii.gz"

declare -a masks=("amygdala")
declare -a hemisphere=("left" "right")

for mask in ${masks[@]};do
    for hem in ${hemisphere[@]};do

        mask_name="${hem}_${mask}ROI"

        ## make masks from atlas in temp_dir
        whereami -mask_atlas_region TT_Daemon:${hem}:${mask} -prefix ${mask_name}_temp
        
        # recenter ROI 
        echo "--RECENTER--"
        bash ${WD_dir}/masks_recenter.sh ${mask_name}_temp+tlrc

        # resample !!!! USING SUBJ 24 !!!!
        echo "--RESAMPLE--"
        3dfractionize -template ${sample_subj} -input ${mask_name}_temp+tlrc \
                      -clip 0.2 -preserve -prefix ${mask_name}

        # move to mask folder
        mv ${temp_dir}/${mask_name}+tlrc* ${masks_dir}

    done
done 

# remove temp_dir
cd ${WD_dir}
rm -rf ${temp_dir}



# join r and l
# 3dcalc -a ${mask_name}_rROI+tlrc -b ${mask_name}_lROI+tlrc \
#        -expr 'a+b' -prefix ${mask_name}ROI