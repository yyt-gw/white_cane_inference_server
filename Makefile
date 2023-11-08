tag = v1
tag_dev = dev

.PHONY : download-openvino-weights build-white-cane-openvino-env run-white-cane-openvino-env run-white-cane-openvino-env-dev build-white-cane-openvino-env-dev

download-openvino-weights:
	./bash/download_openvino_weights.sh
	
build-white-cane-openvino-env: download-openvino-weights
	./bash/build_white_cane_openvino_docker.sh $(tag)

run-white-cane-openvino-env: build-white-cane-openvino-env
	./bash/run_white_cane_openvino_docker.sh $(tag)

build-white-cane-openvino-env-dev: download-openvino-weights
	./bash/build_white_cane_openvino_docker.sh $(tag_dev)

run-white-cane-openvino-env-dev: build-white-cane-openvino-env-dev
	./bash/run_white_cane_openvino_docker.sh $(tag_dev)