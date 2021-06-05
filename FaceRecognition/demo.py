import os
import cv2
import pyttsx3
import numpy as np
from PIL import Image

def inputFace():
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)

    config = os.path.join(os.path.dirname(os.path.abspath(__file__)),'haarcascade_frontalface_default.xml')
    if os.path.exists(config):
        face_detector = cv2.CascadeClassifier(config)
    else:
        print('模型文件不存在')
        return

    name = input('输入用户名称:')

    # engine.say("正在准备采集人脸，请直视摄像机")
    # engine.runAndWait()

    count = 0

    while count < 60:
        img = camera.read()[1]
        img = cv2.flip(img, 1)
        cv2.imshow('image', img)
        cv2.waitKey(50)
        count += 1

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'face')

    if not os.path.exists(path):
        os.mkdir(path)

    count = 0

    while count < 10:
        img = camera.read()[1]
        img = cv2.flip(img, 1)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

            cv2.imwrite(os.path.join(path,name + '.' + str(count) + ".jpg"), gray[y:y+h,x:x+w])

            count += 1
            
            print(count)
            
        cv2.imshow('image', img)

        cv2.waitKey(100)
    # engine.say("采集完成！")
    # engine.runAndWait()

    camera.release()

    cv2.destroyAllWindows()

def generateModule():

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    config = os.path.join(os.path.dirname(os.path.abspath(__file__)),'haarcascade_frontalface_default.xml')
    if os.path.exists(config):
        detector = cv2.CascadeClassifier(config)
    else:
        print('模型文件不存在')
        return

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'face')

    images = [os.path.join(path,f) for f in os.listdir(path)]

    face = []
    name = []
    for img in images:
        s = int(os.path.split(img)[-1].split(".")[0])
        img_numpy = np.array(Image.open(img).convert('L'),'uint8')
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            face.append(img_numpy[y:y+h,x:x+w])
            name.append(s)

    trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)),'trainer.yml')
    if os.path.exists(trainer):
        recognizer.read(trainer)
        recognizer.update(face, np.array(name))
    else:
        recognizer.train(face, np.array(name))

    # recognizer.save() worked on Mac, but not on Pi
    recognizer.write(trainer)

    [os.remove(f) for f in images]

    print("训练完成，添加了{}名用户，共计{}个有效数据".format(len(np.unique(name)),len(face)))


def detection():
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)),'trainer.yml')
    if os.path.exists(trainer):
        recognizer.read(trainer)
    else:
        print('模型文件不存在')
        return

    config = os.path.join(os.path.dirname(os.path.abspath(__file__)),'haarcascade_frontalface_default.xml')
    if os.path.exists(config):
        faceCascade = cv2.CascadeClassifier(config)
    else:
        print('模型文件不存在')
        return

    font = cv2.FONT_HERSHEY_SIMPLEX

    id = 0

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    # 能被检测到的最小人脸
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        img = cam.read()[1]

        img = cv2.flip(img, 1)

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x + w,y + h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            if (0 < confidence < 40):
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(id), (x + 5,y - 5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x + 5,y + h - 5), font, 1, (255,255,0), 1)

        cv2.imshow('camera',img)

        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    cam.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':

    engine = pyttsx3.init()

    while True:
        print(
            '1.采集人脸\n'
            '2.生成模型\n'
            '3.实时检测\n'
        )

        command = input('请输入命令:')

        if command == '1':
            inputFace()
        elif command == '2':
            generateModule()
        elif command == '3':
            detection()
    