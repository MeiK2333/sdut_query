# coding=utf-8
from sdut_query import AuthServer, Ehall, Ecard, Lib, Jwglxt

if __name__ == '__main__':
    a = AuthServer()
    username = input('username: ')  # 山东理工大学统一登录中心账号密码
    password = input('password: ')  # http://ehall.sdut.edu.cn/new/ehall.html
    print('AuthServer login:', a.login(username, password))

    e = Ehall(a)
    print('Ehall login:', e.login())
    print('name:', e.get_name())
    print('dorm health', e.get_dorm_health())

    # c = Ecard(e)
    # print('Ecard login:', c.login())
    # print('balance:', c.balance())
    # print('consume:', c.consume_info())

    l = Lib(a)
    print('Lib login:', l.login())
    print('borrow:', l.get_borrow())
    print('borrow info:', l.get_borrow_info())

    a.logout()

    a = AuthServer()
    a.login(username, password)
    cookies = a.cookies()

    for i in range(10):
        a = AuthServer(cookies)  # 通过 cookies 复用，防止多次登陆导致账号被 ban(如果短时间内多次登陆会导致账号被 ban，无法登陆)
        print('login:', a.login(username, password))

    a.logout()

    username = input('username: ')  # 山东理工大学教学综合信息服务平台
    password = input('password: ')  # http://211.64.28.123
    jwglxt = Jwglxt()
    jwglxt.login(username, password)
    print(jwglxt.get_schedule(2017, 1))  # 获取个人课程表
