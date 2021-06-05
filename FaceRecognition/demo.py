import os
import cv2
import pyttsx3
import numpy as np

import tkinter as tk
from PIL import Image, ImageTk

from PIL import Image, ImageDraw, ImageFont


width = 640
heigh = 480

scaleFactor = 1.2

minNeighbors = 3

minW = int(0.2 * width)
minH = int(0.2 * heigh)

module = os.path.join(os.path.dirname(os.path.abspath(__file__)),'haarcascade_frontalface_default.xml')
if os.path.exists(module):
    faceCascade = cv2.CascadeClassifier(module)
else:
    print('模型文件不存在')
    exit(0)

font = cv2.FONT_HERSHEY_SIMPLEX

cameraUrl = 0 # 'https://192.168.5.196:4343/video'


def inputFace():
    camera = cv2.VideoCapture(cameraUrl)
    camera.set(3, width)
    camera.set(4, heigh)

    id = input('输入用户id:')

    count = 60

    while count > 0:
        img = camera.read()[1]
        img = cv2.flip(img, 1)
        cv2.putText(img, 'count down:' + str(count), (100, 100), font, 2, (0, 0, 0), 5)
        cv2.imshow('image', img)
        cv2.waitKey(20)
        count -= 1

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'face')

    path = os.path.join(path, id)

    if not os.path.exists(path):
        os.mkdir(path)

    while count < 10:
        img = camera.read()[1]
        img = cv2.flip(img, 1)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = scaleFactor,
            minNeighbors = minNeighbors,
            minSize = (int(minW), int(minH))
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite(os.path.join(path, str(count) + ".jpg"), gray[y:y+h, x:x+w])
            cv2.putText(img, 'save:' + str(count), (100, 100), font, 2, (0, 0, 0), 5)
            count += 1
            break

        cv2.imshow('image', img)
        cv2.waitKey(20)

    camera.release()

    cv2.destroyAllWindows()


def generateModule():

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'face')

    fail = []

    face = []

    ids = []

    for id in os.listdir(path):

        file = os.path.join(path, id)

        count = 0

        for image in os.listdir(file):

            img_numpy = np.array(Image.open(os.path.join(file, image)).convert('L'), 'uint8')

            dim = img_numpy.shape

            faces = faceCascade.detectMultiScale(
                img_numpy,
                scaleFactor = scaleFactor - 0.1,
                minNeighbors = minNeighbors,
                minSize = (dim[1] // 2, dim[0] // 2)
            )

            if len(faces) != 0:
                (x, y, w, h) = faces[0]
                cv2.rectangle(img_numpy, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imshow('image', img_numpy)
                cv2.waitKey(0)
                count += 1
                face.append(img_numpy[y:y+h, x:x+w])
                ids.append(int(id))

        if count == 0:
            fail.append(id)

    recognizer.train(face, np.array(ids))

    trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer.yml')
    # recognizer.save() worked on Mac, but not on Pi
    recognizer.write(trainer)

    cv2.destroyAllWindows()
    # if os.path.exists(trainer):
    #     recognizer.read(trainer)
    #     recognizer.update(face, np.array(name))
    # else:
    #     recognizer.train(face, np.array(name))
    print('训练完成')
    if len(fail) > 0:
        print('下列用户模型训练错误，请尝试重新录入人脸')
        for id in fail:
            print(id)

    # yes = input('是否删除训练数据？(y/n)')
    # if yes == '' or yes == 'y':
    #     [os.remove(f) for f in images]


def detection(loop,success,fail):

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer.yml')
    if os.path.exists(trainer):
        recognizer.read(trainer)
    else:
        print('模型文件不存在，请先训练模型')
        return

    cam = cv2.VideoCapture(cameraUrl)
    cam.set(3, width)
    cam.set(4, heigh)

    lastId = 0

    while True:
        img = cam.read()[1]

        img = cv2.flip(img, 1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = scaleFactor,
            minNeighbors = minNeighbors,
            minSize = (int(minW), int(minH)),
        )

        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            if 0 < confidence < 45:
                confidence = "{0}%".format(round(100 - confidence))
                if lastId != id:
                    lastId = id
                else:
                    success(str(id))
                    return
            else:
                id = "unknown"
                confidence = "{0}%".format(round(100 - confidence))

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGBA))

        loop(ImageTk.PhotoImage(image))

        # lab.config(image = image)
        # lab.image = image
        # root.update()

        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    cam.release()

    fail()


def deleteTrainer():
    trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer.yml')
    if os.path.exists(trainer):
        os.remove(trainer)
        print('已删除！')
    else:
        print('模型文件不存在，请先训练模型')


# if __name__ == '__main__':


#     while True:
#         print(
#             '\n1.采集人脸\n'
#             '2.生成模型\n'
#             '3.实时检测\n'
#             '4.清空已录入的人脸数据\n'
#         )

#         command = input('请输入命令:')

#         if command == '1':
#             inputFace()
#         elif command == '2':
#             generateModule()

#         elif command == '3':

#             root.after(1000,detection)

#             root.mainloop()

#         elif command == '4':
#             deleteTrainer()
