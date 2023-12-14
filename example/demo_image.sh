#/bin/bash
function loop() {
    in_dir=$1
    out_dir=$2
    mkdir $out_dir
    files=$(ls $in_dir |grep .jpg)
    for basename in $files[@]; do
        echo $basename
        filename=$in_dir/$basename
        output_filename=$out_dir/$basename
        case "$output_filename" in
        *\.jpg)
            flag=true
            ;;
        *\.png)
            flag=true
            ;;
        *)
            flag=false
            ;;
        esac
        if $flag; then
            python3 example_demo.py -f $filename -o $output_filename
        fi
    done    
}
in_dir="/white-cane-openvino-inference/data/tachikawa20231128"
out_dir="/white-cane-openvino-inference/data/tachikawa20231128_overlay1"
loop $in_dir $out_dir

# in_dir="/white-cane-openvino-inference/data/tachikawa20231123"
# out_dir="/white-cane-openvino-inference/data/tachikawa20231123_overlay1"
# loop $in_dir $out_dir
# 
# in_dir="/white-cane-openvino-inference/data/tachikawa20231124"
# out_dir="/white-cane-openvino-inference/data/tachikawa20231124_overlay1"
# loop $in_dir $out_dir
# 
# in_dir="/white-cane-openvino-inference/data/tachikawa20231122"
# out_dir="/white-cane-openvino-inference/data/tachikawa20231122_overlay1"
# loop $in_dir $out_dir