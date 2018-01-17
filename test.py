# coding=utf-8
from sdut_query import AuthServer

if __name__ == '__main__':
    a = AuthServer()
    username = input('username: ')
    password = input('password: ')
    print(a.login(username, password))
