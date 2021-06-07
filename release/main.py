import os

import FaceRecognition

import tkinter as tk

from playsound import playsound


def nop():
    pass


def inputFace():
    text.config(text='请面向摄像头开始采集人脸信息')
    playsound(sound2)
    discerner.inputFace(id.get(), inputFinish)


def inputFinish(text):
    text.config(text=text)
    playsound(sound3)
    root.update()


def detection():
    discerner.detection(success,nop)


def success(id):
    text.config(text = id + ' 签到成功！')
    playsound(sound1)
    root.update()


if __name__ == '__main__':

    sound1 = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sound','check _success.mp3')
    sound2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sound','start_enter.mp3')
    sound3 = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sound','enter_success.mp3')

    root = tk.Tk()

    root.geometry("1280x720+10+10")

    root.attributes("-fullscreen", False)

    root.update()

    width = root.winfo_width()
    heigh = root.winfo_height()

    tk.Label(root,text='考勤系统',font=('Arial', 15),fg="black").place(x=16,y=0,width=width,height=64)

    x = width // 3 * 2 + 16

    id = tk.Entry(root, font=('Arial', 14))

    wx = (width-x-16)//2
    id.place(x=x, y=150, width=wx, height=50)

    tk.Button(root,text='录入',command=inputFace).place(x=x+wx+16,y=150,width=width-x-wx-30,height=50)

    tk.Button(root,text='训练',command=nop).place(x=x,y=210,width=width-x-16,height=50)
    tk.Button(root,text='检测',command=detection).place(x=x,y=270,width=width-x-16,height=50)

    image_lab = tk.Label(root,bg="black")

    image_lab.place(x=16, y=72, width=x-32, height=int((x-32)/1.3))

    text = tk.Label(root,text='Welcome',font=('Arial', 15),fg="black")

    text.place(x=x, y=72, width=width-x, height=64)

    try:
        discerner = FaceRecognition.FaceRecognition(root)
    except Exception as e:
        text.config(text=e.__str__)

    root.mainloop()