.PHONY : download-openvino-weights build-white-cane-openvino-env run-white-cane-openvino-env

download-openvino-weights:
	./bash/download_openvino_weights.sh
	
build-white-cane-openvino-env:
	./bash/build_white_cane_openvino_docker.sh

run-white-cane-openvino-env:
	./bash/run_white_cane_openvino_docker.sh
