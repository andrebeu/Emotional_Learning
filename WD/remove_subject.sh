subno=$1

# DIR
if [[ $(pwd) == *"srm254"* ]]; then
    bids_dir="/home/fs01/srm254/visser_replicate/BIDSdataset"
fi
if [[ $(pwd) == *"andrebeukers"* ]];then
    bids_dir="/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset"
fi

if [ ${#subno} = 1 ]; then
    sid="sub-00${subno}"
fi
if [ ${#subno} = 2 ]; then
    sid="sub-0${subno}"
fi
if [ ${#subno} = 3 ]; then
    sid="sub-${subno}"
fi
echo ${sid}

prob_subj_folder="${bids_dir}/prob_subj"
raw_data_subj_folder="${bids_dir}/raw_data/${sid}"

mv ${raw_data_subj_folder} ${prob_subj_folder}


