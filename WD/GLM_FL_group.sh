#!/usr/bin/env bash

GLMoutput_dir=$1
# GLMoutput_dir=/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset/deriv_data/GLMcbc-output_TASK-funcloc

# PATHS and folders
main_dir=${GLMoutput_dir%visser_replicate*}/visser_replicate
bids_dir=${main_dir}/BIDSdataset
wd_dir=${main_dir}/WD_visser_replicate

# group GLM folder
path2_groupGLM_folder="${bids_dir}/deriv_data/GLMgroup_TASK-funcloc"
mkdir -p ${path2_groupGLM_folder}

# subject beta volumes (input for ttest)
all_betavolumes="${GLMoutput_dir}/sub-???/sub-???_TASK-funcloc_GLMoutput-AFNIbucket+tlrc.HEAD"


echo
echo "RUNNING GROUP T-TEST"
echo

# ttest
cd ${path2_groupGLM_folder}
3dttest++ -paired -AminusB -toz -no1sam \
          -labelA "face"    \
          -setA "${all_betavolumes}[face#0_Coef]" \
          -labelB "house"   \
          -setB "${all_betavolumes}[house#0_Coef]" \
          -prefix "GLMgroup-bucket_TASK-funcloc"   \

3dinfo ${all_betavolumes}

echo
echo "GENERATING FIGURES OFF"
echo

# figures
# cd ${wd_dir}
path2_overlay="${path2_groupGLM_folder}/GLMgroup-bucket_TASK-funcloc"
olay_mont.sh ${path2_overlay} 
