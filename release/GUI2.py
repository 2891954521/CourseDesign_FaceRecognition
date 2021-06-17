#所需库
import os
import time
import pickle
import tkinter as tk
from tkinter import *
import tkinter.messagebox
import FaceRecognition
from playsound import playsound

#相关文件/数据
sound_checkin_success = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound', 'checkin_success.mp3')
sound_checkout_success = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound', 'checkout_success.mp3')
sound_start_input = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sound','start_enter.mp3')
sound_input_success = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sound','enter_success.mp3')

#加载配置
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.bin'),'rb') as fi :data = pickle.load(fi)
print(data)
#print(data)
    #页面设置
main_page = tk.Tk() # 创建窗口
main_page.title("考勤管理系统") # 设置窗口名称
main_page.attributes("-fullscreen", True) # 设置登录窗口为全屏模式
swidth=main_page.winfo_screenwidth()
sheight=main_page.winfo_screenheight()

def initialize():
    data = {'888':['admin',False],
'2029740101':['ABC',False],'2029740102':['ABC',False],'2029740103':['ABC',False],
'2029740104':['ABC',False],'2029740105':['ABC',False],'2029740106':['ABC',False],
'2029740107':['ABC',False],'2029740108':['ABC',False],'2029740109':['ABC',False],
'2029740110':['ABC',False],'2029740111':['ABC',False],'2029740112':['ABC',False],
'2029740113':['ABC',False],'2029740114':['ABC',False],'2029740115':['ABC',False],
'2029740116':['ABC',False],'2029740117':['ABC',False],'2029740118':['ABC',False],
'2029740119':['ABC',False],'2029740120':['ABC',False],'2029740121':['ABC',False],
'2029740122':['ABC',False],'2029740123':['ABC',False],'2029740124':['ABC',False],
'2029740125':['ABC',False],'2029740126':['ABC',False],'2029740127':['ABC',False],
'20297401228':['ABC',False]}
    #FaceRecognition.deleteTrainer()
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.bin'),'wb') as fi :pickle.dump(data,fi)
  
def close():
    main_page.destroy()

def check_pwd():
    print( data['888'][0], input_pwd.get())
    if input_pwd.get() ==  data['888'][0] :
        entery_pwd.delete(0, END)
        manage_page.pack()
    else:
        tkinter.messagebox.showerror('错误','密码错误')
        
def check_face():
    if discerner.detection()=='888':
        manage_page.pack()
    else:
        tkinter.messagebox.showerror('错误','您不是管理员')

input_pwd = StringVar()

tk.Label(main_page, text = '考勤管理系统', font = ('', round((sheight/10-8)*3/4)), fg = "black").place(x = 0, y = sheight*5/100, width = swidth, height = sheight*12.5/100)
tk.Button(main_page, text = '考勤', command = lambda: check_page.pack(), font = ('', round((sheight/30-8)*3/4))).place(x = 0, y = 0, width = swidth*5/100)
tk.Button(main_page, text = '关闭', command = close, font = ('', round((sheight/30-8)*3/4))).place(x = swidth*95/100, y = 0, width = swidth*5/100)
tk.Label(main_page, text = '密码：', font = ('', round((sheight/20-8)*3/4))).place(x = swidth*61/100, y = sheight*45/100)
entery_pwd=tk.Entry(main_page, textvariable = input_pwd, font = ('', round((sheight/20-8)*3/4)), show = '*')
entery_pwd.place(x = swidth*68/100, y = sheight*45/100, width = swidth*20/100)
tk.Button(main_page, text = '登录', command = lambda: check_pwd(), font = ('', round((sheight/25-8)*3/4))).place(x = swidth*65/100, y = sheight*58/100, width=swidth*6/100)
tk.Button(main_page, text = '刷脸登录', command = check_face, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*75/100, y = sheight*58/100, width=swidth*10/100)
tk.Button(main_page, text = '修改密码', command = lambda: change_pwd_page.pack(), font = ('', round((sheight/25-8)*3/4))).place(x = swidth*70/100, y = sheight*70/100, width=swidth*10/100)





        #密码修改界面
change_pwd_page= Frame(main_page, height = sheight, width = swidth)

def change_admin() :
    if old_pwd.get()== data['888'][0] and new_pwd.get()==new_pwd2.get():
        data['888'][0]=new_pwd.get()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.bin'),'wb') as info_fi :pickle.dump(data,info_fi)
        
