#所需库
import tkinter as tk
from tkinter import *
import  tkinter.messagebox
from PIL import Image,ImageTk
import  pickle
import cv2
import os
import time

from win32 import win32api, win32gui, win32print
from win32.lib import win32con
from win32.win32api import GetSystemMetrics

import FaceRecognition
from playsound import playsound

'''预加载部分'''
#获取真实的分辨率
hdc = win32gui.GetDC(0)
# swidth = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)# 横向分辨率
# sheight = win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES)# 纵向分辨率
swidth = GetSystemMetrics (0)
sheight = GetSystemMetrics (1)
print(swidth,sheight)

    # mp = tk.Message(manage_page, text="I love Python!")
    # mp.pack()

#生成测试页
def create_test_page():
    test_page = tk.Tk()
    test_page.attributes("-fullscreen", True)#全屏模式

def show_success():
    tk.messagebox.showerror(message='成功！')

#锁定
def create_lock_page():
    print('芜湖!')




#考勤页
def create_check_page():
    #####################################################
    def nop():
        pass


    def inputFace():
        global flag
        flag = False
        text.config(text='请面向摄像头开始采集人脸信息')
        playsound(sound2)
        discerner.inputFace(id.get(), update, inputFinish)


    def inputFinish():
        clear()
        text.config(text='录入成功！')
        playsound(sound3)
        root.update()


    def generate():
        text.config(text=discerner.generateModule())
        root.update()


    def detection():
        global flag
        flag = False
        discerner.detection(update,success,nop)


    def success(id):
        clear()
        text.config(text = id + ' 签到成功！')
        playsound(sound1)
        root.update()


    def update(image):
        image_lab.config(image=image)
        image_lab.image = image
        root.update()


    def clear():
        # image_lab.config(image=None)
        # image_lab.image = None
        global flag
        flag = True
        root.after(20,loop)


    def loop():
        if flag:
            update(discerner.getImage())
            root.after(20,loop)


    if __name__ == '__main__':
            
        flag = True

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

        tk.Button(root,text='训练',command=generate).place(x=x,y=210,width=width-x-16,height=50)
        tk.Button(root,text='检测',command=detection).place(x=x,y=270,width=width-x-16,height=50)

        image_lab = tk.Label(root,bg="black")

        image_lab.place(x=16, y=72, width=x-32, height=int((x-32)/1.3))

        text = tk.Label(root,text='Welcome',font=('Arial', 15),fg="black")

        text.place(x=x, y=72, width=width-x, height=64)

        try:
            discerner = FaceRecognition.FaceRecognition()
        except Exception as e:
            text.config(text=e.__str__)
        else:
            root.after(20,loop)

        root.mainloop()
    #####################################################
    

    # def quit():
    #     check_page.destroy()

    # check_page=tk.Tk()
    # check_page.title("考勤页") # 设置窗口名称
    # check_page.attributes("-fullscreen", True) # 设置为全屏模式

    # tk.Label(check_page,text='考勤页',font=('',20),fg="green").place(x=0,y=0)
    # tk.Button(check_page,text='退出考勤',command=quit).place(x=125,y=0,width=75)#退出

    # check_page.mainloop()

#信息管理
def create_edit_page():

    def quit():
        edit_page.destroy()

    edit_page=tk.Tk() 
    edit_page.title("信息管理") # 设置窗口名称
    edit_page.attributes("-fullscreen", True) # 设置为全屏模式

    def search():
        tk.messagebox.showerror(message='搜索中！')

    search_name = tk.StringVar()#存放需要搜索的内容

    tk.Label(edit_page,text='信息管理',font=('',20),fg="green").place(x=0,y=0)
    tk.Button(edit_page,text='返回',command=quit).place(x=125,y=0,width=75)#退出
    
    tk.Entry(edit_page, textvariable=search_name).place(x=swidth/2, y=0)#搜索框
    tk.Button(edit_page,text='搜索',command=search).place(x=swidth*3/4,y=0)#搜索按钮

    edit_page.mainloop()

#信息查看
def create_view_page():
    
    def quit():
        view_page.destroy()

    view_page=tk.Tk()
    tk.Label(view_page,text='信息查看',font=('',20),fg="green").place(x=0,y=0)
    view_page.attributes("-fullscreen", True) # 设置为全屏模式

    tk.Button(view_page,text='返回',command=quit).place(x=125,y=0,width=75)#退出

    view_page.mainloop()

#排班页
def create_work_page():

    def quit():
        work_page.destroy()

    work_page=tk.Tk()
    work_page.title("排班页") # 设置窗口名称
    work_page.attributes("-fullscreen", True) # 设置为全屏模式
    
    tk.Label(work_page,text='排班页',font=('',20),fg="green").place(x=0,y=0)
    tk.Button(work_page,text='返回',command=quit).place(x=125,y=0,width=75)#退出

    work_page.mainloop()

