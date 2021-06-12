import os
import time
import tkinter as tk

import FaceRecognition

from win32 import win32gui
from playsound import playsound
from win32.win32api import GetSystemMetrics


# 获取真实的分辨率
hdc = win32gui.GetDC(0)
swidth = GetSystemMetrics(0)
sheight = GetSystemMetrics(1)


def create_check_page():

    check_page = tk.Toplevel()
    check_page.title("考勤窗口")
    check_page.attributes("-fullscreen", True)

    def success(id):
        text_notice.config(text = id + ' 签到成功！')
        playsound(sound_success, False)
        check_page.update()

    def check():
        discerner.detection(success)

    def update_time():
        text_time.config(text=time.strftime('%Y-%m-%d\n%H:%M:%S',time.localtime(time.time())))
        text_time.after(1000, update_time)  
    
    sound_success = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sound','check _success.mp3')

    tk.Label(check_page, text='考勤系统', font=('Arial', 20), fg="black").place(x=16, y=0, width=swidth, height=sheight/8)

    tk.Button(check_page, text='检测', command=check).place(x=swidth*17/32, y=sheight*3/4, width=swidth*14/32, height=sheight/8)

    text_notice = tk.Label(check_page, text='Welcome', font=('Arial', 40), fg="black")
    text_time = tk.Label(check_page, text='', font=('Arial', 70), fg="black")

    text_notice.place(x=swidth*17/32, y=sheight/8, width=swidth*14/32, height=sheight/8)
    text_time.place(x=swidth*17/32, y=sheight/4, width=swidth*14/32, height=sheight/2)

    try:
        discerner = FaceRecognition.FaceRecognition(check_page, swidth/32, sheight/8, swidth*15/32, sheight*3/4)
    except Exception as e:
        text_notice.config(text=str(e))

    update_time()

    check_page.mainloop()


# 登陆/注册窗口
def create_login_page():

    login_page = tk.Tk()
    login_page.title("登陆/注册/管理窗口")
    login_page.attributes("-fullscreen", True)

    tk.Label(login_page, text='考勤管理系统', font=('Arial',54), fg="black").place(x=swidth/8, y=sheight*9/20)

    tk.Label(login_page, text='账户：', font=('Arial',20), fg="green").place(x=swidth*9/16, y=sheight*4/10)

    tk.Label(login_page, text='密码：', font=('Arial',20), fg="green").place(x=swidth*9/16, y=sheight*5/10)

    tk.Button(login_page, text='关闭', command = lambda: login_page.destroy() ).place(x=swidth-75, y=0, width=75)

    tk.Button(login_page, text='登录').place(x=swidth*3/4, y=sheight*3/5)

    button_check = tk.Button(login_page, text='考勤模式', command=create_check_page)

    button_check.place(x=50, y=0, width=75)
    
    input_name = tk.Entry(login_page)
    
    input_pwd = tk.Entry(login_page, show='*')

    input_name.place(x=swidth*10/16, y=sheight*4/10, width=swidth/5)

    input_pwd.place(x=swidth*10/16, y=sheight*5/10, width=swidth/5)

    login_page.mainloop()


if __name__ == '__main__':
    create_login_page()