def update_face():
    if old_pwd.get()== data['888'][0]:
        change_pwd_title.config(text='请面向摄像头')
        playsound(sound_start_input)
        discerner.inputFace('888', inputFinish)
        change_pwd_title.config(text='考勤管理系统')

old_pwd = tk.StringVar()
new_pwd = tk.StringVar()
new_pwd2 = tk.StringVar()
change_pwd_title=tk.Label(change_pwd_page, text = '考勤管理系统', font = ('', round((sheight/10-8)*3/4)), fg = "black")
change_pwd_title.place(x = 0, y = sheight*5/100, width = swidth, height = sheight*12.5/100)
tk.Button(change_pwd_page, text = '返回', command = change_pwd_page.pack_forget, font = ('', round((sheight/30-8)*3/4))).place(x = 0, y = 0, width = swidth*5/100)
tk.Button(change_pwd_page, text = '关闭', command = close, font = ('', round((sheight/30-8)*3/4))).place(x = swidth*95/100, y = 0, width = swidth*5/100)
tk.Label(change_pwd_page, text = '原密码：', font = ('', round((sheight/25-8)*3/4)), fg = "green").place(x = swidth*21/40, y = sheight*33/100)
tk.Entry(change_pwd_page, textvariable = old_pwd, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*10/16, y = sheight*33/100, width = swidth/5)
tk.Label(change_pwd_page, text = '新密码：', font = ('', round((sheight/25-8)*3/4)), fg = "green").place(x = swidth*21/40, y = sheight*43/100)
tk.Entry(change_pwd_page, textvariable = new_pwd, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*10/16, y = sheight*43/100, width = swidth/5)
tk.Label(change_pwd_page, text = '确认密码：', font = ('', round((sheight/25-8)*3/4)), fg = "green").place(x = swidth*21/40, y = sheight*53/100)
tk.Entry(change_pwd_page, textvariable = new_pwd2, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*10/16, y = sheight*53/100, width = swidth/5)
tk.Button(change_pwd_page, text = '修改密码', command=change_admin, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*27/40, y = sheight*73/100)
tk.Button(change_pwd_page, text = '更新面部数据', command=update_face, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*27/40, y = sheight*80/100)






        #考勤页面
check_page =Frame(main_page, height = sheight, width = swidth)

def update_time():
    text_time.config(text = time.strftime('%Y-%m-%d\n%H:%M:%S', time.localtime(time.time())))
    text_time.after(1000, update_time)  

def detect():
    faceid=discerner.detection()
    if data[faceid][1] ==True:
        data[faceid][1]=False
        text_time.config(text = faceid + ' 签退成功！')
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.bin'),'wb') as fi :pickle.dump(data,fi)
        playsound(sound_checkout_success)
    elif data[faceid][1]==False :
        data[faceid][1]=True
        text_time.config(text = faceid + ' 签到成功！')
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.bin'),'wb') as fi :pickle.dump(data,fi)
        playsound(sound_checkin_success)


    check_page.update()
    text_time.config(text = time.strftime('%Y-%m-%d\n%H:%M:%S', time.localtime(time.time())))

tk.Label(check_page, text = 'Welcome', font = ('', round((sheight/10-8)*3/4)), fg = "black").place(x = 0, y = sheight*5/100, width = swidth, height = sheight*12.5/100)
tk.Button(check_page, text = '返回', command = check_page.pack_forget, font = ('', round((sheight/30-8)*3/4))).place(x = 0, y = 0, width = swidth*5/100)
tk.Button(check_page, text = '关闭', command = close, font = ('', round((sheight/30-8)*3/4))).place(x = swidth*95/100, y = 0, width = swidth*5/100)
text_time = tk.Label(check_page, text = '加载中', font = ('', 70), fg = "black")
text_time.place(x = swidth*53/100, y = sheight/4, width = swidth*44/100, height = sheight/2)
tk.Button(check_page, text = '检测', command = detect).place(x = swidth*53/100, y = sheight*3/4, width = swidth*44/100, height = sheight*12.5/100)






        #管理页面
manage_page= Frame(main_page, height = sheight, width = swidth) 

def add_stu():
    if input_id.get()!='' and input_name.get()!='':
        data[input_id.get()]=[input_name.get(),False]
        inputFace(input_id.get())
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.bin'),'wb') as info_fi :pickle.dump(data,info_fi)
        update_list()
        tkinter.messagebox.showinfo('提示','录入完成')
    else:
        tkinter.messagebox.showerror('错误','错误，数据填写不完整')

