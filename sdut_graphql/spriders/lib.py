# coding=utf-8
from . import AuthServer
from bs4 import BeautifulSoup


class Lib(object):
    """ 图书馆中心 """

    def __init__(self, auth_server_class):
        assert isinstance(auth_server_class, AuthServer)
        self.session = auth_server_class.session

    def login(self):
        """ 通过统一登录平台登录至图书馆 """
        rst = self.session.get(
            'http://authserver.sdut.edu.cn/authserver/login?service=http%3A%2F%2F222.206.65.12%2Freader%2Fhwthau.php')
        if rst.url == 'http://222.206.65.12/reader/redr_info.php':
            return True
        return False

    def get_borrow(self):
        """ 获取借书本数 """
        rst = self.session.get(
            'http://222.206.65.12/reader/book_lst.php')
        soup = BeautifulSoup(rst.text, 'html.parser')
        cnt = soup.find_all('b')[0].string
        return cnt if cnt else 0

    def get_borrow_info(self):
        """ 获取借书详情 """
        rst = self.session.get(
            'http://222.206.65.12/reader/book_lst.php')
        soup = BeautifulSoup(rst.text, 'html.parser')
        table = soup.find('table')
        rdata = []
        trs = table.find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            if len(tds) < 5:  # 判断是否有书
                break
            rdata.append({
                'title': tds[1].find('a').string,  # 图书名
                'author': tds[1].text[len(tds[1].find('a').string) + 3:],  # 作者
                'borrowDate': tds[2].string.split()[0],  # 借书日期(xxxx-yy-zz)
                'backDate': tds[3].string.split()[0],  # 应还日期(xxxx-yy-zz)
                'borrowCnt': tds[4].string,  # 续借次数
                'site': tds[5].string  # 借书地点
            })
        return rdata
