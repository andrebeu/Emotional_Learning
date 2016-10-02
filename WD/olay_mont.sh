#!/usr/bin/env bash

path2_overlay=${1}

# PATHS
olay_dir=${path2_overlay%/*}
olay_fname=${path2_overlay##*/}

## folder for saving
if [ -d ${olay_dir} ];then
    output_dir=${olay_dir}/images
fi
if [ -s ${olay_dir} ];then
    output_dir=images
fi

# Where image is saved
mkdir -p ${output_dir}

afni -echo_edu \
     -com 'SWITCH_DIRECTORY A.All_Datasets' \
     -com 'OPEN_WINDOW A.sagittalimage mont=1x1:3' \
     -com 'OPEN_WINDOW A.axialimage mont=1x1:3' \
     -com 'OPEN_WINDOW A.coronalimage mont=1x1:3' \
     -com 'SWITCH_UNDERLAY A.MNI_caez_N27' \
     -com 'SWITCH_OVERLAY A.'${olay_fname} \
     -com 'SET_THRESHNEW A 0.05 *p' \
     -com 'SET_PBAR_NUMBER A.12' \
     -com 'SAVE_JPEG A.sagittalimage '${output_dir}/${olay_fname}_sagittal.jpg \
     -com 'SAVE_JPEG A.axialimage '${output_dir}/${olay_fname}_axial.jpg \
     -com 'SAVE_JPEG A.coronalimage '${output_dir}/${olay_fname}_coronal.jpg \
     ~/abin ${olay_dir}
     # -com 'CHDIR '${output_dir} \
     # -com 'SET_XHAIRS A.ON' \
     # -com 'QUIT' \



## NB ANIMAION FILE 

# SAVE_ALLJPEG [c].imagewindowname filename
# SAVE_ALLPNG  [c].imagewindowname filename
# SAVE_MPEG    [c].imagewindowname filename
# SAVE_AGIF    [c].imagewindowname filename
#   Save ALL the images in the given image sequence viewer (either as a
#   series of JPEG/PNG files, or as one animation file).  The windowname can
#   be one of 'axialimage', 'sagittalimage', or 'coronalimage'.  Do NOT
#   put a suffix like '.jpg' or '.mpg' on the filename -- it will be added.
#   ++ Unlike 'SAVE_JPEG', these commands do not work with graph windows.