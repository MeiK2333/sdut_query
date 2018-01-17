# coding=utf-8
from sdut_query import AuthServer, Ehall, Ecard, Lib

if __name__ == '__main__':
    a = AuthServer()
    username = input('username: ')
    password = input('password: ')
    print('AuthServer login:', a.login(username, password))

    e = Ehall(a)
    print('Ehall login:', e.login())
    print('name:', e.get_name())

    c = Ecard(e)
    print('Ecard login:', c.login())
    print('balance:', c.balance())
    # print('consume:', c.consume_info())

    l = Lib(a)
    print('Lib login:', l.login())
    print('borrow:', l.get_borrow())
    print('borrow info:', l.get_borrow_info())

    a.logout()
