import json

from config import *
from date_utils import *
from http_utils import *
from rk import RClient


class Bcode(object):
    cookies = {}
    bcUser = ''
    bcPass = ''

    def __init__(self, username, password):
        self.bcUser = username
        self.bcPass = password

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
                print("登录成功")
                self.cookies.update(response.cookies.items())
                return True
        return False

    def get_captcha(self):
        url = "https://console.bonuscloud.io/api/web/captcha/get/"
        png_file = "cap_" + self.bcUser + "_" + str(get_now_time()) + ".png"
        response = download(url, file_name=png_file)
        print(dict(response.cookies.items()))
        rc = RClient(RUO_KUAI_USER, RUO_KUAI_PASSWORD, RUO_KUAI_SOFT_ID, RUO_KUAI_SOFT_KEY)
        im = open(png_file, 'rb').read()
        rc_result = rc.rk_create(im, 3060)
        # print(rc_result)
        if 'Result' in rc_result:
            code = rc_result['Result']
        else:
            return None, None
        print('验证码为：', code)
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
                print("抢码成功")
                return True
        if 'message' in data:
            message = data['message']
            if 'maximum in this time period' in message:
                print('该时段已抢购成功')
                return True
            elif 'next time' in message:
                print('该时段已抢完')
                return True
            elif 'captcha error' in message:
                print('验证码有误')
                return False
            else:
                print(data['message'])
        return False

    def start(self):
        if self.login():
            while True:
                while True:
                    now_time = get_now_time()
                    start_time = get_timestamp(format_time(now_time)) + 60 * 60
                    delta = start_time - now_time
                    if delta <= 0:
                        break
                    if delta < 10:
                        time.sleep(delta + 0.2)
                        break
                    print(str(delta) + ' 秒后开始抢码')
                    time.sleep(10)
                print('开始抢码')
                i = 1
                while i < 10:
                    print('第' + str(i) + '次')
                    i += 1
                    code, cookie = self.get_captcha()
                    if code is not None:
                        if self.get_bcode(code, cookie):
                            break
        else:
            print('登录失败')
