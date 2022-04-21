from requests.sessions import Session
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from lxml import etree
import base64
import re
from pusher import pusher


class XgdYqtb(object):
    def __init__(self):
        self.session = None
        self.cas_url = 'https://uis.nwpu.edu.cn/cas/login?service=http%3A%2F%2Fyqtb.nwpu.edu.cn%2F%2Fsso%2Flogin.jsp%3FtargetUrl%3Dbase64aHR0cHM6Ly95cXRiLm53cHUuZWR1LmNuLy93eC94Zy95ei1tb2JpbGUvaW5kZXguanNw'
        self.yqtb_url = 'https://yqtb.nwpu.edu.cn/wx/ry/jrsb_xs.jsp'
        self.yqtb_index_url = 'https://yqtb.nwpu.edu.cn//wx/xg/yz-mobile/index.jsp'
        self.public_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBQw6TmvJ+nOuRaLoHsZJGIBzRg/wbskNv6UevL3/nQioYooptPfdIHVzPiKRVT5+DW5+nqzav3DOxY+HYKjO9nFjYdj0sgvRae6iVpa5Ji1wbDKOvwIDNukgnKbqvFXX2Isfl0RxeN3uEKdjeFGGFdr38I3ADCNKFNxtbmfqvjQIDAQAB
-----END PUBLIC KEY-----'''
        self.username = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
        }

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
        }, headers=self.headers)

    def get_save_data(self, data):
        return {
            'hsjc': data['hsjc'],
            'sfczbcqca': data['sfczbcqca'],
            'czbcqcasjd': data['czbcqcasjd'],
            'sfczbcfhyy': data['sfczbcfhyy'],
            'czbcfhyysjd': data['czbcfhyysjd'],
            'actionType': data['actionType'],
            'userLoginId': data['userLoginId'],
            'szcsbm': data['csbm'] if data['szcsbm'] == '3' else data['szcsbm'],
            'szcsmc': data['gwcs'],
            'sfjt': data['sfjt'],
            'sfjtsm': data['sfjtsm'],
            'sfjcry': data['sfjcry'],
            'sfjcrysm': data['sfjcrysm'],
            'sfjcqz': data['sfjcqz'],
            'sfyzz': data['sfyzz'],
            'sfqz': data['sfqz'],
            'ycqksm': data['ycqksm'],
            'glqk': data['glqk'],
            'glksrq': data['glksrq'],
            'gljsrq': data['gljsrq'],
            'tbly': data['tbly'],
            'glyy': data['glyy'],
            'qtqksm': data['qtqksm'],
            'sfjcqzsm': data['sfjcqzsm'],
            'sfjkqk': data['sfjkqk'],
            'jkqksm': data['jkqksm'],
            'sfmtbg': data['sfmtbg'],
            'userType': data['userType'],
            'userName': data['userName'],
            'qrlxzt': data['qrlxzt'],
            'bdzt': data['bdzt'],
            'xymc': data['xymc'],
            'xssjhm': data['xssjhm']
        }

    def get_savefx_data(self, data):
        return {
            'hsjc': data['hsjc'],
            'xasymt': data['xasymt'],
            'actionType': data['actionType'],
            'userLoginId': data['userLoginId'],
            'szcsbm': data['csbm'] if data['szcsbm'] == '3' else data['szcsbm'],
            'bdzt': data['bdzt'],
            'szcsmc': data['gwcs'],
            'sfyzz': data['sfyzz'],
            'sfqz': data['sfqz'],
            'tbly': data['tbly'],
            'qtqksm': data['qtqksm'],
            'ycqksm': data['ycqksm'],
            'userType': data['userType'],
            'userName': data['userName'],
        }

    def get_submit_info_once(self):
        self.session.get(self.yqtb_index_url)
        res = self.session.get(self.yqtb_url)
        res_tree = etree.HTML(res.text)

        data = {}
        try:
            data_from_html = {
                'hsjc': '1',
                'sfczbcqca': '',
                'czbcqcasjd': '',
                'sfczbcfhyy': '',
                'czbcfhyysjd': '',
                'sfmtbg': '',
            }
            script_text = res_tree.xpath('/html/body/script[2]')[0].text

            submit_url_prefix = 'https://yqtb.nwpu.edu.cn/wx/ry/'
            try:
                data['submit_url'] = submit_url_prefix + \
                    re.search(r'ry_util[^\']+', script_text).group(0)
            except:
                data['res'] = '提交链接消失了？？？'
                return data

            data_from_html['userType'], data_from_html['userName'], data_from_html['qrlxzt'], data_from_html['bdzt'], data_from_html['xymc'], data_from_html['xssjhm'] = re.search(
                r"userType:'([^']*)',userName:'([^']*)',qrlxzt:'([^']*)',bdzt:'([^']*)',xymc:'([^']*)',xssjhm:'([^']*)'", script_text).groups()
            try:
                data_from_html['csbm'] = re.search(
                    r'select\("(\d+)"\);\s+\}', script_text, re.S).group(1)
            except:
                data_from_html['csbm'] = ''

            cast_table = {
                'sfjthb_ms': 'sfjtsm',
                'hbjry_ms': 'sfjcrysm',
                'ycqk_ms': 'ycqksm',
                'jkqk_ms': 'jkqksm',
                'radio2': 'sfjt',
                'radio3': 'sfjcry',
                'radio4': 'sfjcqz',
                'radio5': 'sfyzz',
                'radio6': 'sfqz',
                'radio7': 'glqk',
                'radio8': 'sfjkqk',
                'radio11': 'xasymt',
            }
            info_loc = res_tree.xpath(
                "//textarea|//input[@type='radio' and @checked]|//input[@type='checkbox'][@checked]|//input[@type!='radio' and @type!='checkbox']")
            for ele in info_loc:
                attr = ele.attrib
                try:
                    key = cast_table[attr['name']]
                except:
                    key = attr['name']
                if ele.tag == 'textarea':
                    if ele.text == None:
                        data_from_html[key] = ''
                    else:
                        data_from_html[key] = ele.text
                else:
                    data_from_html[key] = attr['value']

            sub_cate = res_tree.xpath("//*[@id='save_div']")[0].attrib['href']
            submit_data = {}
            if sub_cate == 'javascript:save()':
                submit_data = self.get_save_data(data_from_html)
            else:
                submit_data = self.get_savefx_data(data_from_html)
            data['submit_data'] = submit_data
            data['res'] = 'success'

        except Exception as e:
            data['res'] = "获取信息失败，可能需要手动签到一次:"+e
        return data

    def checkin(self):
        info = self.get_submit_info_once()
        if info['res'] == 'success':
            res = self.session.post(info['submit_url'], data=info['submit_data'],
                                    headers={'referer': self.yqtb_url})
            pusher(res.text.strip())
        else:
            pusher(info['res'])
