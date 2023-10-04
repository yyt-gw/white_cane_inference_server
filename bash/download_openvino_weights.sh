: '
 * file : download_openvino_weights.sh
 * 
 * author : yyt
 * cdate : Wednesday October 4th 2023
 * mdate : Wednesday October 4th 2023
 * copyright: 2023 GlobalWalkers.inc. All rights reserved.
'
temp=./temp
link_id=1hE-t82ScDhfM-LllkfplwOggdQ0cSTs6
extracted_folder=white_cane_openvino
openvino_weights_zip=$extracted_folder.zip
weights_dest_dir=weights/openvino/best_ckpt
mkdir $temp

# download yolox weight
wget --load-cookies $temp/cookies.txt "https://docs.google.com/uc?export=download&confirm=\
    $(wget --quiet --save-cookies $temp/cookies.txt --keep-session-cookies --no-check-certificate \
    'https://docs.google.com/uc?export=download&id=FILEID' -O- | \
    sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$link_id" -O $openvino_weights_zip && rm -rf $temp

# unzip the zip file
unzip -q $openvino_weights_zip
# delete zip fileopenvino_weights.zip
rm -f $openvino_weights_zip

mv $extracted_folder/* $weights_dest_dir/
echo "Weights have been downloaded at $weights_dest_dir"
rm -rf $extracted_folder