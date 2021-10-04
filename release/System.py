import re
import os
import json
import pygame
import requests

import _thread

import GUI
import FaceRecognition


class System:

    path = None

    data = None

    sounds = None

    cookie = None

    discerner = None
    
    main_page = None

    check_page = None

    manage_page = None

    def __init__(self, cameraWidth=0, cameraHeight=0, threshold=45, fps=25):

        self.path = os.path.dirname(os.path.abspath(__file__))

        path = os.path.join(self.path,'data.json')

        if os.path.exists(path):
            with open(path,'r') as f:
                self.data = json.load(f)
        else:
            self.data = []

        path = os.path.join(self.path, 'sound')

        self.sounds = {
            '暂无考勤！': os.path.join(path, 'no_attendance.mp3'),
            '签到成功！': os.path.join(path, 'checkin_success.mp3'),
            '签退成功！': os.path.join(path, 'checkout_success.mp3'),
            '早退！':     os.path.join(path, 'checkout_early.mp3'),
            '迟到！':     os.path.join(path, 'checkin_late.mp3'),
            '录入提示':   os.path.join(path, 'start_enter.mp3'),
            '录入成功':   os.path.join(path, 'enter_success.mp3'),
            '录入失败':   os.path.join(path, 'input _failed.mp3')
        }

        pygame.mixer.init(frequency = 16000)

        self.main_page = GUI.MainPage(self)   

        self.manage_page = GUI.ManagePage(self, self.main_page) 

        self.check_page = GUI.CheckPage(self, self.main_page)

        def init():
            width = self.main_page.width
            height = self.main_page.height
            self.discerner = FaceRecognition.FaceRecognition(self.path, self.main_page,
                width*3//100, height*22//100, width*47//100, height*65//100, 
                cameraWidth = cameraWidth, cameraHeight = cameraHeight,threshold = threshold, fps = fps)

        _thread.start_new_thread(init, ())



    def playSound(self, msg):
        pygame.mixer.music.load(self.sounds[msg])
        pygame.mixer.music.play()


    def signIn(self, uid):
        self.playSound('签到成功！')
        return (0, '签到成功！')

        # js = requests.get('http://139.224.16.208:8081/api/signIn?uid=' + uid).json()
        # if js['code'] == 200:
        #     self.playSound(js['msg'])
        #     return (0, js['msg'])
        # return (1, js['msg'])


    def addUser(self, uid, name):
        
        return None

        # js = requests.post(
        #     url = 'http://139.224.16.208:8081/api/userRegister',
        #     data = {
        #         'name': name,
        #         'uid': uid,
        #         'password': 123456,
        #         'conformPassword': 123456
        #     }
        # ).json()

        # if js['code'] == 200:
        #     return None
        # else:
        #     return js['msg']


    def login(self, uid, password):
        if uid == 0 and password == '123456':
            return (0, '登陆成功！')
        else:
            return (1, '登陆失败！')
        # response = requests.get('http://139.224.16.208:8081/index.jsp')
        # self.cookie = re.findall(r'JSESSIONID=(.*?);', response.headers['Set-Cookie'])[0]

        # js = requests.post(
        #     url = 'http://139.224.16.208:8081/api/userLogin',
        #     cookies = {
        #         'JSESSIONID': self.cookie
        #     },
        #     data = {
        #         'name': uid,
        #         'password': password
        #     }
        # ).json()

        # if js['code'] == 200:

        #     path = os.path.join(self.path,'data.json')

        #     js = requests.get(
        #         url = 'http://139.224.16.208:8081/master/getUsers',
        #         cookies = {
        #             'JSESSIONID': self.cookie
        #         },
        #     ).json()

        #     if js['code'] == 200:

        #         self.data = dict()

        #         for user in js['data']['users']:
        #             self.data[str(user['uid'])] = user

        #         with open(path,'w') as f:
        #             f.write(json.dumps(self.data))
        #     else:
                
        #         self.data = []

        #         print(js['msg'])

        #     return (0, js['msg'])
        # else:
        #     self.cookie = None
        #     return (1, js['msg'])