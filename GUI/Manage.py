#所需库
import os
import time
import tkinter as tk
from tkinter import *
from win32.win32api import GetSystemMetrics
import FaceRecognition
from playsound import playsound
import json


#预加载

# ##获取真实的分辨率
# swidth = GetSystemMetrics (0)
# sheight = GetSystemMetrics (1)

root=tk.Tk()
root.attributes("-fullscreen", True) # 设置登录窗口为全屏模式
swidth=root.winfo_screenwidth()
sheight=root.winfo_screenheight()
root.destroy()




#考勤页面
def create_check_page():
    
    check_page = tk.Toplevel() # 创建窗口
    check_page.title("考勤窗口") # 设置窗口名称 
    check_page.attributes("-fullscreen", True) # 设置登录窗口为全屏模式

    def success(id):
        text_notice.config(text = id + ' 签到成功！')
        playsound(sound_success)
        check_page.update()

    def detect():
        discerner.detect(success)

    def update_time():
        text_time.config(text = time.strftime('%Y-%m-%d\n%H:%M:%S', time.localtime(time.time())))
        text_time.after(1000, update_time)  
    
    sound_success = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound', 'check _success.mp3')
    tk.Label(check_page, text = '考勤系统', font = ('', 20), fg = "black").place(x = 16, y = 0, width = swidth, height = sheight/8)
    tk.Button(check_page, text = '关闭', command = check_page.destroy).place(x = swidth-75, y = 0, width = 75)#关闭按钮
    tk.Label(check_page, bg = "pink").place(x = swidth/32, y = sheight/8, width = swidth*15/32, height = sheight*3/4)#图像显示区域
    text_notice = tk.Label(check_page, text = 'Welcome', font = ('', 40), fg = "black")
    text_notice.place(x = swidth*17/32, y = sheight/8, width = swidth*14/32, height = sheight/8)
    text_time = tk.Label(check_page, text = '加载中', font = ('', 70), fg = "black")
    text_time.place(x = swidth*17/32, y = sheight/4, width = swidth*14/32, height = sheight/2)
    tk.Button(check_page, text = '检测', command = detect).place(x = swidth*17/32, y = sheight*3/4, width = swidth*14/32, height = sheight/8)

    #执行程序

    try:
        discerner = FaceRecognition.FaceRecognition(check_page, x = swidth/32, y = sheight/8, w = swidth*15/32, h = sheight*3/4)
    except Exception as e:
        text_time.config(text = e.__str__)

    update_time()
    check_page.mainloop()

