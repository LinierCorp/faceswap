import cv2
import os
import insightface
import numpy as np

# Chemins des fichiers
video_path = 'video.mp4'
temp_frame_folder = 'video_frames'

# Création des répertoires temporaires pour les frames
os.makedirs(temp_frame_folder, exist_ok=True)

# Étape 1 : Extraction des frames de la vidéo
cap = cv2.VideoCapture(video_path)
frame_count = 0
frames = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
    cv2.imwrite(f'{temp_frame_folder}/frame_{frame_count:04d}.jpg', frame)
    frame_count += 1

cap.release()

print("Done!")