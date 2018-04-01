# coding=utf-8
from . import Ehall
from bs4 import BeautifulSoup
import requests
import datetime
import json


class Ecard(object):
    """ 校园卡中心 """

    def __init__(self, ehall_class):
        assert isinstance(ehall_class, Ehall)  # 参数为已经登录的 Ehall
        self.ehall_class = ehall_class
        self.session = requests.session()  # 校园卡中心的模拟登录需要新建会话

    def login(self):
        """ 通过网上服务大厅登录至校园卡中心 """
        rst = self.ehall_class.session.get(
            'http://ehall.sdut.edu.cn/publicapp/sys/xkpyktjc/single_sign.do')
        data = json.loads(rst.text)
        rst = self.session.post(data['url'], data=data)
        if rst.url == 'http://211.64.27.136/SelfSearch/Default.aspx':
            return True
        return False

    def balance(self):
        """ 余额查询 """
        url = 'http://211.64.27.136/SelfSearch/EcardInfo/UserBaseInfo_Seach.aspx'
        rst = self.session.get(url)
        soup = BeautifulSoup(rst.text, 'html.parser')
        ipts = soup.find_all('input')
        data = {
            'uid': ipts[3].get('value'),
            'name': ipts[4].get('value'),
            'balance': ipts[9].get('value')
        }
        return data

    def consume_info(self):
        """ 消费详情查询 """
        uid = self.ehall_class.get_uid()
        url = 'http://211.64.27.136/SelfSearch/EcardInfo/CONSUMEINFO_SEACH.ASPX?outid=' + uid
        rst = self.session.get(url)
        soup = BeautifulSoup(rst.text, 'html.parser')
        ipts = soup.find_all('input')
        today = datetime.date.today()
        old_3 = today - datetime.timedelta(days=2)  # 默认查两天的数据(因为校园卡中心的限制，大部分情况下，更多的数据也很难查询出来)
        data = {
            'ctl00$ContentPlaceHolder1$ConsumeAscx1$sDateTime': old_3.strftime("%Y%m%d"),
            'ctl00$ContentPlaceHolder1$ConsumeAscx1$eDateTime': today.strftime("%Y%m%d"),
            'ctl00$ContentPlaceHolder1$ConsumeAscx1$ScriptManager1': 'ctl00$ContentPlaceHolder1$ConsumeAscx1$ScriptManager1|ctl00$ContentPlaceHolder1$ConsumeAscx1$btnSeach',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'ctl00$ContentPlaceHolder1$ConsumeAscx1$btnSeach': ''
        }
        for ipt in ipts:
            if ipt.get('value'):
                data[ipt.get('name')] = ipt.get('value')
        rst = self.session.post(
            'http://211.64.27.136/SelfSearch/EcardInfo/CONSUMEINFO_SEACH.ASPX?outid=' + uid, data=data)
        soup = BeautifulSoup(rst.text, 'html.parser')
        table = soup.find('table').find_all('table')[3]
        trs = table.find_all('tr')
        rdata = []
        for tr in trs[2:]:
            tds = tr.find_all('td')
            time_s = tds[0].string.split('/')
            time = time_s[0] + '-'
            time += time_s[1] if len(time_s[1]) == 2 else '0' + time_s[1]
            time += '-'
            time += time_s[2] if len(time_s[2]) == 11 else '0' + time_s[2]

            rdata.append({
                'time': time[:-3],  # 交易时间
                'reason': tds[1].string,  # 科目描述
                'amount': tds[2].string,  # 交易金额
                'balance': tds[4].string,  # 余额
                'position': tds[7].string,  # 工作站
                'termName': tds[8].string  # 交易终端
            })
        return rdata