#管理页面
def create_manage_page():

    ##管理界面(直接显示)
    manage_page = tk.Toplevel() # 创建窗口
    manage_page.title("管理窗口") # 设置窗口名称 
    manage_page.attributes("-fullscreen", True) # 设置登录窗口为全屏模式

    def logout():
        manage_page.destroy()
        lock_page.pack()
    
    def create_lock_page():
        lock_page.pack()
    
    def create_edit_page():
        edit_page.pack()

    def create_view_page():
        view_page.pack()
   
    def create_work_page():
        work_page.pack()

    def create_log_page():
        log_page.pack()

    tk.Button(manage_page, text = '锁定', command = create_lock_page).place(x = 0, y = 0, width = 50)
    tk.Button(manage_page, text = '退出登录', command = logout).place(x = swidth-75, y = 0, width = 75)
    tk.Button(manage_page, text = '信息编辑', command = create_edit_page).place(x = swidth*2/11, y = sheight*13/16)
    tk.Button(manage_page, text = '信息查询', command = create_view_page).place(x = swidth*4/11, y = sheight*13/16)
    tk.Button(manage_page, text = '排班', command = create_work_page).place(x = swidth*6/11, y = sheight*13/16)
    tk.Button(manage_page, text = '操作记录查询', command = create_log_page).place(x = swidth*8/11, y = sheight*13/16)


    ##锁定界面
    lock_page = Frame(manage_page, height = sheight, width = swidth)

    def unlock():
        lock_page.pack_forget()

    input_pwd_unlock = StringVar()
    tk.Label(lock_page, text = '输入密码以解锁', font = ('', 20), fg = "green").place(x = 0, y = 0)
    tk.Entry(lock_page,textvariable=input_pwd_unlock).place(x = swidth/2, y = 0)#密码框
    tk.Button(lock_page, text = '解锁', command = unlock).place(x = swidth*3/4, y = 0)#解锁按钮


    ##信息编辑界面
    edit_page = Frame(manage_page, height = sheight, width = swidth)

    def search():
        tk.messagebox.showerror(message = '搜索中！')   

    input_search_name = StringVar()
    avatar=NONE
    tk.Label(edit_page, text = '信息编辑', font = ('', 20), fg = "black").place(x = 0, y = 0, width = swidth, height = sheight*3/48)
    tk.Button(edit_page, text = '返回', command = edit_page.pack_forget).place(x = swidth-75, y = 0, width = 75)#返回
    tk.Entry(edit_page,textvariable=input_search_name).place(x = swidth/30, y = sheight*3/48, width = swidth*8/30, height = sheight*3/48)#搜索框
    tk.Button(edit_page, text = '搜索', command = search).place(x = swidth*9/30, y = sheight*3/48, width = swidth*2.5/30, height = sheight*3/48)#搜索按钮
    img_avatar=tk.Label(edit_page, bg='pink')
    img_avatar.place(x=swidth*1/30, y=sheight*7/48, width = swidth*10.5/30, height = sheight*26/48)  #用来存放图像
    tk.Label(edit_page, text = '姓名', font = ('', 20), fg = "black").place(x=swidth*1.5/30, y=sheight*34/48, width = swidth*10/30, height = sheight*6/48)
    tk.Label(edit_page, text = '学号', font = ('', 20), fg = "black").place(x=swidth*1.5/30, y=sheight*40/48, width = swidth*10/30, height = sheight*6/48)
    tk.Label(edit_page, text = '   姓名   |     学号     |     学院     |      联系方式      ', font = ('', 20), bg='yellow', fg = "black").place(x=swidth*2/5, y = sheight*3/48, width = swidth*17/30, height = sheight*3/48)
    #更新图像用
        # avatar=NONE
        # img_avatar.config(image=avatar)

    ##信息查看界面
    view_page = Frame(manage_page, height = sheight, width = swidth)

    tk.Label(view_page, text = '信息查看', font = ('', 20), fg = "black").place(x = 16, y = 0, width = swidth, height = sheight/16)
    tk.Button(view_page, text = '返回', command = view_page.pack_forget).place(x = swidth-75, y = 0, width = 75)#返回


    ##排班界面
    work_page = Frame(manage_page, height = sheight, width = swidth)

    tk.Label(work_page, text = '排班页', font = ('', 20), fg = "black").place(x = 16, y = 0, width = swidth, height = sheight/16)
    tk.Button(work_page, text = '返回', command = work_page.pack_forget).place(x = swidth-75, y = 0, width = 75)#返回
    
    ##操作记录查看
    log_page = Frame(manage_page, height = sheight, width = swidth)

    tk.Label(log_page, text = '操作记录查看', font = ('', 20), fg = "black").place(x = 16, y = 0, width = swidth, height = sheight/16)
    tk.Button(log_page, text = '返回', command = log_page.pack_forget).place(x = swidth-75, y = 0, width = 75)#返回


    #执行程序
    manage_page.mainloop()

