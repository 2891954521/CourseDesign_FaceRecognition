#所需库
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
import  pickle
import cv2
import os
import time
from win32 import win32gui
from win32.win32api import GetSystemMetrics
import FaceRecognition
from playsound import playsound

'''预加载部分'''

#获取真实的分辨率
hdc = win32gui.GetDC(0)
swidth = GetSystemMetrics (0)
sheight = GetSystemMetrics (1)

'''控件部分'''
def create_check_page():
    #初始化
    check_page=tk.Tk() # 创建窗口
    check_page.title("考勤窗口") # 设置窗口名称 
    check_page.attributes("-fullscreen", True) # 设置登录窗口为全屏模式

    sound_success = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sound','check _success.mp3')






def create_manage_page():

#初始化
    manage_page=tk.Tk() # 创建窗口
    manage_page.title("管理窗口") # 设置窗口名称 
    manage_page.attributes("-fullscreen", True) # 设置登录窗口为全屏模式
    
#点击事件

    #管理界面
    def logout():
        manage_page.destroy()

    def show_manage_page():
        button_lock.place(x=0,y=0,width=50)

        button_logout.place(x=125,y=0,width=75)
        button_edit.place(x=swidth*2/11,y=sheight*13/16)
        button_view.place(x=swidth*4/11,y=sheight*13/16)
        button_work.place(x=swidth*6/11,y=sheight*13/16)
        button_log.place(x=swidth*8/11,y=sheight*13/16)
        manage_page.mainloop()

    def create_lock_page():
        title_lock.place(x=0,y=0)
        input_pwd_unlock.place(x=swidth/2, y=0)
        button_unlock.place(x=swidth*3/4,y=0)

        lock_page.pack()

    def create_edit_page():
        title_edit.place(x=0,y=0)
        button_edit_back.place(x=125,y=0,width=75)
        input_search_name.place(x=swidth/2, y=0)
        button_search.place(x=swidth*3/4,y=0)

        edit_page.pack()

    def create_view_page():
        text_view_title.place(x=0,y=0)
        button_view_back.place(x=125,y=0,width=75)#back

        view_page.pack()
   
    def create_work_page():
        title_work.place(x=0,y=0)
        butten_work_back.place(x=125,y=0,width=75)

        work_page.pack()

    def create_log_page():
        title_log.place(x=0,y=0)
        button_log_back.place(x=125,y=0,width=75)

        log_page.pack()

    #锁定界面
    def unlock():
        lock_page.pack_forget()

    #信息编辑界面
    def edit_back():
        edit_page.pack_forget()

    def search():
        tk.messagebox.showerror(message='搜索中！')

    #信息查看界面
    def view_back():
        view_page.pack_forget()

    #排班界面
    def work_back():
        work_page.pack_forget()

    #操作记录查看
    def log_back():
        log_page.pack_forget()


#控件设定

    #管理界面
    button_lock=tk.Button(manage_page,text='锁定',command=create_lock_page)

    button_logout=tk.Button(manage_page,text='退出登录',command=logout)
    button_edit=tk.Button(manage_page,text='信息编辑',command=create_edit_page)
    button_view=tk.Button(manage_page,text='信息查询',command=create_view_page)
    button_work=tk.Button(manage_page,text='排班',command=create_work_page)
    button_log=tk.Button(manage_page,text='操作记录查询',command=create_log_page)

    #锁定界面
    lock_page=Frame(manage_page,height=sheight,width=swidth)
    title_lock=tk.Label(lock_page,text='输入密码以解锁',font=('',20),fg="green")
    input_pwd_unlock=tk.Entry(lock_page)#密码框
    button_unlock=tk.Button(lock_page,text='解锁',command=unlock)#解锁按钮

    #信息编辑界面
    edit_page=Frame(manage_page,height=sheight,width=swidth)
    title_edit=tk.Label(edit_page,text='信息编辑',font=('',20),fg="green")
    button_edit_back=tk.Button(edit_page,text='返回',command=edit_back)#返回
    input_search_name=tk.Entry(edit_page)#搜索框
    button_search=tk.Button(edit_page,text='搜索',command=search)#搜索按钮

    #信息查看界面
    view_page=Frame(manage_page,height=sheight,width=swidth)
    text_view_title=tk.Label(view_page,text='信息查看',font=('',20),fg="green")
    button_view_back=tk.Button(view_page,text='返回',command=view_back)

    #排班界面
    work_page=Frame(manage_page,height=sheight,width=swidth)
    title_work=tk.Label(work_page,text='排班页',font=('',20),fg="green")
    butten_work_back=tk.Button(work_page,text='返回',command=work_back)#返回

    #操作记录查看
    log_page=Frame(manage_page,height=sheight,width=swidth)
    title_log=tk.Label(log_page,text='操作记录查看',font=('',20),fg="green")
    button_log_back=tk.Button(log_page,text='返回',command=log_back)#返回


#执行程序
    show_manage_page()





#登陆/注册窗口
def create_login_page():

#初始化
    login_page=tk.Tk() # 创建窗口
    login_page.title("登陆/注册/管理窗口") # 设置窗口名称
    login_page.attributes("-fullscreen", True) # 设置登录窗口为全屏模式

