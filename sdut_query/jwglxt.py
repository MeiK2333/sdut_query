# coding=utf-8
import rsa
import json
import base64
import requests
from bs4 import BeautifulSoup


class Jwglxt(object):
    """ 教务管理系统（他们官方就叫jwglxt...） """

    def __init__(self):
        self.session = requests.session()
        self.exponent = ''
        self.modulus = ''

    def get_public_key(self):
        """ 获取加密公钥 """
        url = 'http://211.64.28.123/jwglxt/xtgl/login_getPublicKey.html'
        rst = self.session.get(url)
        rjson = json.loads(rst.text)
        self.exponent = rjson['exponent']
        self.modulus = rjson['modulus']

    def get_csrf(self):
        """ 获取 csrf 防跨站参数 """
        url = 'http://211.64.28.123/jwglxt/xtgl/login_slogin.html'
        rst = self.session.get(url)
        soup = BeautifulSoup(rst.text, 'html.parser')
        ipts = soup.form.find_all('input')
        data = {}
        for ipt in ipts:
            if ipt.get('value'):
                data[ipt.get('name')] = ipt.get('value')
        return data['csrftoken']

    def login(self, username, password):
        """ 登录 """
        csrf_token = self.get_csrf()
        self.get_public_key()
        n = base64_to_hex(self.modulus)
        e = base64_to_hex(self.exponent)
        public_key = rsa.PublicKey(int(n, 16), int(e, 16))
        rsa_k = rsa.encrypt(bytes(password, encoding='utf-8'), public_key)
        final_k = str(hex_to_base64(rsa_k))[2:-1]
        data = {
            'csrftoken': csrf_token,
            'yhm': username,
            'mm': final_k
        }
        rst = self.session.post('http://211.64.28.123/jwglxt/xtgl/login_slogin.html', data=data)
        if 'http://211.64.28.123/jwglxt/xtgl/index_initMenu.html' in rst.url:
            return True
        return False

    def logout(self):
        """ 退出登录 """
        url = 'http://211.64.28.123/jwglxt/logout'
        self.session.get(url)

    def get_schedule(self, year=-1, semester=-1, parse=True):
        """ 获得个人课表 """
        # 若不填写年份与学期，则按照默认的查询（最近要上的课表）
        url = 'http://211.64.28.123/jwglxt/xkcx/xkmdcx_cxXkmdcxIndex.html?doType=query'
        data = {
            'queryModel.showCount': '100',  # 要是有哪位同学一个学期的课程超过一百门...那就节哀吧
            'queryModel.currentPage': '1',
            'time': '0',
        }
        if year != -1:
            data['xnm'] = str(year)
        if semester != -1:
            if semester == 1:
                data['xqm'] = '3'
            elif semester == 2:
                data['xqm'] = '12'
        rst = self.session.post(url, data=data)
        rjson = json.loads(rst.text)
        if parse:  # 若指定信息 parse，则解析数据
            rdata_list = []
            for i in rjson['items']:
                d = {
                    '学年': i.get('xnmc', ''),
                    '学期': i.get('xqmc', ''),
                    '课程代码': i.get('kch_id', ''),
                    '课程名称': i.get('kcmc', ''),
                    '学分': i.get('xf', ''),
                    '开课状态': i.get('kkztmc', ''),
                    '上课时间': i.get('sksj', ''),
                    '上课地点': i.get('jxdd', ''),
                    '课程类别': i.get('kclbmc', ''),
                    '课程性质': i.get('kcxzmc', ''),
                    '开课类型': i.get('kklxmc', ''),
                    '教学班': i.get('jxbmc', ''),
                }
                if i.get('jsxx'):  # parse 任课教师
                    _tmp = i.get('jsxx').split('/')
                    if len(_tmp) == 3:
                        _bh, _xm, _zc = _tmp
                    else:
                        _bh, _xm = _tmp
                        _zc = 'None'
                    d['任课教师'] = {
                        '编号': _bh,
                        '姓名': _xm,
                        '职称': _zc
                    }
                if i.get('sksj', ''):  # parse 上课时间地点
                    _sj = i.get('sksj', '').split(';')
                    _dd = i.get('jxdd', '').split(';')
                    cnt = len(_sj)
                    _sjdd = []
                    for i in range(cnt):
                        _sj_s = _sj[i].split('{')
                        _sjdd.append({
                            '时间': _sj_s[0],
                            '地点': _dd[i],
                            '周次': _sj_s[1][:-2]
                        })
                    d['上课时间地点'] = _sjdd
                rdata_list.append(d)
            rdata = {
                'data': rdata_list,
                'name': rjson['items'][0].get('xm'),
                'sex': rjson['items'][0].get('xbmc'),
                'stuid': rjson['items'][0].get('xh_id'),
                'grade': rjson['items'][0].get('njdm_id'),
                'major': rjson['items'][0].get('zymc'),
                'class': rjson['items'][0].get('bjmc')
            }
            return rdata
        else:  # 否则以原始形式返回
            return rjson


def base64_to_hex(_s):
    _b = ''
    for _i in base64.b64decode(_s):
        _b += '%02x' % _i
    return _b


def hex_to_base64(_s):
    return base64.b64encode(_s)
