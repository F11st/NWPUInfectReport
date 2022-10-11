from requests.sessions import Session
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from lxml import etree
import base64
import re
from pusher import pusher


class XgdYqtb(object):
    def __init__(self):
        self.wx_login_url = 'https://wxapp.nwpu.edu.cn/uc/wap/login/check'
        self.wx_redirect_url = 'https://wxapp.nwpu.edu.cn/uc/api/oauth/index?redirect=https://yqtb.nwpu.edu.cn/wx/common/metaWeiXin_new.jsp&appid=200200204192458714&state=1'
        self.yqtb_url = 'https://yqtb.nwpu.edu.cn/wx/ry/jrsb_xs.jsp'
        self.yqtb_index_url = 'https://yqtb.nwpu.edu.cn//wx/xg/yz-mobile/index.jsp'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36 Edg/106.0.1370.37'
        }
        
        self.session = Session()
        self.username = None

    def login(self, username, password):
        self.username = username
        self.session.post(self.wx_login_url, data={
            'username': username,
            'password': password
        })

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
            'szcsmc1': data['gwcs'],
            'sfyzz': data['sfyzz'],
            'sfqz': data['sfqz'],
            'tbly': data['tbly'],
            'qtqksm': data['qtqksm'],
            'ycqksm': data['ycqksm'],
            'sfxn': data['sfxn'],
            'sfdw': data['sfdw'],
            'longlat': data['longlat'],
            'userType': data['userType'],
            'userName': data['userName'],
        }

    def get_submit_info_once(self):
        res = self.session.get(self.wx_redirect_url)
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
            script_text = res_tree.xpath('/html/body/script')[6].text

            submit_url_prefix = 'https://yqtb.nwpu.edu.cn/wx/ry/'
            try:
                data['submit_url'] = submit_url_prefix + \
                    re.search(r'ry_util\.jsp[^\']+', script_text).group(0)
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
            raise RuntimeError('调用失败')
