#!/usr/bin/python2
# -*- coding:utf-8 -*-

import urllib, urllib2
import time
from bs4 import BeautifulSoup

icp_url = 'http://icp.aizhan.com/'
SOURCE = 'ename'

TIMEOUT = 6


def get_domains():
    domains = []
    for line in open('data/' + SOURCE + '/domain.txt', 'r'):
        line = line.replace('\n', '')
        if line is '':
            continue
        domains.append(line)
    return domains


def get_icp(domain):
    req = urllib2.Request(icp_url + str(domain), headers=structure_headers())
    try:
        conn = urllib2.urlopen(req, timeout=TIMEOUT)
        response = conn.read()
    except urllib2.HTTPError, e:
        print(e.read().strip())
        print('-----------------------------------------------------' + str(domain))
        return {'result': 2}
    except Exception, e:
        print(e)
        print('-----------------------------------------------------' + str(domain))
        return {'result': 2}

    soup = BeautifulSoup(response, 'html.parser')
    div = soup.find('div', {'id': 'refresh-txt'})
    if div.span is None:
        return {'result': 0}
    else:
        table = soup.find('table', {'class': 'table'})
        return {'result': 1, 'icp': str(table)}


def structure_headers():
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/38.0.2125.111 Safari/537.36")
    request_header = {
        "User-Agent": user_agent,  # 伪装成浏览器访问
        "X-Requested-With": "XMLHttpRequest",
    }
    return request_header


def main():
    f = open('data/' + SOURCE + '/icp.txt', 'a')
    domains = get_domains()

    for index, domain in enumerate(domains):
        result = get_icp(domain)
        result['domain'] = str(domain)
        try:
            f.write(str(result) + '\n')
        except:
            print('write error')
        time.sleep(0.4)  # 该网站控制访问频率
        if index % 10 == 0:
            print('--------' + str(index) + '--------')


if __name__ == '__main__':
    main()
