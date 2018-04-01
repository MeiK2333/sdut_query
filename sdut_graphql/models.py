from django.db import models

import json
import graphene
import requests

from .spriders import AuthServer, Ecard, Ehall, Lib, Jwglxt

dorm_id_set = (
    ('1bh', '西校区 1 号公寓北楼'),
    ('1nh', '西校区 1 号公寓南楼',),
    ('2bh', '西校区 2 号公寓北楼'),
    ('2nh', '西校区 2 号公寓南楼'),
    ('3bh', '西校区 3 号公寓北楼'),
    ('3nh', '西校区 3 号公寓南楼'),
    ('4bh', '西校区 4 号公寓北楼'),
    ('4nh', '西校区 4 号公寓南楼'),
    ('5h', '西校区 5 号公寓'),
    ('6h', '西校区 6 号公寓'),
    ('7h', '西校区 7 号公寓'),
    ('8h', '西校区 8 号公寓'),
    ('9h', '西校区 9 号公寓'),
    ('10h', '西校区 10 号公寓'),
    ('11h', '西校区 11 号公寓'),
    ('12h', '西校区 12 号公寓'),
    ('13bh', '西校区 13 号公寓北楼'),
    ('13nh', '西校区 13 号公寓南楼'),
    ('14h', '西校区 14 号公寓'),
    ('15h', '西校区 15 号公寓'),
    ('16h', '西校区 16 号公寓'),
    ('17h', '西校区 17 号公寓'),
    ('18h', '西校区 18 号公寓'),
    ('19h', '西校区 19 号公寓'),
    ('20h', '西校区 20 号公寓'),
    ('21h', '西校区 21 号公寓'),
    ('22h', '西校区 22 号公寓'),
    ('y2h', '西校区研究生公寓北楼'),
    ('y1h', '西校区研究生公寓南楼'),
    ('d1h', '东校区 1 号公寓'),
    ('d2h', '东校区 2 号公寓'),
    ('d4h', '东校区 4 号公寓'),
    ('d6h', '东校区 6 号公寓'),
    ('d8h', '东校区 8 号公寓'),
    ('d9h', '东校区 9 号公寓'),
    ('d10h', '东校区 10 号公寓')
)


class BaseQuery(graphene.ObjectType):
    code = graphene.Int()
    message = graphene.String()
    status = graphene.String()

    def success(self, message):
        self.code = 0
        self.status = 'OK'
        self.message = message
        return self

    def param_err(self, message):
        self.code = -1
        self.status = 'PARAM_ERR'
        self.message = message
        return self

    def connect_err(self, message):
        self.code = 2
        self.status = 'CONNECT_ERR'
        self.message = message
        return self

    def auth_err(self, message):
        self.code = 1
        self.status = 'AUTH_ERR'
        self.message = message
        return self

    def parse_err(self, message):
        self.code = 4
        self.status = 'PARSE_ERR'
        self.message = message
        return self


class EcardConsume(graphene.ObjectType):
    time = graphene.String()
    reason = graphene.String()
    amount = graphene.String()
    balance = graphene.Float()
    position = graphene.String()
    termName = graphene.String()


class EcardQuery(BaseQuery):
    username = graphene.String()
    password = graphene.String()
    cookie = graphene.String()
    name = graphene.String()
    balance = graphene.Float()
    consume = graphene.List(EcardConsume)

    def get_info(self, get_balance=True, get_consume=False):
        if self.username is None or self.password is None:
            return self.param_err('参数 [username] 和 [password] 均为必填')

        try:
            a = AuthServer(json.loads(self.cookie))
            flag = a.login(self.username, self.password)
            if flag is False:
                return self.auth_err('授权验证失败，请检查用户名或密码')
            e = Ehall(a)
            flag = e.login()
            if flag is False:
                return self.auth_err('授权验证失败，可能是目标服务器出错')
            c = Ecard(e)
            flag = c.login()
            if flag is False:
                return self.auth_err('授权验证失败，可能是目标服务器出错')
        except json.decoder.JSONDecodeError:
            return self.parse_err('cookie 读取失败')
        except requests.exceptions.TooManyRedirects:
            return self.connect_err('连接服务器时发生了过多的重定向，一般是因为连接过于频繁，请稍后再尝试连接')
        except Exception as e:
            return self.connect_err('连接服务器时发生了错误：' + repr(e))

        try:
            if get_balance:
                balance_data = c.balance()
            if get_consume:
                consume_data = c.consume_info()
        except:
            return self.connect_err('请求连接原始服务器时出错')

        try:
            if get_balance:
                self.name = balance_data['name']
                self.balance = float(balance_data['balance'][:-3])
            if get_consume:
                data_list = []
                for i in consume_data:
                    ecard_consume = EcardConsume(
                        time=i['time'],
                        reason=i['reason'],
                        amount=i['amount'],
                        balance=i['balance'],
                        position=i['position'],
                        termName=i['termName']
                    )
                    data_list.append(ecard_consume)
                self.consume = data_list
        except:
            return self.parse_err('页面解析错误，可能是目标服务器出错或者目标服务器更新了页面结构')

        self.cookie = json.dumps(a.cookies())
        return self.success('OK')


