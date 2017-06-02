#!/usr/bin/python2
# -*- coding:utf-8 -*-

import pymysql
import json
import datetime

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='456123xyZ',
                       db='pa_domain',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


def insert(domain):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO `domain_info` (`domain`, `from`) VALUES (%s, 'ename.cn')"
            cursor.execute(sql, (domain))
            conn.commit()
    except Exception, e:
        print(str(e))


def main():
    for line in open('data/ename/domain.txt', 'r'):
        line = line.replace('\n', '')
        if line is '':
            continue
        insert(line)
    conn.close()


if __name__ == '__main__':
    main()
