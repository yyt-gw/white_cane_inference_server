: '
 * file : build_white_cane_openvino_docker.sh
 * 
 * author : yeyintthu
 * cdate : Wednesday October 4th 2023
 * mdate : Wednesday October 4th 2023
 * copyright: 2023 GlobalWalkers.inc. All rights reserved.
'
TAG_ENV=$1
. ./env/white_cane_openvino.env
if [ "$TAG_ENV" = "dev" ]; then
    docker_file="Dockerfile.dev"
else
    docker_file="Dockerfile"
fi
docker build --build-arg WHITE_CANE_DIR=$WHITE_CANE_ROOT -t $WHITE_CANE_IMAGE:$TAG_ENV -f docker/$docker_file .