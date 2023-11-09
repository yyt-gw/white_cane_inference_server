: '
 * file : run_white_cane_openvino_docker.sh
 * 
 * author : yeyintthu
 * cdate : Wednesday October 4th 2023
 * mdate : Wednesday October 4th 2023
 * copyright: 2023 GlobalWalkers.inc. All rights reserved.
'
TAG_ENV=$1
. ./env/white_cane_openvino.env
echo "Running server.."
docker run -it --rm --net=host -e WHITE_CANE_PORT=$WHITE_CANE_PORT -p 8081:8082 -v $(pwd):$WHITE_CANE_ROOT $WHITE_CANE_IMAGE:$TAG_ENV
