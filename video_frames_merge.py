import cv2
import os

temp_frame_folder = 'video_frames'
swapped_frame_folder = 'video_frames_swapped'
output_video = 'swapped_video.mp4'

images = [img for img in sorted(os.listdir(swapped_frame_folder)) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(swapped_frame_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(swapped_frame_folder, image)))

video.release()

print("Done!")

import shutil
shutil.rmtree(temp_frame_folder)
shutil.rmtree(swapped_frame_folder)