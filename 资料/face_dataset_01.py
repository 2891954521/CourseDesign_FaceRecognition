import os
import cv2

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('D:\ProgramData\Anaconda3\envs\paddle\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

id = input('输入用户id:')

print("正在采集人脸，请直视摄像机")

count = 0

while count > 60:
    ret, img = cam.read()
    # img = cv2.flip(img, -1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        count += 1
        
    cv2.imshow('image', img)

count = 0

if not os.path.exists('G:\\face\\data' + str(id)):
    os.mkdir('G:\\face\\data' + str(id))


while True:
    ret, img = cam.read()
    # img = cv2.flip(img, -1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imwrite('G:\\face\\data' + str(id) + '\\' + str(id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        count += 1
        
        print(count)

    k = cv2.waitKey(100) & 0xff

    if k == 27:
        break
    elif count >= 30:
        break
        
    cv2.imshow('image', img)

print("采集完成！")

cam.release()

cv2.destroyAllWindows()