#!/usr/bin/python2
# -*- coding:utf-8 -*-

import urllib, urllib2
from bs4 import BeautifulSoup

rank_url = 'https://www.baidu.com/s?wd=site%3A'
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


def get_rank(domain):
    req = urllib2.Request(rank_url + str(domain), headers=structure_headers())
    try:
        conn = urllib2.urlopen(req, timeout=TIMEOUT)
        response = conn.read()
    except urllib2.HTTPError, e:
        print(e.read().strip())
        print('-----------------------------------------------------' + str(domain))
        return 'error'
    except Exception, e:
        print(e)
        print('-----------------------------------------------------' + str(domain))
        return 'error'

    num = 0
    soup = BeautifulSoup(response, 'html.parser')
    find = soup.find('div', {'class': 'c-span21 c-span-last'})
    if find is None:
        find = soup.find('b', {'style': 'color:#333'})
        if find is not None:
            num = find.string
    else:
        num = find.p.b.string
    return num


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
    f = open('data/' + SOURCE + '/rank.txt', 'a')
    domains = get_domains()

    for index, domain in enumerate(domains):
        num = get_rank(domain)
        result = {'domain': str(domain), 'num': num}
        try:
            f.write(str(result) + '\n')
        except:
            print('write error')
        if index % 50 == 0:
            print('--------' + str(index) + '--------')


if __name__ == '__main__':
    main()
