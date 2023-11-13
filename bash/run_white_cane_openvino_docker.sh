: '
 * file : run_white_cane_openvino_docker.sh
 * 
 * author : yeyintthu
 * cdate : Wednesday October 4th 2023
 * mdate : Wednesday October 4th 2023
 * copyright: 2023 GlobalWalkers.inc. All rights reserved.
'
. ./env/white_cane_openvino.env
docker run -it --rm --network host -v $(pwd):$WHITE_CANE_ROOT $WHITE_CANE_IMAGE:$WHITE_CANE_IMAGE_TAG