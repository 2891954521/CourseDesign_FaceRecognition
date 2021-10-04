import os
import cv2
import numpy as np

from PIL import Image, ImageTk

class FaceRecognition:

    width = 640
    heigh = 480

    minW = int(0.2 * width)
    minH = int(0.2 * heigh)

    scaleFactor = 1.2

    minNeighbors = 3

    faceCascade =  None

    font = cv2.FONT_HERSHEY_SIMPLEX

    cameraUrl = 0


    # 初始化
    def __init__(self):
        module = os.path.join(os.path.dirname(os.path.abspath(__file__)),'haarcascade_frontalface_default.xml')
        if os.path.exists(module):
            self.faceCascade = cv2.CascadeClassifier(module)
        else:
            print('模型文件不存在')
            exit(0)


    # 获取人脸
    def __face__(self, camera) -> tuple:

        image = cv2.flip(camera.read()[1], 1)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor = self.scaleFactor,
            minNeighbors = self.minNeighbors,
            minSize = (int(self.minW), int(self.minH))
        )

        return image, gray, faces


    # 录入人脸
    # id       str  <- 录入人的ID
    # loop     img  -> 每捕获一帧调用一次，返还一个label图片
    # finish   None -> 录入结束时调用
    # return   None

    def inputFace(self, id:str, loop, finish):

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'face', id)

        if not os.path.exists(path):
            os.makedirs(path)

        camera = cv2.VideoCapture(self.cameraUrl)
        camera.set(3, self.width)
        camera.set(4, self.heigh)

        count = 30

        while count > 0:
            img = camera.read()[1]
            img = cv2.flip(img, 1)

            cv2.putText(img, 'count down:' + str(count), (100, 100), self.font, 2, (0, 0, 0), 5)

            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGBA))
            loop(ImageTk.PhotoImage(image))

            cv2.waitKey(20)
        
            count -= 1

        while count < 10:

            image, gray, faces= self.__face__(camera)

            for (x, y, w, h) in faces:
                cv2.imwrite(os.path.join(path, str(count) + ".jpg"), gray[y:y+h, x:x+w])

                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                break

            cv2.putText(image, 'record:' + str(count), (100, 100), self.font, 2, (0, 0, 0), 5)

            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGBA))
            loop(ImageTk.PhotoImage(image))

            cv2.waitKey(20)

        camera.release()
    
        finish()


    # 训练人脸模型
    # return   str -> 训练结果

    def generateModule(self):

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

                faces = self.faceCascade.detectMultiScale(
                    img_numpy,
                    scaleFactor = self.scaleFactor - 0.1,
                    minNeighbors = self.minNeighbors,
                    minSize = (dim[1] // 2, dim[0] // 2)
                )

                if len(faces) != 0:
                    (x, y, w, h) = faces[0]
                    face.append(img_numpy[y:y+h, x:x+w])
                    ids.append(int(id)) 
                    count += 1

            if count == 0:
                fail.append(id)

        recognizer.train(face, np.array(ids))

        trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer.yml')
        # recognizer.save() worked on Mac, but not on Pi
        recognizer.write(trainer)

        msg = '训练完成'

        if len(fail) > 0:
            msg += '\n下列用户模型训练错误，请尝试重新录入人脸\n'
            for id in fail:
                msg += id + '\n'
        
        return msg


    # 实时检测人脸
    # loop     img -> 每捕获一帧调用一次，返还一个label图片
    # success  str -> 检测到的人
    # return   None

    def detection(self, loop, success, stop):

        recognizer = cv2.face.LBPHFaceRecognizer_create()

        trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer.yml')
        if os.path.exists(trainer):
            recognizer.read(trainer)
        else:
            stop('模型文件不存在，请先训练模型')
            return

        camera = cv2.VideoCapture(self.cameraUrl)
        camera.set(3, self.width)
        camera.set(4, self.heigh)

        lastId = 0

        while True:
            image, gray, faces = self.__face__(camera)

            for(x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                if 0 < confidence < 45:
                    confidence = "{}%".format(round(100 - confidence))
                    if lastId != id:
                        lastId = id
                    else:
                        success(str(id))
                        camera.release()
                        return
                else:
                    id = "unknown"
                    confidence = "{}%".format(round(100 - confidence))

                cv2.putText(image, str(id), (x + 5, y - 5), self.font, 1, (255, 255, 255), 2)
                cv2.putText(image, str(confidence), (x + 5, y + h - 5), self.font, 1, (255, 255, 0), 1)

            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGBA))
            loop(ImageTk.PhotoImage(image))

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        camera.release()

        stop('终止')


    # 删除现有模型
    
    def deleteTrainer(self):
        trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer.yml')
        if os.path.exists(trainer):
            os.remove(trainer)
            return '已删除！'
        else:
            return '模型文件不存在，请先训练模型'
