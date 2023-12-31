"""
file : app.py

author : yyt
cdate : Tuesday October 3rd 2023
mdate : Tuesday October 3rd 2023
copyright: 2023 GlobalWalkers.inc. All rights reserved.
"""
from flask import Flask, request, Response, json
import numpy as np
import cv2
import os
from white_cane_detector.openvino_inference import WhiteCaneDetector
from config.config import PORT

# Initialize the Flask application
app = Flask(__name__)

white_cane_detector = WhiteCaneDetector()


# cropped_images_dir = '/home/jetson1/cropped_images_dir'
# route http posts to this method
@app.route("/api/send_image", methods=["POST"])
def detect_white_cane():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result_json = white_cane_detector._predict(img)
    # build a response dict to send back to client
    response = {
        "results": result_json,
    }

    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


white_cane_port = os.getenv("WHITE_CANE_PORT", PORT)
# start flask app
app.run(host="0.0.0.0", port=white_cane_port)
