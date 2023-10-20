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


class WhiteCaneSocketListener:
    def __init__(self) -> None:
        self._white_cane_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_address = ("", PORT)
        self._white_cane_socket.bind(self.__socket_address)
        self._white_cane_socket.listen(5)
        print("White cane socket is now listening...")


def main():
    white_cane_detector = WhiteCaneDetector()
    white_cane_socket_listener = WhiteCaneSocketListener()
    while True:
        client_socket, addr = white_cane_socket_listener._white_cane_socket.accept()
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
            except:
                print("Connection dropped by client")

        client_socket.close()


if __name__ == "__main__":
    main()
