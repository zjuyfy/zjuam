import requests
from urllib.parse import quote
import re

def rsa_encrypt(passwd:str, e_hex:str, n_hex:str):
    pwd = 0
    for c in passwd:
        pwd = pwd * 256 + ord(c)
    n = int(n_hex, 16)
    e = int(e_hex,16)
    crypt = pow(pwd,e,n)
    ciphertext_hex = hex(crypt)[2:]
    return ciphertext_hex


class login:
    def __init__(self, username:str, password:str,service:str):
        url = 'https://zjuam.zju.edu.cn/cas/login?service='+quote(service)
        pubkey_url = 'https://zjuam.zju.edu.cn/cas/v2/getPubKey'
        self.session = requests.session()
        res = self.session.get(url)
        execution = re.findall(r"(?<=name=\"execution\" value=\").*(?=\")",res.text)[0]
        pubkey = self.session.get(pubkey_url)
        modulus = pubkey.json()["modulus"]
        exponent = pubkey.json()["exponent"]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }
        encrypted_password = rsa_encrypt(password, exponent, modulus)

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