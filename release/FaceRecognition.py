import os
import cv2
import System
import numpy as np

import tkinter as tk

from PIL import Image, ImageTk

class FaceRecognition:

    # 图片组件
    image = None

    # 当前状态 0为空闲
    status = 0

    # 相机
    camera = None

    system = None
    # 人脸检测
    faceCascade = None

    # 人脸分类
    recognizer = None

    # 最小临近
    minNeighbors = 3
    # 缩放尺寸
    scaleFactor = 1.2

    fps = 25

    font = cv2.FONT_HERSHEY_SIMPLEX

    # 初始化
    def __init__(self,system, root, x, y, w, h):

        self.system = system

        self.width = w
        self.heigh = h

        # self.width = 480
        # self.heigh = 320

        self.minW = int(0.2 * self.width)
        self.minH = int(0.2 * self.heigh)

        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, self.width)
        self.camera.set(4, self.heigh)

        # 加载人脸检测模型
        module = os.path.join(self.system.path, 'haarcascade_frontalface_default.xml')
        if os.path.exists(module):
            self.faceCascade = cv2.CascadeClassifier(module)
        else:
            raise Exception('模型文件不存在')

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        # 加载已有人脸数据
        trainer = os.path.join(self.system.path, 'trainer.yml')
        if os.path.exists(trainer):
            self.recognizer.read(trainer)

        self.fps = 1000 // self.fps

        self.image = tk.Label(root.page,bg="black")

        root.place_widget(self.image, x, y, w, h)

        self.image.after(1000,self.loop)

    # 获取人脸
    def __face__(self):

        image = cv2.flip(self.camera.read()[1], 1)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor = self.scaleFactor,
            minNeighbors = self.minNeighbors,
            minSize = (int(self.minW), int(self.minH))
        )

        return image, gray, faces
    

    # 录入人脸
    # id       str  录入人的ID
    # return   None 为录入成功,否则返还错误信息

    def inputFace(self, id):
        self.status = -1

        path = os.path.join(self.system.path, 'face', id)

        if os.path.exists(path):
            os.remove(path)

        os.makedirs(path)
        
        count = 20

        while count > 0:
            image = cv2.flip(self.camera.read()[1], 1)
            self.update(image)
            cv2.waitKey(self.fps)
            count -= 1

        time = 0

        face = []
        
        while count < 10:

            image, gray, faces = self.__face__()

            for (x, y, w, h) in faces:
                face.append(gray[y:y+h, x:x+w])
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                break

            self.update(image)
            cv2.waitKey(self.fps)

            time += 1

            if time > 200:
                self.clear()
                return '录入超时'

        time = 0
        ct = [0 for i in range(len(face))]

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(face, np.array([i for i in range(len(face))]))

        count = 20

        while count > 0:
            image, gray, faces = self.__face__()

            for(x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                c, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                if 0 < confidence < 50:
                    ct[c] += 1
                    count -= 1

            self.update(image)
            cv2.waitKey(self.fps)

            time += 1

            if time > 200:
                self.clear()
                return '录入超时'

        for i in range(len(face)-1,-1,-1):
            if ct[i] < 2:
                del face[i]

        for i in range(len(face)):
            cv2.imwrite(os.path.join(path, str(i) + ".jpg"), face[i])

        trainer = os.path.join(self.system.path,'trainer.yml')

        if os.path.exists(trainer):
            self.recognizer.update(face, np.array([int(id)] * len(face)))
        else:
            self.recognizer.train(face, np.array([int(id)] * len(face)))

        # recognizer.save() worked on Mac, but not on Pi
        self.recognizer.write(trainer)

        self.clear()

        return None


    # 实时检测人脸
    # return   str 检测到的人的id,超时返还None

    def detection(self):
        
        self.status = -1

        time = 0

        lastId = 0
        lastTime = 0

        while time < 200:

            image, gray, faces = self.__face__()

            for(x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                uid, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])

                if 0 < confidence < 50:
                    
                    if lastId == uid:
                        lastTime += 1
                        if lastTime > 2:
                            self.clear()
                            return str(uid)
                    else:
                        lastId = uid
                        lastTime = 0
                    
                    cv2.putText(image, str(uid), (x + 5, y - 5), self.font, 1, (255, 255, 255), 2)
                    # cv2.putText(image, "{}%".format(round(100 - confidence)), (x + 5, y + h - 5), self.font, 1, (255, 255, 0), 1)

                else:
                    cv2.putText(image, "unknown", (x + 5, y - 5), self.font, 1, (255, 255, 255), 2)

            self.update(image)

            cv2.waitKey(self.fps)

            time += 1

        self.clear()

        return None


    # 重新生成模型
    def createTrainer(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'face')

        for uid in os.listdir(path):
            
            face = []

            p = os.path.join(path, uid)

            for i in os.listdir(p):

                img_numpy = np.array(Image.open(os.path.join(p, i)).convert('L'), 'uint8')

                dim = img_numpy.shape

                faces = self.faceCascade.detectMultiScale(
                    img_numpy,
                    scaleFactor = self.scaleFactor - 0.1,
                    minNeighbors = self.minNeighbors,
                    minSize = (dim[1] // 2, dim[0] // 2)
                )

                if len(faces) != 0:
                    (x, y, w, h) = faces[0]
                    face.append(img_numpy[y:y+h, x:x+w])

            self.recognizer.update(face, np.array([int(uid)] * len(face)))

        # recognizer.save() worked on Mac, but not on Pi
        self.recognizer.write(os.path.join(os.path.dirname(os.path.abspath(__file__)),'trainer.yml'))

        self.clear()


    # 删除现有模型
    def deleteTrainer(self):
        trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer.yml')
        if os.path.exists(trainer):
            os.remove(trainer)
            return '已删除！'
        else:
            return '模型文件不存在，请先训练模型'


    # 刷新
    def update(self,img):
        img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)))
        self.image.config(image=img)
        self.image.image = img
        self.image.update()


    # 进入待机状态
    def clear(self):
        self.status = 1000
        self.image.after(100,self.loop)


    # 主循环
    def loop(self):
        if self.status > 0:
            self.update(cv2.flip(self.camera.read()[1], 1))
            self.image.after(self.fps,self.loop)
            self.status -= 1
        
        if self.status == 0:
            self.image.config(image=None)
            self.image.image = None
            self.image.update()
