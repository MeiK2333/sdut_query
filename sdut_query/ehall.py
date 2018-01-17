# coding=utf-8
from sdut_query import AuthServer
import json


class Ehall(object):
    """ 山东理工大学网上服务大厅 """

    def __init__(self, auth_server_class):
        assert isinstance(auth_server_class, AuthServer)  # 参数应该为已登录的 AuthServer
        self.session = auth_server_class.session

    def login(self):
        """ 利用统一登录平台来进行登录 """
        # 如果统一登录平台已经登录成功，那这里是会直接认证通过的
        rst = self.session.get(
            'http://ehall.sdut.edu.cn/login?service=http://ehall.sdut.edu.cn/new/ehall.html')
        if rst.url == 'http://ehall.sdut.edu.cn/new/ehall.html':
            return True
        return False

    def get_name(self):
        """ 获取姓名信息 """
        rst = self.session.get(
            'http://ehall.sdut.edu.cn/publicapp/sys/myyktzd/api/getOverviewInfo.do')
        rjson = json.loads(rst.text)
        return rjson['datas']['NAME']

    def get_uid(self):
        """ 获取学号信息 """
        rst = self.session.get(
            'http://ehall.sdut.edu.cn/publicapp/sys/myyktzd/api/getOverviewInfo.do')
        rjson = json.loads(rst.text)
        return rjson['datas']['SFRZH']
