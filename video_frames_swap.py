import datetime
import numpy as np
import os
import os.path as osp
import glob
import cv2
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image


bulk_folder = 'video_frames'
bulk_destination = 'video_frames_swapped'

os.makedirs(bulk_folder, exist_ok=True)
os.makedirs(bulk_destination, exist_ok=True)

if __name__ == '__main__':
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))
    model = insightface.model_zoo.get_model('model/inswapper_128.onnx', download=True, download_zip=True)

    source_image = cv2.imread('source_face.png')
    source_face = app.get(source_image)[0]
    
    images = [img for img in sorted(os.listdir(bulk_folder)) if img.endswith(".jpg") or img.endswith(".png") or img.endswith(".gif") or img.endswith(".webp")]
    
    i = 0
    for image in images:
        try:
            print("Processing image " + image)
            destination_image = cv2.imread(bulk_folder + '/' + image)
            destination_face = app.get(destination_image)[0]
            result_image = model.get(destination_image, destination_face, source_face, paste_back=True)
            cv2.imwrite(bulk_destination + '/' + image, result_image)
            i += 1
        except:
            print("Error with file " + image)
        

print("Done !")