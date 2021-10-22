from requests.sessions import Session
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from lxml import etree
import base64
import re
import json
from pusher import pusher


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
        self.get_session()

    def encrypt_password(self, plain):
        recipient_key = serialization.load_pem_public_key(
            self.public_key.encode())
        cipher = recipient_key.encrypt(
            plain.encode(),
            padding.PKCS1v15()
        )
        base_ciper = base64.b64encode(cipher).decode()
        return '__RSA__'+base_ciper

    def get_session(self):
        self.session = Session()
        return self.session

    def login(self, username, password):
        self.username = username
        self.session.get(self.cas_url)
        self.session.post(self.cas_url, data={
            'username': username,
            'password': self.encrypt_password(password),
            'currentMenu': '1',
            'execution': 'e1s1',
            '_eventId': 'submit'
        })

    def get_csbm(self, cs):
        csbm = ''
        # 转data.js内容为python dict,区划代码字典
        res = self.session.get(
            'http://yqtb.nwpu.edu.cn/wx/js/eams.area.data.js')
        region_data_re = re.compile(r'var placesMap=(?P<addr>.*) ;')
        region_dict = region_data_re.match(res.text).group('addr')
        region_dict = json.loads(region_dict)
        # 根据正则切割连续字符串，填报系统总是三段信息组成
        fullname_re = re.compile(
            r'^(?P<province>.+?自治区|.+?省|.+?行政区|.+?市)\s*(?P<city>市辖区|县|.+?市|.+?盟|.+?自治州|.+?地区|.+?行政区|.+?直辖县级行政区划|.+?省)\s*(?P<county>.+县|.+区|.+市|.+旗|.+海域|.+省|.+行政区|.+岛)?')
        try:
            re_result = fullname_re.match(cs)
        except Exception as e:
            print("城市匹配失败", cs, e)
            return csbm

        provice = re_result.group('province')
        city = re_result.group('city')
        county = re_result.group('county')

        provice_code_list = []
        city_code_list = []
        county_code_list = []
        for code, addr in region_dict.items():
            if county != None and county == addr:
                county_code_list.append(code)
            elif city != None and city == addr and int(code) % 100 == 0:
                city_code_list.append(code)
            elif provice != None and provice == addr and int(code) % 10000 == 0:
                provice_code_list.append(code)

        if len(provice_code_list) != 1:
            return csbm
        csbm = provice_code_list[0]
        for city_code in city_code_list:
            if int(int(city_code)/10000)*10000 == int(csbm):
                csbm = city_code
        for county_code in county_code_list:
            if int(int(county_code)/100)*100 == int(csbm):
                csbm = county_code
        return csbm

    def init_info(self):
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
            csbm = self.get_csbm(self.info['家庭地址'])
            # print("获取csdm成功")
            if csbm:
                self.info['csbm'] = csbm
            # print(self.info)
        except Exception as e:
            print("获取个人信息失败", e)

    def get_personal_info(self, skey):
        if len(self.info) == 0:
            self.init_info()
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