#登陆/注册窗口
def create_login_page():

        #登录界面(直接显示)
    login_page = tk.Tk() # 创建窗口
    login_page.title("登陆/注册/管理窗口") # 设置窗口名称
    login_page.attributes("-fullscreen", True) # 设置登录窗口为全屏模式

    def goto_manage_page():
        
        pwd=''
        if input_pwd.get() == pwd :
            create_manage_page()

    print(swidth,sheight)
    def create_signup_page():
        signup_page.pack()
    # round((size-8)*3/4)
    input_name = StringVar()
    input_pwd = StringVar()

    tk.Button(login_page, text = '考勤', command = create_check_page, font = ('', round((sheight/30-8)*3/4))).place(x = 0, y = 0, width = 75)

    tk.Label(login_page, text = '考勤管理系统', font = ('', round((sheight/10-8)*3/4)), fg = "black").place(x = swidth/8, y = sheight*9/20)
    
    tk.Label(login_page, text = '账户：', font = ('', round((sheight/25-8)*3/4)), fg = "green").place(x = swidth*9/16, y = sheight*35/80)
    #"账户输入框"
    tk.Entry(login_page, textvariable = input_name, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*10/16, y = sheight*35/80, width = swidth/5)
    
    tk.Label(login_page, text = '密码：', font = ('', round((sheight/25-8)*3/4)), fg = "green").place(x = swidth*9/16, y = sheight*21/40)
    #密码输入框
    tk.Entry(login_page, textvariable = input_pwd, font = ('', round((sheight/25-8)*3/4)), show = '*').place(x = swidth*10/16, y = sheight*21/40, width = swidth/5)
    
    tk.Button(login_page, text = '关闭', command = login_page.destroy, font = ('', round((sheight/30-8)*3/4))).place(x = swidth-75, y = 0, width = 75)

    tk.Button(login_page, text = '注册', command = create_signup_page, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*25/40, y = sheight*26/40)
  
    tk.Button(login_page, text = '登录', command = goto_manage_page, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*29/40, y = sheight*26/40)

        #注册界面(点击后显示)
    signup_page = Frame(login_page, height = sheight, width = swidth)






    new_name = tk.StringVar()
    new_pwd = tk.StringVar()
    new_pwd2 = tk.StringVar()
    invitation_code = tk.StringVar()

    tk.Button(signup_page, text = '返回', command = signup_page.pack_forget, font = ('', round((sheight/30-8)*3/4))).place(x = 0, y = 0, width = 75)

    tk.Button(signup_page, text = '关闭', command = login_page.destroy, font = ('', round((sheight/30-8)*3/4))).place(x = swidth-75, y = 0, width = 75)

    tk.Label(signup_page, text = '考勤管理系统\n管理员账户注册', font = ('', round((sheight/10-8)*3/4)), fg = "black").place(x = swidth*4/40, y = sheight*8/20)
    
    tk.Label(signup_page, text = '账户：', font = ('', round((sheight/25-8)*3/4)), fg = "green").place(x = swidth*21/40, y = sheight*33/100)

    tk.Label(signup_page, text = '密码：', font = ('', round((sheight/25-8)*3/4)), fg = "green").place(x = swidth*21/40, y = sheight*43/100)

    tk.Label(signup_page, text = '确认密码：', font = ('', round((sheight/25-8)*3/4)), fg = "green").place(x = swidth*21/40, y = sheight*53/100)

    tk.Label(signup_page, text = '邀请码：', font = ('', round((sheight/25-8)*3/4)), fg = "green").place(x = swidth*21/40, y = sheight*63/100)
    #账户输入框
    tk.Entry(signup_page, textvariable = new_name, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*10/16, y = sheight*33/100, width = swidth/5)
    #密码输入框
    tk.Entry(signup_page, textvariable = new_pwd, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*10/16, y = sheight*43/100, width = swidth/5)
    #确认密码输入框
    tk.Entry(signup_page, textvariable = new_pwd2, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*10/16, y = sheight*53/100, width = swidth/5)
    #邀请码输入框
    tk.Entry(signup_page, textvariable = invitation_code, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*10/16, y = sheight*63/100, width = swidth/5)

    tk.Button(signup_page, text = '注册', command = create_signup_page, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*27/40, y = sheight*73/100)


    #执行程序
    login_page.mainloop()


#主程序
create_login_page()