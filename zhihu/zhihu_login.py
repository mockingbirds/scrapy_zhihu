# -*- coding: utf-8 -*-

import requests
from http import cookiejar
from bs4 import BeautifulSoup
import time

session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print ("cookie未能加载")


header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
    'Host': 'www.zhihu.com',
    "Referer": "https://www.zhihu.com/",
}

def get_xsrf():
    response = session.get('https://www.zhihu.com', headers=header)
    soup = BeautifulSoup(response.text)
    crsf = soup.select('input[name="_xsrf"]')[0]['value']
    print(soup.select('input[name="_xsrf"]')[0]['value'])
    return crsf

def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    print(captcha_url)
    response = session.get(captcha_url, headers=header)
    with open('captcha.gif', 'wb') as f:
        f.write(response.content)
        f.close()
    from PIL import Image
    try:
        im = Image.open('captcha.gif')
        im.show()
        im.close()
    except:
        pass

    captcha = input('请输入验证码: ')
    return captcha

def is_login():
    inbox_url = 'https://www.zhihu.com/inbox'
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code == 200:
        print('登录成功')
    else:
        print('登录失败')


def zhihu_login(username, passwd):
    login_url = 'https://www.zhihu.com/login/phone_num'
    login_data = {
        '_xsrf': get_xsrf(),
        'phone_num': username,
        'password': passwd,
        'captcha': get_captcha()
    }
    response = session.post(login_url, data=login_data, headers=header)
    print(response.text)
    session.cookies.save() # 保存cookie



# get_captcha()
# get_xsrf()
# zhihu_login('手机号码','密码')
is_login()