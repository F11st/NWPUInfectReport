from requests.sessions import Session
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from bs4 import BeautifulSoup
import base64
import os
try:
    from pusher import pusher
except:
    pass

class XgdYqtb:
    def __init__(self):
        self.session = None
        self.casUrl = 'https://uis.nwpu.edu.cn/cas/login?service=http%3A%2F%2Fyqtb.nwpu.edu.cn%2F%2Fsso%2Flogin.jsp%3FtargetUrl%3Dbase64aHR0cDovL3lxdGIubndwdS5lZHUuY24vL3d4L3hnL3l6LW1vYmlsZS9pbmRleC5qc3A%3D'
        self.yqtbUrl = 'http://yqtb.nwpu.edu.cn/wx/ry/ry_util.jsp'
        self.publicKey = '''-----BEGIN PUBLIC KEY-----
         MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBQw6TmvJ+nOuRaLoHsZJGIBzRg/wbskNv6UevL3/nQioYooptPfdIHVzPiKRVT5+DW5+nqzav3DOxY+HYKjO9nFjYdj0sgvRae6iVpa5Ji1wbDKOvwIDNukgnKbqvFXX2Isfl0RxeN3uEKdjeFGGFdr38I3ADCNKFNxtbmfqvjQIDAQAB
         -----END PUBLIC KEY-----'''
        
        self.username = None
        self.personalName = None

    def encryptPassword(self, ciper):
        recipient_key = RSA.import_key(self.publicKey)
        cipher_rsa = PKCS1_v1_5.new(recipient_key)
        enc_ciper = base64.b64encode(cipher_rsa.encrypt(ciper.encode()))
        return "__RSA__"+enc_ciper.decode()

    def getSession(self):
        self.session = Session()
        return self.session

    def login(self, username, password):
        self.username = username
        self.session.get(self.casUrl)
        self.session.post(self.casUrl, data={
            'username': username,
            'password': self.encryptPassword(password),
            'currentMenu': '1',
            'execution': 'e1s1',
            '_eventId': 'submit'
        })
        # 获取个人信息
        infoRes = self.session.get('http://yqtb.nwpu.edu.cn/wx/ry/jbxx_v.jsp')
        soup = BeautifulSoup(infoRes.text, 'lxml')
        self.personalName = soup.select('#form1 > div:nth-child(5) > div:nth-child(2) > span')[0].text
        

    def checkin(self):
        res = self.session.post(self.yqtbUrl, data={
            'xasymt': '1',
            'actionType': 'addRbxx',
            'userLoginId': self.username,
            'szcsbm': '1',
            'sfyzz': '0',
            'sfqz': '0',
            'tbly': 'sso',
            'qtqksm': '',
            'ycqksm': '',
            'userType': '2',
            'szcsmc': '在学校',
            'userName': self.personalName,
            'bdzt': '1'
        }, headers={'referer': 'http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp'})
        pusher(res.text)


xgd_username = os.environ.get('xgd_username')
xgd_password = os.environ.get('xgd_password')

yq = XgdYqtb()
yq.getSession()
yq.login(xgd_username, xgd_password)
yq.checkin()
