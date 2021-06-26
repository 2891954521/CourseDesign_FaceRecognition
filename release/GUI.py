import time
import tkinter as tk
import tkinter.messagebox

import System
import FaceRecognition

from tkinter import ttk


class BasePage:

    page = None

    width = 640

    height = 480

    system = None

    def __init__(self,system):
        self.system = system

    def place_widget(self, widget, x, y, w = 0, h = 0):
        if h == 0:
            if w == 0:
                widget.place(x = self.width*x//100, y = self.height*y//100)
            else:
                widget.place(x = self.width*x//100, y = self.height*y//100, width = self.width*w//100)
        else:
            widget.place(x = self.width*x//100, y = self.height*y//100, width = self.width*w//100, height = self.height*h//100)

    def get_font(self, size):
        return ('Arial', round((self.height*size//100-8)*3//4))


class MainPage(BasePage):

    def __init__(self,system):

        super().__init__(system)

        self.page = tk.Tk()

        self.page.title("考勤管理系统")
        self.page.attributes("-fullscreen", True)

        self.input_uid = tk.StringVar()
        self.input_pwd = tk.StringVar()

        self.page.update()

        self.width = self.page.winfo_screenwidth()
        self.height = self.page.winfo_screenheight()

        self.place_widget(tk.Label(self.page, text = '考勤管理系统', font = self.get_font(10), fg = "black"), 0, 5, 100, 12.5)
        
        self.place_widget(tk.Button(self.page, text = '考勤', command = lambda:self.system.check_page.page.pack(), font = self.get_font(3)), 0, 0, 5)
        self.place_widget(tk.Button(self.page, text = '关闭', command = self.page.destroy, font = self.get_font(3)), 95, 0, 5)
        
        self.place_widget(tk.Label(self.page, text = '学号:', font = self.get_font(5)), 61, 45)
        self.entery_uid = tk.Entry(self.page, textvariable = self.input_uid, font = self.get_font(5))
        self.place_widget(self.entery_uid, 68, 45, 20)

        self.place_widget(tk.Label(self.page, text = '密码:', font = self.get_font(5)), 61, 55)
        self.entery_pwd = tk.Entry(self.page, textvariable = self.input_pwd, font = self.get_font(5), show = '*')
        self.place_widget(self.entery_pwd, 68, 55, 20)

        self.place_widget(tk.Button(self.page, text = '登录', command = self.login, font = self.get_font(4)), 65, 65, 6)
        self.place_widget(tk.Button(self.page, text = '刷脸登录', command = self.check_face, font = self.get_font(4)), 75, 65, 10)
    

    def login(self):
        status, msg = self.system.login(self.input_uid.get(), self.input_pwd.get())
        if status == 0:
            self.entery_uid.delete(0, tk.END)
            self.entery_pwd.delete(0, tk.END)
            self.system.manage_page.show()
        else:
            tkinter.messagebox.showerror('错误',msg)
    

    def check_face(self):
        uid = self.system.discerner.detection()
        if uid is not None and self.system.data[uid]['admin'] == 1:
            self.system.manage_page.show()
        else:
            tkinter.messagebox.showerror('错误','您不是管理员')


class ManagePage(BasePage):

    main = None

    def __init__(self,system,main):
    
        super().__init__(system)

        self.main = main

        self.page = tk.Frame(self.main.page, width = self.main.width, height = self.main.height)
        self.width = self.main.width
        self.height = self.main.height

        self.input_id = tk.StringVar()
        self.input_name = tk.StringVar()

        self.place_widget(tk.Label(self.page, text = '信息编辑', font = self.get_font(5), fg = "black"), 18, 10)

        self.place_widget(tk.Button(self.page, text = '返回', command = self.page.pack_forget, font = self.get_font(3)), 0, 0, 5)

        self.place_widget(tk.Button(self.page, text = '关闭', command = self.main.page.destroy, font = self.get_font(3)), 95, 0, 5)

        self.tree = ttk.Treeview(self.page, columns=["学号", "姓名"], show = 'headings')
        self.tree.column("学号", width=100)
        self.tree.column("姓名", width=100)
        self.tree.heading("学号", text="学号")
        self.tree.heading("姓名", text="姓名")
        self.place_widget(self.tree, 53, 10, 42, 56)

        # 竖直滚动条
        vbar = tk.Scrollbar(self.page)
        self.place_widget(vbar, 95, 10, 2, 56)
        # 绑定事件
        self.tree.configure(yscrollcommand = vbar.set)
        vbar.configure(command = self.tree.yview)

        self.place_widget(tk.Label(self.page, text = '学号', font = self.get_font(4)), 53, 75, 5, 6)

        self.entery_id = tk.Entry(self.page, textvariable = self.input_id, font = self.get_font(4))
        self.place_widget(self.entery_id, 58, 75, 22, 6)

        self.place_widget(tk.Label(self.page,text = '姓名', font = self.get_font(4)), 53, 83, 5, 6)

        self.entery_name = tk.Entry(self.page, textvariable = self.input_name, font = self.get_font(4))
        self.place_widget(self.entery_name, 58, 83, 22, 6)

        self.place_widget(tk.Button(self.page, text = '添加/更新', command = self.input_face, font = self.get_font(3)), 82, 76, 12, 12)
        
        self.update_list()
        

    def input_face(self):

        uid = self.input_id.get()

        if uid is None or uid == '':
            tkinter.messagebox.showerror('错误','请填写学号！')
            return

        if uid not in self.system.data.keys():

            name = self.input_name.get()
            if name is None or name == '':
                tkinter.messagebox.showerror('错误','请填写姓名！')
                return

            msg = self.system.addUser(uid,name)
            if msg is None:
                self.system.data[uid] = { 'name': name }
            else:
                tkinter.messagebox.showerror('错误',msg)
                return

        self.system.playSound('录入提示')
        
        msg  = self.system.discerner.inputFace(uid)
        if msg  == None:
            self.update_list()
            self.entery_id.delete(0, tk.END)
            self.entery_name.delete(0, tk.END)
            self.system.playSound('录入成功')
        else:
            self.system.playSound('录入失败')
            tkinter.messagebox.showerror('错误','录入失败！' + msg)
            

    def show(self):
        self.update_list()
        self.page.pack()


    def update_list(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)
        postion = 0
        for uid in self.system.data:
            postion += 1
            self.tree.insert("", postion, values=(uid, self.system.data[uid]["name"]))


class CheckPage(BasePage):

    main = None

    def __init__(self, system, main):

        super().__init__(system)

        self.main = main

        self.page = tk.Frame(self.main.page, width = self.main.width, height = self.main.height)
        self.width = self.main.width
        self.height = self.main.height

        self.delay = 0

        self.place_widget(tk.Label(self.page, text = 'Welcome', font = self.get_font(10), fg = "black"), 0, 5, 100, 12.5)

        self.place_widget(tk.Button(self.page, text = '返回', command = self.page.pack_forget, font = self.get_font(3)), 0, 0, 5)
        self.place_widget(tk.Button(self.page, text = '关闭', command = self.main.page.destroy, font = self.get_font(3)), 95, 0, 5)

        self.text_time = tk.Label(self.page, text = '', font = self.get_font(10), fg = "black")
        self.place_widget(self.text_time, 53, 25, 44, 50)

        self.place_widget(tk.Button(self.page, text = '签到/签退', command = self.detect), 53, 75, 44, 12.5)

        self.update_time()


    def update_time(self):
        if self.delay > 0:
            self.delay -= 1
        else:
            self.text_time.config(text = time.strftime('%Y-%m-%d\n%H:%M:%S', time.localtime(time.time())))
        self.text_time.after(1000, self.update_time)  


    def detect(self):
        uid = self.system.discerner.detection()

        if uid == None:
            self.delay = 3
            self.text_time.config(text = '超时！')
            return
        
        status, msg = self.system.signIn(uid)
        self.delay = 3
        if status == 0:
            self.text_time.config(text = self.system.data[uid]['name'] + ',' + msg)
        else:
            self.text_time.config(text = msg)

        self.page.update()
