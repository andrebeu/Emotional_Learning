#!/usr/bin/env bash

path2_roi=${1}

if [[ $(pwd) == *andrebeukers* ]]; then
    afni_dir="~/abin"
elif [[ $(pwd) == *srm254* ]]; then
    afni_dir="/opt/abin"
fi

# coordinates for centers of mass
read roi_x roi_y roi_z<<<$(3dCM ${path2_roi})
read mnia_x mnia_y mnia_z<<<$(3dCM ${afni_dir}/MNIa_caez_N27+tlrc)
read mni_x mni_y mni_z<<<$(3dCM ${afni_dir}/MNI_caez_N27+tlrc)

# difference between mnia and mni
delta_x=$(echo "${mnia_x}-(${mni_x})" | bc)
delta_y=$(echo "${mnia_y}-(${mni_y})" | bc)
delta_z=$(echo "${mnia_z}-(${mni_z})" | bc)

# new com
new_x=$(echo "${roi_x}-${delta_x}" | bc)
new_y=$(echo "${roi_y}-${delta_y}" | bc)
new_z=$(echo "${roi_z}-${delta_z}" | bc)

## recenter
3dCM -set ${new_x} ${new_y} ${new_z} ${path2_roi}

