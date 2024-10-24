import cv2
import os
import insightface
import numpy as np
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

# Chemins des fichiers
video_path = 'video.mp4'
source_face_path = 'SOURCE_FACE.png'
output_video_path = 'output_video.mp4'
temp_frame_folder = 'video_frames'
swapped_frame_folder = 'video_frames_swapped'
n_frames_skip = 0  # Nombre de frames à skipper pour interpolation

# Chargement du modèle de FaceSwap
model = insightface.model_zoo.get_model('model/inswapper_128.onnx')
#model.prepare(ctx_id=0)  # Utilise le GPU si disponible

# Création des répertoires temporaires pour les frames
os.makedirs(temp_frame_folder, exist_ok=True)
os.makedirs(swapped_frame_folder, exist_ok=True)

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

# Étape 2 : Application du FaceSwap sur certaines frames clés
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))

# Lire le visage source et la frame cible
source_image = cv2.imread(source_face_path)
source_face = app.get(source_image)[0]
    
for i in range(0, len(frames)):
    target_frame_path = f'{temp_frame_folder}/frame_{i:04d}.jpg'
    destination_image = cv2.imread(target_frame_path)
    destination_face = app.get(destination_image)[0]
    
    # Application du FaceSwap
    swapped_frame = model.get(destination_image, destination_face, source_face, paste_back=True)
    
    # Sauvegarder l'image modifiée
    swapped_frame_path = f'{swapped_frame_folder}/frame_{i:04d}.jpg'
    cv2.imwrite(swapped_frame_path, swapped_frame)

# Étape 3 : Interpolation des frames intermédiaires
'''
def interpolate_frames(frame1, frame2, alpha):
    """ Interpole deux images frame1 et frame2 avec un facteur alpha """
    return cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)

for i in range(0, len(frames) - n_frames_skip, n_frames_skip):
    # Lire les frames modifiées
    frame1_path = f'{swapped_frame_folder}/frame_{i:04d}.jpg'
    frame2_path = f'{swapped_frame_folder}/frame_{i + n_frames_skip:04d}.jpg'
    
    frame1 = cv2.imread(frame1_path)
    frame2 = cv2.imread(frame2_path)
    
    # Interpoler les frames intermédiaires
    for j in range(1, n_frames_skip):
        alpha = j / n_frames_skip
        interpolated_frame = interpolate_frames(frame1, frame2, alpha)
        interpolated_frame_path = f'{swapped_frame_folder}/frame_{i + j:04d}.jpg'
        cv2.imwrite(interpolated_frame_path, interpolated_frame)
'''

# Étape 4 : Recombiner les frames en vidéo
height, width, layers = frames[0].shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, 30, (width, height))

for i in range(len(frames)):
    frame_path = f'{swapped_frame_folder}/frame_{i:04d}.jpg'
    if os.path.exists(frame_path):
        frame = cv2.imread(frame_path)
    else:
        # Si pas d'image swappée, utiliser la frame d'origine
        frame = cv2.imread(f'{temp_frame_folder}/frame_{i:04d}.jpg')
    
    out.write(frame)

out.release()

# Nettoyage des fichiers temporaires (optionnel)
import shutil
shutil.rmtree(temp_frame_folder)
shutil.rmtree(swapped_frame_folder)

print("FaceSwap terminé et vidéo générée.")
