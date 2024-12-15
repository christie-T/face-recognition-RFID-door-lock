import face_recognition
import imutils
import pickle
import time
import cv2
import os


KNOWN_FACES_DIR = 'faces'

print('Loading known faces...')
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):

    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        print(f'Processing image of: {name}')
  
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')

        try:
            encoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            continue
        # Append encodings and name
        known_faces.append(encoding)
        known_names.append(name)



print("[INFO] serializing encodings...")
data =[known_faces, known_names]
f = open('face_encodings.pickle', "wb")
f.write(pickle.dumps(data))
f.close()


