#!/usr/bin/python2
# -*- coding:utf-8 -*-

import urllib, urllib2
import cookielib
import ssl
import pymysql
import json
import datetime
import threading
import socket


TIMEOUT = 5
THREAD_COUNT = 100

socket.setdefaulttimeout(TIMEOUT) # 设置超时时间
ssl._create_default_https_context = ssl._create_unverified_context # 允许不安全访问


conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='test',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

# 登录、验证码
code_url = ""
login_url = ""

# 请求数据的 url
u = ['', '', '']


def simulation_login():
    """
    模拟登陆：启用cookie，先发一次用户名密码获取验证码，后再发验证码
    """
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)

    form_data = urllib.urlencode({
        "loginName": '',
        "password": '',
    })
    req = urllib2.Request(code_url, data = form_data, headers = structure_headers())
    result = urllib2.urlopen(req, timeout = TIMEOUT)
    content = result.read()
    print(str(content))
    word = input('>>')
    form_data = urllib.urlencode({
        "loginName": '',
        "password": '',
        'code': word
    })
    req = urllib2.Request(login_url, data = form_data, headers = structure_headers())
    result = urllib2.urlopen(req, timeout = TIMEOUT)
    content = result.read()
    print(str(content))

def get_data(c_id):
    """ 
    获取数据：post请求数据
    """
    if c_id % 500 == 0:
        print('-> ', c_id) # 输出进度
    form_data = urllib.urlencode({
        "pageIndex": '1',
        "pageSize": '100000',
        'accountID': c_id
    })
    data = list()
    for i in [0, 1, 2]:
        try:
            req = urllib2.Request(u[i], data = form_data, headers = structure_headers())
            result = urllib2.urlopen(req, timeout = TIMEOUT)
            result = str(result.read())
        except:
            result = 'time out'
            print(c_id, i, result)
        finally:
            data.append(result)
    return data

def structure_headers():
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/38.0.2125.111 Safari/537.36")

    request_header = {
        "User-Agent": user_agent, # 伪装成浏览器访问
        "X-Requested-With": "XMLHttpRequest",
    }
    return request_header

def get_ids():
    try:
        with conn.cursor() as cursor:
            sql = "select id from customers order by id asc"
            cursor.execute(sql)
            ids = cursor.fetchall()
    finally:
        pass
    return ids

def deal(ids, filename):
    """
    处理数据，根据id获取数据写入文本
    """
    for c_id in ids:
        c_id = c_id['id']
        data = get_data(c_id)
        f = open(filename, 'a')
        try:
            f.write('\n'+str(c_id)+'|||'+json.dumps(data))
        except:
            print(c_id, 'write error')
        finally:
            f.close()


def main():
    simulation_login()
    print(datetime.datetime.now().strftime('%X')) # 开始时间

    ids = get_ids()
    threads = []

    # id分组
    id_group = [ids[i:i+THREAD_COUNT] for i in xrange(0, len(ids), THREAD_COUNT)]
    # 文件名组
    filename_group = ['d'+str(i)+'.txt' for i in xrange(THREAD_COUNT)]

    # 多线程
    for i in xrange(THREAD_COUNT):
        threads.append(threading.Thread(target=deal, args=(id_group[i], filename_group[i])))

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    conn.close()
    print(datetime.datetime.now().strftime('%X')) # 结束时间


if __name__ == '__main__':
    main()
