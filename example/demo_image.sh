#/bin/bash

in_dir=/white-cane-openvino-inference/data/tachikawa_station_20231113_orgin
out_dir=/white-cane-openvino-inference/data/tmp_fliped
mkdir $out_dir
files=$(ls $in_dir |grep .jpg)
for basename in $files[@]; do
    echo $basename
    filename=$in_dir/$basename
    output_filename=$out_dir/$basename
    python3 example_demo.py -f $filename -o $output_filename
done
