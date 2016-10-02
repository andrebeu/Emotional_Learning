if [[ $(pwd) == *"srm254"* ]]; then
    main_dir="/home/fs01/srm254/visser_replicate"
fi
if [[ $(pwd) == *"andrebeukers"* ]];then
    main_dir="/Users/andrebeukers/Documents/fMRI/RVstudy/visser_replicate"
fi
if [[ $(pwd) == *"tmp"* ]]; then
    main_dir="/tmp/*.hd-hni.cac.cornell.edu"
fi

echo ${main_dir}