#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import queue
import threading
import json
import pymysql


get_url = 'http://www.juming.com/ykj/?api_sou=1&ymlx=0&jgpx=0&meiye=&page='
check_url = 'http://m1.njzyxs.cn/check_wx_url.php?url='

domain_queue = queue.Queue()
check_queue = queue.Queue()

THREAD_COUNT = 100

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='123456',
                       db='wechat_prevent',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

headers = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/38.0.2125.111 Safari/537.36"),
    "X-Requested-With": "XMLHttpRequest",
}


def get_domains(request_url, f):
    response = requests.get(request_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    domains = soup.findAll('td', {'class': 'xinbz'})

    for domain in domains:
        for inp in domain.children:
            a = inp.find('a')
            if not a.string is None and a.string != ' ':
                domain_queue.put(a.string)
                f.write(a.string + '\n')


def check_domain(f):
    while True:
        domain = domain_queue.get()
        domains = {'original': domain, 'pre': 'abc.' + domain, 'rear': domain + '/abc', 'pr': 'abc.' + domain + '/abc'}
        data = dict()
        for key, domain1 in domains.items():
            response = requests.get(check_url + domain1)
            response.encoding = 'utf-8'
            try:
                result = json.loads(response.text)
                status = result['status']
            except Exception as e:
                status = -1
                print(e)
            data[key] = status
        data['domain'] = domain
        f.write(json.dumps(data) + '\n')
        check_queue.put(data)
        domain_queue.task_done()


def save():
    while True:
        data = check_queue.get()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO `domain_check` (`domain`, `original`, `pre`, `rear`, `pr`, `d_from`) VALUES (%s, %s, %s, %s, %s, 'juming.com')"
                cursor.execute(sql, (data['domain'], data['original'], data['pre'], data['rear'], data['pr']))
                conn.commit()
        except Exception as e:
            print(e)
        check_queue.task_done()


def main():
    cf = open('data/juming/check.txt', 'a')
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=check_domain, args=(cf,))
        t.daemon = True
        t.start()

    t1 = threading.Thread(target=save)
    t1.daemon = True
    t1.start()

    for i in range(1, 1000):
        if i % 50 == 0:
            print('--------------------' + str(i) + '-----------------------')
        try:
            with open('data/juming/domains.txt', 'a') as df:
                get_domains(get_url + str(i), df)
        except Exception as e:
            print(e)

    domain_queue.join()
    check_queue.join()
    cf.close()


if __name__ == '__main__':
    main()
