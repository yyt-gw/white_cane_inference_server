FROM openvino/ubuntu20_dev:latest

ARG DEBIAN_FRONTEND=noninteractive
ARG WHITE_CANE_DIR
ARG WHITE_CANE_PORT
ENV INFERENCE_SERVER_PORT=$WHITE_CANE_PORT
USER root
# update and install necessary tools
RUN pip3 install --upgrade pip

RUN mkdir $WHITE_CANE_DIR

COPY . $WHITE_CANE_DIR/
WORKDIR $WHITE_CANE_DIR/
RUN echo $INFERENCE_SERVER_PORT
RUN pip install -r requirements.txt

CMD ["sh", "-c", " uvicorn app:app --reload --port $INFERENCE_SERVER_PORT --host 0.0.0.0"]