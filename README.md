# Comment faire ?

## Installation de la lib insightswap modifiée

- Se placer dans le répertoire du projet et saisir la commande pip suivante pour installer la lib et ses dépendances :
```
	pip install ./python-package
```

## Image source

- Mettre à la racine du projet une image avec un visage source nommée **SOURCE_FACE.png**. L'image doit contenir un seul visage. Il s'agit du visage que nous souhaitons conserver et utiliser pour le FaceSwap.

## Swapper des images

- Mettre les images à swapper dans le dossier **images_to_swap**
- Exécuter **_start_images_swap.bat** ou bien saisir la commande suivante :
```
python images_swap.py
```
- Les images "swappées" sont générées dans le dossier **images_swapped**

## Swaper une vidéo

- Mettre la vidéo à swapper dans un fichier **video.mp4** à la racine du projet.

- Exécuter **_start_video_fullprocess.bat** ou bien saisir la commande suivante :
```
python video_full_process.py
``` 

La vidéo finale est générée dans un fichier **swapped_video.mp4**

### Méthode step-by-step

*Le mode step by step est utile en cas de "plantage", afin de pouvoir reprendre à l'épape où on en était.*

1. Spliter la vidéo en frames : **_start_video_frames_split.bat**
2. Lancer le FaceSwap sur chacune des frames : **_start_video_frames_swap.bat**
3. Reconstruire la vidéo finale : **_start_video_frames_merge.bat**
