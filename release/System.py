import re
import os
import json
import requests

from playsound import playsound


class System:

    path = None

    data = None

    sounds = None

    cookie = None

    def __init__(self):
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


    def playSound(self, msg):
        playsound(self.sounds[msg], False)


    def signIn(self, uid):
        js = requests.get('http://139.224.16.208:8081/api/signIn?uid=' + uid).json()

        if js['code'] == 200:
            self.playSound(js['msg'])
            return (0, js['msg'])
        return (1, js['msg'])


    def addUser(self, uid, name):
        js = requests.post(
            url = 'http://139.224.16.208:8081/api/userRegister',
            data = {
                'name': name,
                'uid': uid,
                'password': 123456,
                'conformPassword': 123456
            }
        ).json()

        if js['code'] == 200:
            return None
        else:
            return js['msg']



    def login(self, uid, password):

        response = requests.get('http://139.224.16.208:8081/index.jsp')
        self.cookie = re.findall(r'JSESSIONID=(.*?);', response.headers['Set-Cookie'])[0]

        js = requests.post(
            url = 'http://139.224.16.208:8081/api/userLogin',
            cookies = {
                'JSESSIONID': self.cookie
            },
            data = {
                'name': uid,
                'password': password
            }
        ).json()

        if js['code'] == 200:

            path = os.path.join(self.path,'data.json')

            js = requests.get(
                url = 'http://139.224.16.208:8081/master/getUsers',
                cookies = {
                    'JSESSIONID': self.cookie
                },
            ).json()

            if js['code'] == 200:

                self.data = dict()

                for user in js['data']['users']:
                    self.data[str(user['uid'])] = user

                with open(path,'w') as f:
                    f.write(json.dumps(self.data))
            else:
                
                self.data = []

                print(js['msg'])

            return (0, js['msg'])
        else:
            self.cookie = None
            return (1, js['msg'])