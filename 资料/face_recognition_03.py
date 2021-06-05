import os
import cv2
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(r'G:\face\trainer\trainer.yml')
# recognizer.read(r'G:\face\trainer\trainer1.yml')

faceCascade = cv2.CascadeClassifier("D:\ProgramData\Anaconda3\envs\paddle\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

names = ['None', 'tanshengjang', 'Paula', 'Ilza', 'Z', 'W']

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    # img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
    )

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (0 < confidence < 40):
            # id = 'cpf'# id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)

    img = cv2.flip(img, 1)

    cv2.imshow('camera',img)

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()