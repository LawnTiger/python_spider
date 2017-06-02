#!/usr/bin/python2
# -*- coding:utf-8 -*-

import pymysql
import json

SOURCE = 'ename'

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='pa_domain',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


def rank(f):
    i = 0
    for line in open(f, 'r'):
        try:
            if line is '':
                continue
            data = eval(line)
            if not isinstance(data, dict):
                print('--------------------------' + str(line))
                continue
            num = data['num']
            if not isinstance(num, int):
                num = num.encode('utf8')
                try:
                    num = int(filter(str.isdigit, num))
                except Exception, e:
                    print(e)

            try:
                with conn.cursor() as cursor:
                    sql = "UPDATE domain_info SET baidu_rank = %s WHERE domain = %s"
                    cursor.execute(sql, (str(num), data['domain']))
                    conn.commit()
            except Exception, e:
                print(e)

            if i % 2000 == 0:
                print('--------' + str(i))
            i += 1
        except Exception, e:
            print(e)


def whois(f):
    i = 0
    for line in open(f, 'r'):
        try:
            if line is '':
                continue
            try:
                data = json.loads(line)
            except Exception, e:
                print(e)
                continue
            if data['result']['status'] == 1:
                whois = data['result']['whois']
                creation = json.loads(data['result']['whois'])['FormatCreationDate']
                if 'T' in creation:
                    creation = creation.split('T')[0]

                try:
                    with conn.cursor() as cursor:
                        sql = "UPDATE domain_info SET creation = %s , whois_info = %s WHERE domain = %s"
                        cursor.execute(sql, (creation, whois, data['domain']))
                        conn.commit()
                except Exception, e:
                    print(e)

            if i % 5000 == 0:
                print('--------' + str(i))
            i += 1
        except Exception, e:
            print(e)


def icp(f):
    i = 0
    for line in open(f, 'r'):
        try:
            if line is '':
                continue
            data = eval(line)
            if not isinstance(data, dict):
                print('--------------------------' + str(line))
                continue
            if data.has_key('icp'):
                try:
                    with conn.cursor() as cursor:
                        sql = "UPDATE domain_info SET icp = 1, icp_info = %s WHERE domain = %s"
                        cursor.execute(sql, (data['icp'], data['domain']))
                        conn.commit()
                except Exception, e:
                    print(e)
            elif data.has_key('result') and data['result'] == 0:
                try:
                    with conn.cursor() as cursor:
                        sql = "UPDATE domain_info SET icp = 0 WHERE domain = %s"
                        cursor.execute(sql, (data['domain']))
                        conn.commit()
                except Exception, e:
                    print(e)
            if i % 2000 == 0:
                print('--------' + str(i))
            i += 1
        except Exception, e:
            print(e)


def main():
    f = 'data/' + SOURCE + '/icp.txt'
    rank(f)
    whois(f)
    icp(f)
    conn.close()


if __name__ == '__main__':
    main()
