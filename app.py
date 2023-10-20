"""
file : app.py

author : yyt
cdate : Tuesday October 3rd 2023
mdate : Tuesday October 3rd 2023
copyright: 2023 GlobalWalkers.inc. All rights reserved.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import numpy as np
import cv2
import os
from white_cane_detector.openvino_inference import WhiteCaneDetector
import uvicorn
from config.config import PORT, RELOAD
from time import time

# Initialize the Flask application
app = FastAPI()

white_cane_detector = WhiteCaneDetector()


# cropped_images_dir = '/home/jetson1/cropped_images_dir'
# route http posts to this method
@app.websocket("/ws/detect_objects")
async def detect_white_cane(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            start_t = time()
            img_contents = await websocket.receive_bytes()
            # convert string of image data to uint8
            nparr = np.frombuffer(img_contents, np.uint8)
            # decode image
            img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

            result_json = white_cane_detector._predict(img)
            # build a response dict to send back to client
            response = {
                "results": result_json,
            }
            await websocket.send_json(response)
            print(f"Time taken : {round((time()-start_t)*1000, 2)} ms")
    except WebSocketDisconnect:
        print("Client disconnected")


if __name__ == "__main__":
    white_cane_port = int(os.getenv("WHITE_CANE_PORT", PORT))
    reload_flag = os.getenv("SERVER_ENV") == "dev"
    # start uvicorn server
    uvicorn.run("app:app", host="0.0.0.0", port=white_cane_port, reload=reload_flag)