#点击事件

    #登录界面
    def show_login_page():
        button_check.place(x=50,y=0,width=75)
        butten_exit.place(x=swidth-75,y=0,width=75)#显示退出按钮
        text_title1.place(x=swidth/8,y=sheight*9/20)#显示"考勤管理系统"
        text_name.place(x=swidth*9/16,y=sheight*4/10)#显示"账户"
        input_name.place(x=swidth*10/16, y=sheight*4/10,width=swidth/5)#显示"账户输入框"
        text_pwd.place(x=swidth*9/16,y=sheight*5/10)#显示"密码"
        input_pwd.place(x=swidth*10/16,y=sheight*5/10,width=swidth/5)#显示密码输入框
        butten_signup.place(x=swidth*13/20,y=sheight*3/5)#显示注册按钮
        butten_manage.place(x=swidth*3/4,y=sheight*3/5)#显示登录按钮
        login_page.mainloop()

    def close():
        login_page.destroy()
    
    def create_signup_page():
        button_back_signup.place(x=0,y=0,width=75)#返回按钮
        button_quit_signup.place(x=swidth-75,y=0,width=75)#关闭按钮
        text_title.place(x=swidth/8,y=sheight*8/20)#考勤管理系统管理员账户注册
        text_name2.place(x=swidth*8/16,y=sheight*30/100)
        text_pwd21.place(x=swidth*8/16,y=sheight*40/100)
        text_pwd22.place(x=swidth*8/16,y=sheight*50/100)
        text_invitation_code.place(x=swidth*8/16,y=sheight*60/100)
        new_name.place(x=swidth*10/16, y=sheight*30/100,width=swidth/5)#显示账户输入框
        new_pwd.place(x=swidth*10/16, y=sheight*40/100,width=swidth/5)#显示密码输入框
        new_pwd2.place(x=swidth*10/16, y=sheight*50/100,width=swidth/5)#显示确认密码输入框
        invitation_code.place(x=swidth*10/16, y=sheight*60/100,width=swidth/5)#显示邀请码输入框
        button_signup.place(x=swidth*22/32,y=sheight*70/100)#注册
        signup_page.pack()

    #注册界面
    def back():
        signup_page.pack_forget()

#控件设定

    #登录界面
    button_check=tk.Button(login_page,text='考勤模式',command=create_check_page)
    text_title1=tk.Label(login_page,text='考勤管理系统',font=('',54),fg="black")#"考勤管理系统"
    text_name=tk.Label(login_page,text='账户：',font=('',20),fg="green")#"账户"
    input_name=tk.Entry(login_page)#"账户输入框"
    text_pwd=tk.Label(login_page,text='密码：',font=('',20),fg="green")#"密码"
    input_pwd=tk.Entry(login_page, show='*')#密码输入框
    butten_exit=tk.Button(login_page,text='关闭',command=close)#退出按钮
    butten_signup=tk.Button(login_page,text='注册',command=create_signup_page)#注册按钮
    butten_manage=tk.Button(login_page,text='登录',command=create_manage_page)#登录按钮

    #注册界面
    signup_page=Frame(login_page,height=sheight,width=swidth)
    button_back_signup=tk.Button(signup_page,text='返回',command=back)
    button_quit_signup=tk.Button(signup_page,text='关闭',command=close)
    text_title=tk.Label(signup_page,text='考勤管理系统\n管理员账户注册',font=('',54),fg="black")
    text_name2=tk.Label(signup_page,text='账户：',font=('',20),fg="green")
    text_pwd21=tk.Label(signup_page,text='密码：',font=('',20),fg="green")
    text_pwd22=tk.Label(signup_page,text='确认密码：',font=('',20),fg="green")
    text_invitation_code=tk.Label(signup_page,text='邀请码：',font=('',20),fg="green")
    button_signup=tk.Button(signup_page,text='注册',command=create_signup_page)
    new_name = tk.Entry(signup_page)#账户输入框
    new_pwd = tk.Entry(signup_page)#密码输入框
    new_pwd2 = tk.Entry(signup_page)#确认密码输入框
    invitation_code = tk.Entry(signup_page)#邀请码输入框

#执行程序
    show_login_page()
















create_login_page()
































# def login_page():
#     def ss():
#         butten_manage.place(x=swidth*3/4,y=sheight*3/5)#显示登录按钮

#     def aa():
#         text_check.place_forget()
#     login_page=tk.Tk() # 创建登录窗口
#     login_page.title("登录窗口") # 设置窗口名称
#     login_page.attributes("-fullscreen", True) # 设置登录窗口为全屏模式

    # text_title1=tk.Label(login_page,text='考勤管理系统',font=('',54),fg="black")#"考勤管理系统"
    # text_name=tk.Label(login_page,text='账户：',font=('',20),fg="green")#"账户"
    # input_name=tk.Entry(login_page)#"账户输入框"
    # text_pwd=tk.Label(login_page,text='密码：',font=('',20),fg="green")#"密码"
    # input_pwd=tk.Entry(login_page, show='*')#密码输入框
    # butten_exit=tk.Button(login_page,text='退出',command=aa)#退出按钮
    # butten_signup=tk.Button(login_page,text='注册',command=ss)#注册按钮
    # butten_manage=tk.Button(login_page,text='登录',command=manage_page)#登录按钮
    
    # butten_exit.place(x=125,y=0,width=75)#显示退出按钮
    # text_title1.place(x=swidth/8,y=sheight*9/20)#显示"考勤管理系统"
    # text_name.place(x=swidth*9/16,y=sheight*4/10)#显示"账户"
    # input_name.place(x=swidth*10/16, y=sheight*4/10,width=swidth/5)#显示"账户输入框"
    # text_pwd.place(x=swidth*9/16,y=sheight*5/10)#显示"密码"
    # input_pwd.place(x=swidth*10/16,y=sheight*5/10,width=swidth/5)#显示密码输入框
    # butten_signup.place(x=swidth*13/20,y=sheight*3/5)#显示注册按钮
    # butten_manage.place(x=swidth*3/4,y=sheight*3/5)#显示登录按钮
#     login_page.mainloop()


# login_page()

#     # global butten_exit
#     # global text_check
#     # global text_name
#     # global input_name
#     # global text_pwd
#     # global input_pwd
#     # global butten_signup
#     # global butten_manage
#     # global login_page