#/usr/bin/python3
import argparse
import cv2
from white_cane_detector.openvino_inference import WhiteCaneDetector
import os


DOCUMENTS={
    "prog":"whitecane_inference_demo",
    "description":"load image file then detect whitecane."
}

def overwrap_detected_frame(img, bbox, score, class_name, rect_color=(255, 255, 0)):
    cv2.rectangle(img, (bbox["xmin"], bbox["ymin"]), (bbox["xmax"], bbox["ymax"]), rect_color, 2)
    cv2.putText(img, f"{class_name}: {score}", (bbox["xmin"], (bbox["ymin"]-5)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
    return img

def main(filename, output_filename):
    img = cv2.imread(filename)
    enable_flip=True
    if enable_flip:
        img = cv2.flip(img, 1)
    white_cane_detector = WhiteCaneDetector()
    result_jsons, _ = white_cane_detector._predict(img)
    out_flg=False
    for result_json in result_jsons:
        bbox = result_json["bbox"]
        score = result_json["score"]
        class_name = result_json["class"]
        print(class_name)
        if class_name is not None:
            out_flg=True
        overwrap_detected_frame(img, bbox, score, class_name)
    if out_flg:
        print("Detected#####################################")
        print(filename)
        cv2.imwrite(output_filename, img)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(**DOCUMENTS)
    parser.add_argument("-f", "--filename")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    main(args.filename, args.output)
