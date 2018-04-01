# coding=utf-8
from . import AuthServer
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

    def get_dorm_health(self):
        """ 获取宿舍卫生分数 """
        self.session.get('http://ehall.sdut.edu.cn/appShow?appId=4606888687682093')  # 某些神奇的预处理
        data = {
            'pageSize': 50,  # 只读取一页，50 条数据
            'pageNumber': 1  # 我就不信，一个学期能有 50 个周不成？
        }
        rst = self.session.get(
            'http://ehall.sdut.edu.cn/xsfw/sys/sswsapp/modules/dorm_health_student/sswsxs_sswsxsbg.do', data=data)
        rjson = json.loads(rst.text)
        rlist = []
        for i in rjson['datas']['sswsxs_sswsxsbg']['rows']:
            d = {
                '宿舍楼名称': i['SSLMC'],
                '房间号': i['FJH'],
                '周次': i['ZC'],
                '检查日期': i['JCRQ'],
                '分数': i['FS']
            }
            rlist.append(d)
        rdata = {
            'totalSize': rjson['datas']['sswsxs_sswsxsbg']['totalSize'],
            'data': rlist
        }
        return rdata