class DormHealth(graphene.ObjectType):
    dorm_id = graphene.String()
    room_id = graphene.String()
    week = graphene.String()
    time = graphene.String()
    score = graphene.String()


class EhallQuery(BaseQuery):
    username = graphene.String()
    password = graphene.String()
    cookie = graphene.String()
    name = graphene.String()
    dorm_health = graphene.List(DormHealth)

    def get_info(self):
        if self.username is None or self.password is None:
            return self.param_err('参数 [username] 和 [password] 均为必填')

        try:
            a = AuthServer(json.loads(self.cookie))
            flag = a.login(self.username, self.password)
            if flag is False:
                return self.auth_err('授权验证失败，请检查用户名或密码')
            e = Ehall(a)
            flag = e.login()
            if flag is False:
                return self.auth_err('授权验证失败，可能是目标服务器出错')
        except json.decoder.JSONDecodeError:
            return self.parse_err('cookie 读取失败')
        except requests.exceptions.TooManyRedirects:
            return self.connect_err('连接服务器时发生了过多的重定向，一般是因为连接过于频繁，请稍后再尝试连接')
        except Exception as e:
            return self.connect_err('连接服务器时发生了错误：' + repr(e))

        try:
            self.name = e.get_name()
            data = e.get_dorm_health()
        except:
            return self.connect_err('请求连接原始服务器时出错')

        try:
            data_list = []
            for i in data['data']:
                dorm_health = DormHealth(
                    dorm_id=i['宿舍楼名称'],
                    room_id=i['房间号'],
                    week=i['周次'],
                    time=i['检查日期'],
                    score=i['分数']
                )
                data_list.append(dorm_health)
            self.dorm_health = data_list

        except:
            return self.parse_err('页面解析错误，可能是目标服务器出错或者目标服务器更新了页面结构')

        self.cookie = json.dumps(a.cookies())
        return self.success('OK')


class Borrow(graphene.ObjectType):
    title = graphene.String()
    author = graphene.String()
    borrowDate = graphene.String()
    backDate = graphene.String()
    borrowCnt = graphene.String()
    site = graphene.String()


class LibQuery(BaseQuery):
    username = graphene.String()
    password = graphene.String()
    cookie = graphene.String()
    borrow = graphene.List(Borrow)

    def get_info(self):
        if self.username is None or self.password is None:
            return self.param_err('参数 [username] 和 [password] 均为必填')

        try:
            a = AuthServer(json.loads(self.cookie))
            flag = a.login(self.username, self.password)
            if flag is False:
                return self.auth_err('授权验证失败，请检查用户名或密码')
            e = Ehall(a)
            flag = e.login()
            if flag is False:
                return self.auth_err('授权验证失败，可能是目标服务器出错')
            l = Lib(a)
            flag = l.login()
            if flag is False:
                return self.auth_err('授权验证失败，可能是目标服务器出错')
        except json.decoder.JSONDecodeError:
            return self.parse_err('cookie 读取失败')
        except requests.exceptions.TooManyRedirects:
            return self.connect_err('连接服务器时发生了过多的重定向，一般是因为连接过于频繁，请稍后再尝试连接')
        except Exception as e:
            return self.connect_err('连接服务器时发生了错误：' + repr(e))

        try:
            data = l.get_borrow_info()
        except:
            return self.connect_err('请求连接原始服务器时出错')

        try:
            data_list = []
            for i in data:
                borrow = Borrow(
                    title=i['title'],
                    author=i['author'],
                    borrowDate=i['borrowDate'],
                    backDate=i['backDate'],
                    borrowCnt=i['borrowCnt'],
                    site=i['site']
                )
                data_list.append(borrow)
            self.borrow = data_list
        except:
            return self.parse_err('页面解析错误，可能是目标服务器出错或者目标服务器更新了页面结构')

        self.cookie = json.dumps(a.cookies())
        return self.success('OK')


class JwglxtQuery(BaseQuery):
    username = graphene.String()
    password = graphene.String()
    year = graphene.Int()
    semester = graphene.Int()
    data = graphene.JSONString()
    name = graphene.String()
    sex = graphene.String()
    stuid = graphene.String()
    grade = graphene.String()
    major = graphene.String()
    _class = graphene.String()

    def get_info(self):
        if self.username is None or self.password is None:
            return self.param_err('参数 [username] 和 [password] 均为必填')

        try:
            jwglxt = Jwglxt()
            flag = jwglxt.login(self.username, self.password)
            if flag is False:
                return self.auth_err('授权验证失败，请检查用户名或密码')
        except requests.exceptions.TooManyRedirects:
            return self.connect_err('连接服务器时发生了过多的重定向，一般是因为连接过于频繁，请稍后再尝试连接')
        except Exception as e:
            return self.connect_err('连接服务器时发生了错误：' + repr(e))

        try:
            data = jwglxt.get_schedule(self.year, self.semester)
        except:
            return self.connect_err('请求连接原始服务器时出错')

        try:
            self.data = data['data']
            self.name = data['name']
            self.sex = data['sex']
            self.stuid = data['stuid']
            self.grade = data['grade']
            self.major = data['major']
            self._class = data['class']
        except:
            return self.parse_err('页面解析错误，可能是目标服务器出错或者目标服务器更新了页面结构')

        return self.success('OK')
