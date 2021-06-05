import tkinter as tk
import  tkinter.messagebox
from PIL import Image,ImageTk
import  pickle
import cv2
import os
import 


#trainer = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
#登录页
login_page=tk.Tk()
login_page.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico'))#设置窗口图标,将ico放在同级目录下。
login_page.title("请登录")#设置窗口名称
login_page.geometry("1280x720+125+40")
#login_page.attributes("-fullscreen", True)#全屏模式：True 全屏；False 正常显示
photo = tk.PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)),'BG.png'))#创建一个图片管理类#file：图片路径
imgLabel = tk.Label(login_page,image=photo)#把图片整合到标签类中
imgLabel.pack()#自动对齐
# 获取屏幕的大小;
height = login_page.winfo_height()
width = login_page.winfo_width()
# 获取窗体的位置
x = login_page.winfo_x()
y = login_page.winfo_y()
print(width, height, x, y)
#tk.Label(text="天王盖地虎").pack(x=100,y=320)
tk.Label(login_page,text='考勤管理系统',font=(54),fg="black").place(x=100,y=320)
tk.Label(login_page,text='账户：',font=(20),fg="green").place(x=780,y=310)
tk.Label(login_page,text='密码：',font=(20),fg="green").place(x=780,y=380)

admin_name = tk.StringVar()
tk.Entry(login_page, textvariable=admin_name).place(x=900, y=315)
admin_pwd = tk.StringVar()
tk.Entry(login_page, textvariable=admin_pwd, show='*').place(x=900, y=385)

def exit():
#    tk.messagebox.showerror(message='退出？')
    login_page.destroy()
tk.Button(login_page,text='退出',command=exit).place(x=50,y=0)
def signup():
    tk.messagebox.showerror(message='注册！')
tk.Button(login_page,text='注册',command=signup).place(x=870,y=500)
def login():
    #tk.messagebox.showerror(message='登录！')
    create_manage_page()
    # print(admin_pwd.get())
    # if admin_pwd.get()=='admin' :
    #     create_manage_page()

tk.Button(login_page,text='登录',command=login).place(x=950,y=500)

#注册页


#管理页
def create_manage_page():
    manage_page = tk.Toplevel()
    manage_page.title("管理页")
    manage_page.geometry("1920x1080+0+0")
    manage_page.attributes("-fullscreen", True)#全屏模式：True 全屏；False 正常显示
    imgLabel = tk.Label(manage_page,image=photo)#把图片整合到标签类中
    imgLabel.pack()#自动对齐
    mp = tk.Message(manage_page, text="I love Python!")
    mp.pack()
    def quit_manage_page():
        manage_page.destroy()
    tk.Button(manage_page,text='退出登录',command=quit_manage_page).place(x=50,y=0)
    def information():
        # 获取屏幕的大小;
        height = manage_page.winfo_height()
        width = manage_page.winfo_width()
        # 获取窗体的位置
        x = manage_page.winfo_x()
        y = manage_page.winfo_y()
        print(width, height, x, y)
    tk.Button(manage_page,text='信息',command=information).place(x=150,y=0)



#搜索页
#信息管理
#信息查看
#排班页
#操作记录查看





#考勤页


def create():
    top = tk.Toplevel()
    top.title("Python")
    top.geometry("1920x1080+0+0")
    top.attributes("-fullscreen", True)#全屏模式：True 全屏；False 正常显示
    msg = tk.Message(top, text="I love Python!")
    msg.pack()
    def quit_top_page():
        top.destroy()
    tk.Button(top,text='退出',command=quit_top_page).place(x=50,y=0)
tk.Button(login_page, text="创建顶级窗口", command=create).place(x=100,y=0)





















login_page.mainloop()