import json

from config import *
from date_utils import *
from http_utils import *
from rk import RClient
import os


class Bcode(object):
    cookies = {}
    bcUser = ''
    bcPass = ''

    def __init__(self, username, password):
        self.bcUser = username
        self.bcPass = password

    def mkdir(self, path):
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    def login(self):
        if self.bcUser == '' or self.bcPass == '' or RUO_KUAI_USER == '' or RUO_KUAI_PASSWORD == '':
            return False
        payload = {
            'email': BONUS_CLOUD_USER,
            'password': BONUS_CLOUD_PASSWORD
        }
        response = post('https://console.bonuscloud.io/api/user/login/', json.dumps(payload))
        data = response.json()
        if 'code' in data:
            if data['code'] == 200:
                print("login success")
                self.cookies.update(response.cookies.items())
                return True
        return False

    def get_captcha(self):
        url = "https://console.bonuscloud.io/api/web/captcha/get/"
        self.mkdir('img')
        png_file = "img/cap_" + self.bcUser + "_" + str(get_now_time()) + ".png"
        header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        response = download(url, headers=header, file_name=png_file)
        rc = RClient(RUO_KUAI_USER, RUO_KUAI_PASSWORD, RUO_KUAI_SOFT_ID, RUO_KUAI_SOFT_KEY)
        im = open(png_file, 'rb').read()
        rc_result = rc.rk_create(im, 3060)
        if 'Result' in rc_result:
            code = rc_result['Result']
        else:
            print(rc_result)
            return None, None
        print('code：', code)
        return code, dict(response.cookies.items())

    def get_bcode(self, code, cookie):
        url = "https://console.bonuscloud.io/api/bcode/get/"
        payload = "{\"captcha\":\"" + code + "\"}"
        self.cookies.update(cookie)
        response = post(url, payload, self.cookies)
        data = json.loads(response.text)
        if 'code' in data:
            code = data['code']
            if code == 200:
                print("get bcode success")
                return True
        if 'message' in data:
            message = data['message']
            if 'maximum in this time period' in message:
                print('successed')
                return True
            elif 'next time' in message:
                print('no code')
                return True
            elif 'captcha error' in message:
                print('captcha error')
                return False
            else:
                print(data['message'])
        return False

    def start(self):
        if self.login():
            print('testing')
            code, cookie = self.get_captcha()
            while True:
                code = None
                cookie = None
                while True:
                    now_time = get_now_time()
                    start_time = get_timestamp(format_time(now_time)) + 60 * 60
                    delta = start_time - now_time
                    if delta <= 50 and code is None:
                        print("getting code")
                        code, cookie = self.get_captcha(start_time + 1)
                        continue
                    if delta <= 0:
                        break
                    if delta <= 15:
                        time.sleep(delta + 0.2)
                        break

                    print(str(delta) + ' s')
                    time.sleep(10)
                print('getting')
                i = 1
                while i < 10:
                    print('times:' + str(i))
                    i += 1
                    if code is not None:
                        if self.get_bcode(code, cookie):
                            break
                    code, cookie = self.get_captcha()
        else:
            print('login failed')
