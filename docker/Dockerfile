FROM openvino/ubuntu20_dev:latest

ARG DEBIAN_FRONTEND=noninteractive
ARG WHITE_CANE_DIR
USER root
# update and install necessary tools
RUN pip3 install --upgrade pip

RUN mkdir $WHITE_CANE_DIR

COPY . $WHITE_CANE_DIR/
WORKDIR $WHITE_CANE_DIR/

RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["app.py"]