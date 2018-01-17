# coding=utf-8
import requests
from bs4 import BeautifulSoup


class AuthServer(object):
    """ 山东理工大学统一登录平台 """

    def __init__(self, cookies=None):
        self.session = requests.session()
        if cookies:
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)

    def check_login(self):
        """ 检查登录状态 """
        login_html = self.session.get(
            'http://authserver.sdut.edu.cn/authserver/login')
        if login_html.url == 'http://authserver.sdut.edu.cn/authserver/index.do':  # 判断当前是否登录(自动跳转至首页)
            return True
        return False

    def login(self, username, password):
        """ 登录至统一身份认证平台 """
        if self.check_login():  # 如果当前已经登录
            return True

        login_html = self.session.get(
            'http://authserver.sdut.edu.cn/authserver/login')
        soup = BeautifulSoup(login_html.text, 'html.parser')
        ipts = soup.form.find_all('input')
        data = {
            'username': username,
            'password': password,
            'rememberMe': False
        }
        for ipt in ipts:
            if ipt.get('value'):
                data[ipt.get('name')] = ipt.get('value')

        rst = self.session.post(
            'http://authserver.sdut.edu.cn/authserver/login', data=data)
        if rst.url == 'http://authserver.sdut.edu.cn/authserver/index.do':  # 若页面跳转至首页，则说明登录成功
            return True
        elif rst.url == 'http://authserver.sdut.edu.cn/authserver/login':  # 若页面跳转回登录界面，则说明登录失败(用户名或密码错误)
            return False

    def logout(self):
        """ 退出登录 """
        self.session.get(
            'http://authserver.sdut.edu.cn/authserver/logout?service=/authserver/login')

    def cookies(self):
        return self.session.cookies
