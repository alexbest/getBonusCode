import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get(url):
    headers = {'cache-control': 'no-cache'}
    response = requests.request("GET", url, headers=headers)
    return response


def post(url, payload='{}', cookie=None):
    if cookie is None:
        cookie = {}
    payload = payload
    ck = ''
    for k, v in cookie.items():
        ck += k + '=' + str(v) + ';'
    headers = {
        'pragma': "no-cache",
        'cookie': ck,
        'origin': "https://console.bonuscloud.io",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'content-type': "application/json;charset=UTF-8",
        'accept': "application/json, text/plain, */*",
        'cache-control': "no-cache",
        'authority': "console.bonuscloud.io",
        'referer': "https://console.bonuscloud.io/"
    }
    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    # print(response.text)
    return response


def download(url, headers=None, file_name=''):
    response = requests.get(url, headers=headers, verify=False)
    with open(file_name, "wb") as code:
        code.write(response.content)
    return response
