# coding=utf-8
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sdut_query import AuthServer, Ehall, Ecard, Lib, Jwglxt
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/card/balance/', methods=['POST'])
def card_balance():
    """ 校园卡余额查询接口 """
    username = request.form.get('username')
    password = request.form.get('password')
    cookies = request.form.get('cookies', None)
    if cookies:
        cookies = json.loads(cookies)
    auth_server = AuthServer(cookies)
    if auth_server.login(username, password):  # 若成功登录
        if cookies:
            cookies = auth_server.cookies()
        ehall = Ehall(auth_server)
        ehall.login()
        ecard = Ecard(ehall)
        ecard.login()
        data = ecard.balance()
        rdata = {
            'code': 0,
            'data': {
                'item': '校园卡余额',
                'unit': '元',
                'value': data['balance'].split('/')[0]
            }
        }
        if cookies:  # 如果提供了 cookies 参数，则也会返回参数，否则正常退出
            rdata['data']['cookies'] = cookies
        else:
            auth_server.logout()
    else:  # 若未登录成功
        rdata = {
            'code': 1,
            'msg': '用户名或密码错误'
        }
    return jsonify(rdata)


@app.route('/card/info/', methods=['POST'])
def card_info():
    """ 校园卡详情查询接口 """
    username = request.form.get('username')
    password = request.form.get('password')
    cookies = request.form.get('cookies', None)
    if cookies:
        cookies = json.loads(cookies)
    auth_server = AuthServer(cookies)
    if auth_server.login(username, password):
        if cookies:
            cookies = auth_server.cookies()
        ehall = Ehall(auth_server)
        ehall.login()
        ecard = Ecard(ehall)
        ecard.login()
        data = ecard.consume_info()
        rdata = {
            'code': 0,
            'name': '校园卡消费记录',
            'data': data
        }
        if cookies:
            rdata['data']['cookies'] = cookies
        else:
            auth_server.logout()
    else:
        rdata = {
            'code': 1,
            'msg': '用户名或密码错误'
        }
    return jsonify(rdata)


@app.route('/borrow/info/', methods=['POST'])
def borrow_info():
    """ 图书馆详细信息 """
    username = request.form.get('username')
    password = request.form.get('password')
    cookies = request.form.get('cookies', None)
    if cookies:
        cookies = json.loads(cookies)
    auth_server = AuthServer(cookies)
    if auth_server.login(username, password):
        if cookies:
            cookies = auth_server.cookies()
        lib = Lib(auth_server)
        lib.login()
        data = lib.get_borrow_info()
        rdata = {
            'code': 0,
            'name': '借阅图书列表',
            'data': data
        }
        if cookies:
            rdata['data']['cookies'] = cookies
        else:
            auth_server.logout()
    else:
        rdata = {
            'code': 1,
            'msg': '用户名或密码错误'
        }
    return jsonify(rdata)


@app.route('/dorm_health/', methods=['POST'])
def dorm_health():
    """ 宿舍卫生查询接口 """
    username = request.form.get('username')
    password = request.form.get('password')
    cookies = request.form.get('cookies', None)
    if cookies:
        cookies = json.loads(cookies)
    auth_server = AuthServer(cookies)
    if auth_server.login(username, password):
        if cookies:
            cookies = auth_server.cookies()
        ehall = Ehall(auth_server)
        ehall.login()
        data = ehall.get_dorm_health()
        rdata = {
            'code': 0,
            'name': '宿舍卫生评分',
            'data': data
        }
        if cookies:
            rdata['data']['cookies'] = cookies
        else:
            auth_server.logout()
    else:
        rdata = {
            'code': 1,
            'msg': '用户名或密码错误'
        }
    return jsonify(rdata)


@app.route('/schedule/', methods=['POST'])
def schedule():
    """ 个人课表查询接口 """
    username = request.form.get('username')
    password = request.form.get('password')
    jwglxt = Jwglxt()
    if jwglxt.login(username, password):
        data = jwglxt.get_schedule()
        rdata = {
            'code': 0,
            'name': '课程信息',
            'data': data
        }
    else:
        rdata = {
            'code': 1,
            'msg': '用户名或密码错误'
        }
    return jsonify(rdata)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