#操作记录查看
def create_log_page():

    def quit():
        log_page.destroy()
        
    log_page=tk.Tk()

    tk.Label(log_page,text='操作记录查看',font=('',20),fg="green").place(x=0,y=0)
    log_page.attributes("-fullscreen", True) # 设置为全屏模式

    tk.Button(log_page,text='返回',command=quit).place(x=125,y=0,width=75)#退出

    log_page.mainloop()

#管理页
def create_manage_page():

    def logout():
        manage_page.destroy()

    manage_page = tk.Tk()
    manage_page.title("管理页")
    manage_page.attributes("-fullscreen", True)#全屏模式

    tk.Button(manage_page,text='锁定',command=create_lock_page).place(x=0,y=0,width=50)
    tk.Button(manage_page,text='考勤模式',command=create_check_page).place(x=50,y=0,width=75)
    tk.Button(manage_page,text='退出登录',command=logout).place(x=125,y=0,width=75)

    tk.Button(manage_page,text='信息编辑',command=create_edit_page).place(x=swidth*2/11,y=sheight*13/16)
    tk.Button(manage_page,text='信息查询',command=create_view_page).place(x=swidth*4/11,y=sheight*13/16)
    tk.Button(manage_page,text='排班',command=create_work_page).place(x=swidth*6/11,y=sheight*13/16)
    tk.Button(manage_page,text='操作记录查询',command=create_log_page).place(x=swidth*8/11,y=sheight*13/16)

    manage_page.mainloop()

#注册页
def create_signup_page():

    def quit():
        signup_page.destroy()

    signup_page=tk.Tk()# 创建一个主窗口
    signup_page.title("注册页") # 设置窗口名称
    signup_page.attributes("-fullscreen", True) # 设置为全屏模式

    new_name = tk.StringVar()#存放从输入框获取的新账户
    new_pwd = tk.StringVar()#存放从输入框获取的新账户的密码
    new_pwd2 = tk.StringVar()#存放从输入框获取的新账户的确认密码
    invitation_code = tk.StringVar()#存放从输入框获取的管理员邀请码

    tk.Button(signup_page,text='退出',command=quit).place(x=125,y=0,width=75)#退出
    tk.Label(signup_page,text='考勤管理系统\n管理员账户注册',font=('',54),fg="black").place(x=swidth/8,y=sheight*8/20)#考勤管理系统管理员账户注册
    tk.Label(signup_page,text='账户：',font=('',20),fg="green").place(x=swidth*8/16,y=sheight*30/100)#账户
    tk.Entry(signup_page, textvariable=new_name).place(x=swidth*10/16, y=sheight*30/100,width=swidth/5)#账户输入框
    tk.Label(signup_page,text='密码：',font=('',20),fg="green").place(x=swidth*8/16,y=sheight*40/100)#密码
    tk.Entry(signup_page, textvariable=new_pwd).place(x=swidth*10/16, y=sheight*40/100,width=swidth/5)#密码输入框
    tk.Label(signup_page,text='确认密码：',font=('',20),fg="green").place(x=swidth*8/16,y=sheight*50/100)#确认密码
    tk.Entry(signup_page, textvariable=new_pwd2).place(x=swidth*10/16, y=sheight*50/100,width=swidth/5)#确认密码输入框
    tk.Label(signup_page,text='邀请码：',font=('',20),fg="green").place(x=swidth*8/16,y=sheight*60/100)#管理员邀请码
    tk.Entry(signup_page, textvariable=invitation_code).place(x=swidth*10/16, y=sheight*60/100,width=swidth/5)#管理员邀请码输入框
    tk.Button(signup_page,text='注册',command=show_success).place(x=swidth*22/32,y=sheight*70/100)#注册

    signup_page.mainloop()

#登录页
def create_login_page():

    def exit():
        login_page.destroy()

    login_page=tk.Tk() # 创建一个主窗口
    login_page.title("登录页面") # 设置窗口名称
    login_page.attributes("-fullscreen", True) # 设置为全屏模式

    login_name = tk.StringVar()#存放从输入框获取的账户
    login_pwd = tk.StringVar()#存放从输入框获取的密码

    tk.Label(login_page,text='考勤管理系统',font=('',54),fg="black").place(x=swidth/8,y=sheight*9/20)#考勤管理系统
    tk.Label(login_page,text='账户：',font=('',20),fg="green").place(x=swidth*9/16,y=sheight*4/10)#账户
    tk.Entry(login_page, textvariable=login_name).place(x=swidth*10/16, y=sheight*4/10,width=swidth/5)#账户输入框
    tk.Label(login_page,text='密码：',font=('',20),fg="green").place(x=swidth*9/16,y=sheight*5/10)#密码
    tk.Entry(login_page, textvariable=login_pwd, show='*').place(x=swidth*10/16,y=sheight*5/10,width=swidth/5)#密码输入框
    tk.Button(login_page,text='退出',command=exit).place(x=125,y=0,width=75)#退出
    tk.Button(login_page,text='注册',command=create_signup_page).place(x=swidth*13/20,y=sheight*3/5)#注册
    tk.Button(login_page,text='登录',command=create_manage_page).place(x=swidth*3/4,y=sheight*3/5)#登录

    login_page.mainloop()
    
create_login_page()