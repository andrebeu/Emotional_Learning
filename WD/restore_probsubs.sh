
# DIR
if [[ $(pwd) == *"srm254"* ]]; then
    bids_dir="/home/fs01/srm254/visser_replicate/BIDSdataset"
fi
if [[ $(pwd) == *"andrebeukers"* ]];then
    bids_dir="/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate/BIDSdataset"
fi

probsub_dir=${bids_dir}/prob_subj
raw_dir=${bids_dir}/raw_data

mv ${probsub_dir}/* ${raw_dir}