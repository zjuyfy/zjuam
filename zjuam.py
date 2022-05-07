import requests
from jscode import jscode
import execjs
import re
from bs4 import BeautifulSoup


def printhtml(content, n):
    with open(f"temp{n}.html", mode="w") as f:
        f.write(content)


class login:
    def __init__(self, username, password):
        url = 'https://zjuam.zju.edu.cn/cas/login'
        get_pubkey_url = 'https://zjuam.zju.edu.cn/cas/v2/getPubKey'
        self.session = requests.session()
        res1 = self.session.get(url)
        soup = BeautifulSoup(res1.text, "html.parser")
        execution = soup.find("input", attrs={'name': 'execution'})['value']
        pubkey = self.session.get(get_pubkey_url)
        modulus = pubkey.json()["modulus"]
        exponent = pubkey.json()["exponent"]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }

        ctx = execjs.compile(jscode)
        encrypted_password = ctx.call('encrypt', modulus, exponent, password)

        data = {
            'username': username,
            'password': encrypted_password,
            '_eventId': 'submit',
            'execution': execution,
            'authcode': '',
        }
        self.session.headers = headers
        res_login = self.session.post(url, data=data)
        self.content=res_login.text
        self.logger()
    def logger(self):
        if "用户名或密码错误" in self.content:
            print("用户名或密码错误")