def del_stu(): 
    if input_id.get()!='' :
        if input_id.get() in data:
            del data[input_id.get()]
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.bin'),'wb') as info_fi :pickle.dump(data,info_fi)
            print(data)
            update_list()
        else :
            tkinter.messagebox.showerror('错误','用户不存在')

def inputFace(faceid):
    manage_title.config(text='请面向摄像头开始采集人脸信息')
    playsound(sound_start_input)
    discerner.inputFace(faceid, inputFinish)

def inputFinish(text):
    manage_title.config(text=text)
    playsound(sound_input_success)
    manage_page.update()

def update_list():
    list_box.delete(0, END)
    for i in data :
        if i != '888':list_box.insert("end",'            '+i+' '*(21-len(i))+'|    '+data.get(i)[0])


face_id = StringVar()
input_id = StringVar()
input_name = StringVar()
manage_title=tk.Label(manage_page, text = '信息编辑', font = ('', round((sheight/22-8)*3/4)), fg = "black")
manage_title.place(x = 16, y = 0, width = swidth, height = sheight*12.5/100)
tk.Button(manage_page, text = '返回', command = manage_page.pack_forget, font = ('', round((sheight/30-8)*3/4))).place(x = 0, y = 0, width = 75)
tk.Button(manage_page, text = '关闭', command = close, font = ('', round((sheight/30-8)*3/4))).place(x = swidth*95/100, y = 0, width = swidth*5/100)
tk.Entry(manage_page,textvariable=face_id,font = ('', round((sheight/22-8)*3/4))).place(x = swidth*3/100, y = sheight*12.5/100, width = swidth*37/100, height = sheight*8/100)
tk.Button(manage_page, text = '更新人脸数据', font = ('', round((sheight/25-8)*3/4)), command = lambda:inputFace(face_id.get())).place(x = swidth*37/100, y = sheight*12.5/100, width = swidth*13/100, height = sheight*8/100)
tk.Label(manage_page, text = '               '+'学号'+'              '+'|    '+'姓名    ', font = ('', round((sheight/25-8)*3/4)),anchor = W).place(x = swidth*53/100, y = sheight*12.5/100, width = swidth*44/100, height = sheight*8/100)
#
list_box=Listbox(manage_page,font = ('', round((sheight/25-8)*3/4)))
list_box.place(x = swidth*53/100, y = sheight*19/100, width = swidth*42/100,height = sheight*56/100)
#竖直滚动条
vbar=Scrollbar(manage_page)
vbar.place(x = swidth*95/100, width = swidth*2/100, y = sheight*19/100, heigh = sheight*56/100)
#绑定
list_box.configure(yscrollcommand = vbar.set)
vbar.configure(command=list_box.yview)

tk.Label(manage_page, text = '学号', font = ('', round((sheight/22-8)*3/4))).place(x = swidth*53/100, width = swidth*5/100, y = sheight*75.5/100, height = sheight*6/100)
tk.Entry(manage_page, textvariable=input_id, font = ('', round((sheight/22-8)*3/4))).place(x = swidth*58/100, width = swidth*22/100, y = sheight*75.5/100, height = sheight*6/100)
tk.Label(manage_page,text = '姓名', font = ('', round((sheight/22-8)*3/4))).place(x = swidth*53/100, width = swidth*5/100, y = sheight*81.5/100, height = sheight*6/100)
tk.Entry(manage_page, textvariable=input_name, font = ('', round((sheight/22-8)*3/4))).place(x = swidth*58/100, width = swidth*22/100, y = sheight*81.5/100, height = sheight*6/100)
tk.Button(manage_page, text = '添加', command = add_stu, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*77/100, y = sheight*75.5/100, width = swidth*10/100, height = sheight*12/100)
tk.Button(manage_page, text = '删除', command = del_stu, font = ('', round((sheight/25-8)*3/4))).place(x = swidth*87/100, y = sheight*75.5/100, width = swidth*10/100, height = sheight*12/100)

update_list()#显示信息









#执行程序

#initialize()

try:
    discerner = FaceRecognition.FaceRecognition(main_page, x = swidth*3/100, y = sheight*7/32, w = swidth*15/32, h = sheight*21/32)
except Exception as e:
    text_time.config(text=e)

update_time()

main_page.mainloop()