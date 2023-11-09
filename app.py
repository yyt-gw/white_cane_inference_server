"""
file : app.py

author : yyt
cdate : Tuesday October 3rd 2023
mdate : Tuesday October 3rd 2023
copyright: 2023 GlobalWalkers.inc. All rights reserved.
"""
import socket
import pickle
import struct
import json
from white_cane_detector.openvino_inference import WhiteCaneDetector
from config.config import PORT
from post_request import PostRequest
import patlite
import datetime
import uuid
import threading

IPADRESS ="localhost"
JSON_URL = "http://" + IPADRESS + ":8080/api/v1/robot/event/json"
IMAGE_URL = "http://" + IPADRESS + ":8080/api/v1/robot/event/image"
PR = PostRequest(2, 20, 20)
tmp_time = datetime.datetime.now()
detected_time = datetime.datetime.now()
detected_flg = False
counter=0

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
    print("count:", counter)
    counter=counter+1
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
            print("x0:",x0)

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
        print(json_dict)
        # FrameIDID毎に一意なリクエストIDを生成する
        req_id = str(uuid.uuid4())

        #print(
        #    "JSONのPOSTリクエストを開始しました.... URL: ",
        #    JSON_URL
        #)
        print("POST JSON URL:", JSON_URL)
        
        # image_path = 'tmp.jpg'
        # cv2.imwrite("tmp.jpg", img)
        img_info = cv2.imencode('.jpg', img)[1].tostring()
        post_time = datetime.datetime.now()
        json_dict.update([('frame_id', frame_id)])
        json_dict.update([('CaptureTime', time_info[0].strftime("%H:%M:%S.") + str(time_info[0].microsecond)[:3])])
        #json_dict.update([('PreEndTime', time_info[1].strftime("%H:%M:%S.") + str(time_info[1].microsecond)[:3])])
        json_dict.update([('InferEndTime', time_info[1].strftime("%H:%M:%S.") + str(time_info[1].microsecond)[:3])])
        json_dict.update([('PostTime', post_time.strftime("%H:%M:%S.") + str(post_time.microsecond)[:3])])
        print(json_dict)

class WhiteCaneSocketListener:
    def __init__(self) -> None:
        self._white_cane_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._white_cane_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_address = ("", PORT)
        self._white_cane_socket.bind(socket_address)
        self._white_cane_socket.listen(5)

        # patlite
        print("do patlite")

        # def run_patlite():
        #     # patlite
        #     __detected_flg = True
        #     __patlite = patlite.Patlite.get_instance()
        #     __patlite.set_dest(IPADRESS, 10001)
        #     __patlite.set_status("red", __patlite.ON)
        #     __patlite.set_status("yellow", __patlite.BLINK1)
        #     __patlite.set_status("green", __patlite.BLINK2)
        #     __patlite.set_status("buzzer", __patlite.ON)
        #     __patlite.commit()
        # self.__run_patlite_thread = threading.Thread(target=run_patlite)
        print(f"White cane socket is now listening {PORT}...")

def main():
    white_cane_detector = WhiteCaneDetector()
    white_cane_socket_listener = WhiteCaneSocketListener()
    while True:
        client_socket, addr = white_cane_socket_listener._white_cane_socket.accept() # Need change multi threding
        print(f"Received connection from {addr}")
        if client_socket:
            try:
                # used in handling binary data from network connections
                data = b""
                # Q: unsigned long long integer(8 bytes)
                payload_size = struct.calcsize("Q")
                while True:
                    while len(data) < payload_size:
                        packet = client_socket.recv(4 * 1024)
                        if not packet:
                            break
                        data += packet
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("Q", packed_msg_size)[0]
                    while len(data) < msg_size:
                        data += client_socket.recv(4 * 1024)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)
                    result_json = white_cane_detector._predict(frame)
                    # build a response dict to send back to client
                    response = json.dumps({"results": result_json})
                    print(response)
                    client_socket.sendall(bytes(response, encoding="utf-8"))

                    if 1:#detected_flg == False:
                        print("Do patlite bright")
                        # self.__run_patlite_thread.start()
                
                    #if (now_time - tmp_time).seconds < 10:        
                    #    return
                    #tmp_time=now_time

            except Exception as e:
                print(f"{e}")
        client_socket.close()


if __name__ == "__main__":
    main()
