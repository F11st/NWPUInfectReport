from requests.sessions import Session
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from lxml import etree
import os
import re
try:
    from pusher import pusher
except:
    pass


class XgdYqtb(object):
    def __init__(self):
        self.session = None
        self.cas_url = 'https://uis.nwpu.edu.cn/cas/login?service=http%3A%2F%2Fyqtb.nwpu.edu.cn%2F%2Fsso%2Flogin.jsp%3FtargetUrl%3Dbase64aHR0cDovL3lxdGIubndwdS5lZHUuY24vL3d4L3hnL3l6LW1vYmlsZS9pbmRleC5qc3A%3D'
        self.yqtb_url = 'http://yqtb.nwpu.edu.cn/wx/ry/ry_util.jsp'
        self.public_key = '''-----BEGIN PUBLIC KEY-----
         MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBQw6TmvJ+nOuRaLoHsZJGIBzRg/wbskNv6UevL3/nQioYooptPfdIHVzPiKRVT5+DW5+nqzav3DOxY+HYKjO9nFjYdj0sgvRae6iVpa5Ji1wbDKOvwIDNukgnKbqvFXX2Isfl0RxeN3uEKdjeFGGFdr38I3ADCNKFNxtbmfqvjQIDAQAB
         -----END PUBLIC KEY-----'''
        self.username = None

        self.info = {}

    def encrypt_password(self, ciper):
        recipient_key = RSA.import_key(self.public_key)
        cipher_rsa = PKCS1_v1_5.new(recipient_key)
        enc_ciper = base64.b64encode(cipher_rsa.encrypt(ciper.encode()))
        return "__RSA__"+enc_ciper.decode()

    def get_session(self):
        self.session = Session()
        return self.session

    def login(self, username, password):
        if self.session == None:
            self.get_session()
        self.username = username
        self.session.get(self.cas_url)
        self.session.post(self.cas_url, data={
            'username': username,
            'password': self.encrypt_password(password),
            'currentMenu': '1',
            'execution': 'e1s1',
            '_eventId': 'submit'
        })

    def get_personal_info(self, skey):
        def init_info():
            def get_csbm(cs):
                res = self.session.get(
                    'http://yqtb.nwpu.edu.cn/wx/js/eams.area.data.js')
                match = re.search('"([0-9]+)":"'+cs+'"', res.text, re.M)
                try:
                    return match.group(1)
                except Exception as e:
                    print("城市匹配失败", cs, e)
                    return ''
            res = self.session.get(
                'http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/userInfo.jsp')
            res_tree = etree.HTML(res.text)
            try:
                info_cell = res_tree.xpath('//div[@class="weui-cell"]')
                for item in info_cell:
                    cell_key = item.xpath(
                        './/div[@class="weui-cell__bd"]/p/text()')[0]
                    value_xpath = item.xpath(
                        './/div[@class="weui-cell__ft"]/text()')
                    if len(value_xpath) == 0:
                        cell_value = ''
                    else:
                        cell_value = value_xpath[0]
                    self.info[cell_key] = cell_value
                self.info['csbm'] = get_csbm(self.info['家庭地址'].split()[-1])
                # print(self.info)
            except Exception as e:
                print("获取个人信息失败", e)
        if len(self.info) == 0:
            init_info()
        if skey in self.info:
            return self.info[skey]
        return ''

    def checkin(self, user_status):
        szcsmc = ''
        szcsbm = ''
        if user_status == '1':
            szcsmc = '在学校'
            szcsbm = '1'
        elif user_status == '2':
            szcsmc = self.get_personal_info('家庭地址').replace(' ', '')
            szcsbm = self.get_personal_info('csbm')
        data = {
            'actionType': 'addRbxx',
            'userLoginId': self.username,
            'sfjt': '0',
            'sfjcry': '0',
            'sfjcqz': '0',
            'sfjkqk': '0',
            'sfyzz': '0',
            'sfqz': '0',
            'glqk': '0',
            'tbly': 'sso',
            'userType': '2',
            'userName': self.get_personal_info('姓名'),
            'bdzt': '1',
            'xymc': self.get_personal_info('学院/大类'),
            'xssjhm': self.get_personal_info('手机号码'),
            'szcsmc': szcsmc,
            'szcsbm': szcsbm
        }
        # print(data)
        res = self.session.post(self.yqtb_url, data=data,
                                headers={'referer': 'http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp'})
        pusher(res.text.strip())


xgd_username = os.environ.get('xgd_username')
xgd_password = os.environ.get('xgd_password')
user_status = os.environ.get('user_status')

yq = XgdYqtb()
yq.login(xgd_username, xgd_password)
yq.checkin(user_status)
