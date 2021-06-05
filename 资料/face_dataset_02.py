import os
import cv2
import numpy as np
from PIL import Image

id = '2'

path = r'G:\face\data' + id

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("D:\ProgramData\Anaconda3\envs\paddle\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")

# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        id = int(os.path.split(imagePath)[-1].split(".")[0])
        img_numpy = np.array(Image.open(imagePath).convert('L'),'uint8')
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)

if os.path.exists(r'G:\face\trainer\trainer.yml'):
    recognizer.read(r'G:\face\trainer\trainer.yml')
    recognizer.update(faces, np.array(ids))
else:
    recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write(r'G:\face\trainer\trainer.yml') # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))