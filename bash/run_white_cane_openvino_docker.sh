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
if [ $TAG_ENV = "dev" ]; then
    echo "Running dev server.."
    docker run -it --rm -e WHITE_CANE_PORT=$WHITE_CANE_PORT -p $WHITE_CANE_PORT:$WHITE_CANE_PORT -v $(pwd):$WHITE_CANE_ROOT $WHITE_CANE_IMAGE:$TAG_ENV
else
    echo "Running live server.."
    docker run -it --rm -e WHITE_CANE_PORT=$WHITE_CANE_PORT -p $WHITE_CANE_PORT:$WHITE_CANE_PORT $WHITE_CANE_IMAGE:$TAG_ENV
fi