"""
file : openvino_inference.py

author : gw-shinohara
author : Yeyintthu
cdate : Tuesday October 3rd 2023
mdate : Tuesday October 6th 2023
copyright: 2023 GlobalWalkers.inc. All rights reserved.
"""

import logging as log
import sys
import numpy as np
from openvino.inference_engine import IECore

from white_cane_detector.utils.utils import (
    preproc,
    calc_time,
    postprocess,
    multiclass_nms,
    make_result_json,
)
from config.config import MODEL_PATH, SCORE_THRESH, DEVICE


class WhiteCaneDetector:
    def __init__(self) -> None:
        log.basicConfig(
            format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout
        )
        # --------------Step 1. Initialize inference engine core---------------
        log.info("Creating Inference Engine")
        self.ie = IECore()
        # -------------Step 2. Read a model in OpenVINO Intermediate Representation or ONNX format---------------
        log.info(f"Reading the network: {MODEL_PATH}")
        # (.xml and .bin files) or (.onnx file)
        self.net = self.ie.read_network(model=MODEL_PATH)

        if len(self.net.input_info) != 1:
            log.error("Sample supports only single input topologies")
        if len(self.net.outputs) != 1:
            log.error("Sample supports only single output topologies")

        # ----------Step 3. Configure input & output-------------
        log.info("Configuring input and output blobs")
        # Get names of input and output blobs
        self.input_blob = next(iter(self.net.input_info))
        self.out_blob = next(iter(self.net.outputs))

        # Set input and output precision manually
        self.net.input_info[self.input_blob].precision = "FP32"
        self.net.outputs[self.out_blob].precision = "FP16"

        # Get a number of classes recognized by a model
        self.num_of_classes = max(self.net.outputs[self.out_blob].shape)

        # --------Step 4. Loading model to the device------------
        log.info("Loading the model to the plugin")
        self.exec_net = self.ie.load_network(network=self.net, device_name=DEVICE)

    @calc_time
    def __run_openvino_inference(self, image):
        return self.exec_net.infer(inputs={self.input_blob: image})

    def _predict(self, ori_image):
        _, _, h, w = self.net.input_info[self.input_blob].input_data.shape
        image, ratio = preproc(ori_image, (h, w))
        # ------------Step 7. Do inference--------------
        log.info("Starting inference in synchronous mode")
        res = self.__run_openvino_inference(image)
        # ---------------------------Step 8. Process output--------------------------------------------------------------------
        res = res[self.out_blob]

        predictions = postprocess(res, (h, w))[0]
        boxes = predictions[:, :4]
        scores = predictions[:, 4, None] * predictions[:, 5:]
        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.0
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.0
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.0
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.0
        boxes_xyxy /= ratio
        dets = multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=SCORE_THRESH)

        final_boxes = []
        final_scores = []
        final_cls_inds =[]
        if dets is not None:
            final_boxes = dets[:, :4]
            final_scores, final_cls_inds = dets[:, 4], dets[:, 5]
        return make_result_json(final_boxes, final_scores, final_cls_inds), dets
