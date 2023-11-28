#/usr/bin/python3
import argparse
import cv2
from white_cane_detector.openvino_inference import WhiteCaneDetector
import os
import json

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
    result_jsons = white_cane_detector._predict(img)
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
        basename=os.path.basename(filename)
        image_js={
            "license": 4,
            "file_name": basename,
            "coco_url": filename,
            "height": img.shape[0],
            "width": img.shape[1],
            "date_captured": "",
            "id": basename
        }
        annotations_js=[]
        for idx, result_json in enumerate(result_jsons):
            bbox = result_json["bbox"]
            score = result_json["score"]
            class_name = result_json["class"]
            bbox_w=bbox["xmax"]-bbox["xmin"]
            bbox_h=bbox["ymax"]-bbox["ymin"]
            area=bbox_w*bbox_h
            annotation_js={
                "area": area,
                "iscrowd": 0,
                "image_id": idx,
                "bbox": [bbox["xmin"], bbox["ymin"], bbox_w, bbox_h],
                "category_id": result_json["class"],
                "score": result_json["score"],
                "id": basename
            }
            annotations_js.append(annotation_js)
        coco_form={
            "images":[image_js],
            "annotations":[ano for ano in annotations_js]
        }
        out_dir=os.path.dirname(output_filename)
        out_path_js=os.path.join(out_dir, "inference_result.js")
        if os.path.exists(out_path_js):
            with open(out_path_js) as f:
                load_js = json.load(f)
                [load_js["images"].append(im) for im in coco_form["images"]]
                [load_js["annotations"].append(ano) for ano in coco_form["annotations"]]
                coco_form=load_js
        with open(out_path_js, 'w') as f:
            json.dump(coco_form, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(**DOCUMENTS)
    parser.add_argument("-f", "--filename")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    main(args.filename, args.output)
