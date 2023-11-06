"""
file : test.py

author : yyt
cdate : Tuesday October 3rd 2023
mdate : Tuesday October 3rd 2023
copyright: 2023 GlobalWalkers.inc. All rights reserved.
"""
import cv2
import json
import requests

ENDPOINT = "http://localhost:8081/api/send_image"
if __name__ == "__main__":
    #img = cv2.imread("/home/yyt/Downloads/cropped_images/white_cane_example.jpg")
    img = cv2.imread("/home/ubuntu/20231018/whitecane_3.png")
    im_encoded = cv2.imencode(".jpg", img)[1].tostring()
    for _ in range(9000):
        response = requests.post(
            ENDPOINT, data=im_encoded, headers={"content-type": "image/jpeg"}
        )
        #result_json = response.json()
        #print(json.dumps(result_json, indent=4))
        #print(response.status_code)
