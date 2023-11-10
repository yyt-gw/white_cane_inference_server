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
from post_request import PostRequest
import datetime
import uuid
from patrol_light import turnon_light, turnoff_light
import threading
import time

IPADRESS ="localhost"
JSON_URL = "http://" + IPADRESS + ":8080/api/v1/robot/event/json"
IMAGE_URL = "http://" + IPADRESS + ":8080/api/v1/robot/event/image"
PR = PostRequest(2, 20, 20)
tmp_time = datetime.datetime.now()
detected_time = datetime.datetime.now()
detected_flg = False
counter=0
KEEP_TURNON_TIME = 2
keep_turnon_count = KEEP_TURNON_TIME
exist_countdown = False


class_list = [
    "person",
    "knife",
    "white_stick",
    "umbrella",
    "petbottle",
    "phone",
    "stick",
    "maybe_knife",
    "maybe_white_stick",
    "maybe_umbrella",
    "maybe_petbottle",
    "maybe_phone",
    "maybe_stick",
]

def init_dict():
    date_time = datetime.datetime.now()
    json_dict = dict(
        [
            ("date", date_time.strftime("%Y%m%d")),
            # ("time", date_time.strftime("%H:%M:%S.%f")),
            ("time", date_time.strftime("%H:%M:%S.") + str(date_time.microsecond)[:3]),
            # ("time", date_time.isoformat(timespec="milliseconds")),
            ("fileName", "tmp.jpg"),
            ("object", []),
        ]
    )
    return json_dict

def post(boxes, img, frame_id, time_info):
    
    json_dict = init_dict()
    now_time = datetime.datetime.now()
    global tmp_time
    global detected_flg
    global detected_time
    global counter
    #if (now_time - tmp_time).seconds < 10:   
        #return
    #tmp_time = now_time

    #img_info = cv2.imencode('.jpg', img)[1].tostring()
    #PR.request_image(IMAGE_URL, "test", img_info)
    if boxes is not None:
        for i in range(len(boxes)):
            box = boxes[i]
            if box[4] == 0.0:
                continue
            if int(box[5]) != 2 and int(box[5]) != 8:
                continue
            # cls_id = int(cls_ids[i])
            # score = scores[i]
            # if score < conf:
            #     continue
            x0 = int(box[0])
            y0 = int(box[1])
            x1 = int(box[2])
            y1 = int(box[3])
            # print("x0:",x0)

            # if type(score) == torch.Tensor:
            #     score = score.item()

            object_dict = dict(
                [
                    # ("class", "white_stick"),
                    # ("x", x0),
                    # ("y", y0),
                    # ("width", x1),
                    # ("height", y1),
                    # ("confidence", round(score, 5)),
                    ("class", class_list[int(box[5])]),
                    ("x", 0),
                    ("y", 0),
                    ("width", 0),
                    ("height", 0),
                    ("confidence", round(0, 5)),
                ]
            )
            json_dict["object"].append(object_dict)
    if len(json_dict["object"]) != 0:
        # print(json_dict)
        # FrameIDID毎に一意なリクエストIDを生成する
        req_id = str(uuid.uuid4())

        #print(
        #    "JSONのPOSTリクエストを開始しました.... URL: ",
        #    JSON_URL
        #)
        # print("POST JSON URL:", JSON_URL)
        
        # image_path = 'tmp.jpg'
        # cv2.imwrite("tmp.jpg", img)
        img_info = cv2.imencode('.jpg', img)[1].tostring()
        post_time = datetime.datetime.now()
        json_dict.update([('frame_id', frame_id)])
        json_dict.update([('CaptureTime', time_info[0].strftime("%H:%M:%S.") + str(time_info[0].microsecond)[:3])])
        #json_dict.update([('PreEndTime', time_info[1].strftime("%H:%M:%S.") + str(time_info[1].microsecond)[:3])])
        json_dict.update([('InferEndTime', time_info[1].strftime("%H:%M:%S.") + str(time_info[1].microsecond)[:3])])
        json_dict.update([('PostTime', post_time.strftime("%H:%M:%S.") + str(post_time.microsecond)[:3])])
        # print(json_dict)


# Initialize the Flask application
app = Flask(__name__)

white_cane_detector = WhiteCaneDetector()

def countdown_turnoff_light():
    global keep_turnon_count
    global exist_countdown
    exist_countdown = True
    while 0 < keep_turnon_count:
        time.sleep(1)
        keep_turnon_count -= 1
        print(f"Exist countdown thread:{exist_countdown}")
    turnoff_light()
    exist_countdown = False
def update_countdown_timer():
    global keep_turnon_count
    while()
def reset_keep_turnon_count():
    global keep_turnon_count
    keep_turnon_count = KEEP_TURNON_TIME

# cropped_images_dir = '/home/jetson1/cropped_images_dir'
# route http posts to this method
@app.route("/api/send_image", methods=["POST"])
def detect_white_cane():
    global counter
    global exist_countdown
    r = request
    countdown_thread = threading.Thread(target=countdown_turnoff_light)

    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    cap_time = datetime.datetime.now()
    # print("cap_time", counter, cap_time)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # print("GET IMAGE")

    result_jsons, boxes = white_cane_detector._predict(img)
    # print(result_jsons)

    # build a response dict to send back to client
    response = {
        "results": result_jsons,
    }

    # print(result_jsons)
    if result_jsons !=[]:
        
        for idx, result_json in enumerate(result_jsons):
            print(result_json['class'])
            if result_json['class']=='white_cane':
                reset_keep_turnon_count()
                if not exist_countdown:
                    turnon_light()
                    countdown_thread.start() # alive light keep_turnon_count
                # cv2.imwrite(f"/white-cane-openvino-inference/data/{cap_time}_{idx}.jpg", img)
    print(f"exist countdown: {exist_countdown}")
    infer_time = datetime.datetime.now()
    # post(boxes, img, 0, [cap_time, infer_time])
    # print("diff",counter, datetime.datetime.now() - cap_time)
    counter=counter+1

    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


white_cane_port = os.getenv("WHITE_CANE_PORT", PORT)
# start flask app
# print(f"[info] Send data to IP:{IPADRESS}")
app.run(host="0.0.0.0", port=white_cane_port)
