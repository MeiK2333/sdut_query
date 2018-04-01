# SDUT Query

SDUT 的一些信息的爬虫


## 接口

内置接口采用 [GraphQL](http://docs.graphene-python.org/) 规范，使用 Django 开发，支持二次开发成数据统计的网站。

### 启动

```python
python3 manage.py runserver
```

### 使用

访问 ```localhost:8000/graphql``` 以使用接口。

### 示例

输入
```graphql
{
  ecard(username: "你的学号", password: "你的密码") {
    name
    code
    message
    status
    balance
    consume {
      time
      reason
      amount
      balance
      position
      termName
    }
  }
}
```

返回结果
```graphql
{
  "data": {
    "ecard": {
      "name": "你的姓名",
      "code": 0,
      "message": "OK",
      "status": "OK",
      "balance": 888.88,
      "consume": [
        ......(消费详情)
      ]
    }
  }
}
```

更多的使用方法可以参照页面右侧的 ```Documentation Explorer``` 。

## 爬虫

### AuthServer
[山东理工大学校内统一身份认证平台](http://authserver.sdut.edu.cn/authserver/login)，通过统一身份认证可以免账号密码登录至其他平台。

账号为学号，密码一般为身份证后六位（如果没有修改过的话）。

短时间内多次尝试登录（无论是否成功）会导致账号被 ban ，大概一天之内无法登录。

操作完成后记得登出，不然有可能被 ban 。

### Ehall
[山东理工大学网上服务大厅](http://ehall.sdut.edu.cn/new/ehall.html)，可以由此跳转到很多其他的平台。

登录方式为通过统一身份认证平台认证。

### Ecard
[山东理工大学校园卡中心](http://ecard.sdut.edu.cn/)，<del>网站崩了大半，因此对应的爬虫也失效了很多。余额查询功能仍可使用，但是近期消费等功能全部失效。</del>已恢复正常（其实也不正常……）。

登录方式为通过网上服务大厅跳转。

### Lib
[山东理工大学图书馆](http://222.206.65.12/reader/login.php)，可以查询一些借书相关的信息。

登录方式为通过网上服务大厅跳转。

### Jwglxt
[山东理工大学教学综合信息服务平台](http://211.64.28.123)（教务管理系统），看起来应该正在建设中，暂时只能用于查询课表。

账号为学号，密码为您自己的密码。

登录方式为直接到对应网站登录，采用了 csrf + rsa 验证。