#!/usr/bin/python2
# -*- coding:utf-8 -*-

import urllib, urllib2
import socket
import datetime

from bs4 import BeautifulSoup

TIMEOUT = 5

socket.setdefaulttimeout(TIMEOUT)


def main():
    print(datetime.datetime.now().strftime('%X'))
    f = open('data/domains_2.txt', 'a')
    for x in xrange(1, 1192):
        if x % 10 == 0:
            print(datetime.datetime.now().strftime('%X'))
            print x
        page_domains = get_domain(x)
        for domain in page_domains:
            try:
                f.write(str(domain) + '\n')
            except:
                print('write error')
    print(datetime.datetime.now().strftime('%X'))


def get_domain(page):
    url = 'http://www.juming.com/ykj/?api_sou=1&ymlx=0&jgpx=0&meiye=&page=' + str(page)
    try:
        req = urllib2.Request(url, headers=structure_headers())
        result = urllib2.urlopen(req, timeout=TIMEOUT)
        content = result.read()
    except:
        print('request error')

    soup = BeautifulSoup(content, 'html.parser')
    domains = soup.findAll('td', {'class': 'xinbz'})
    i = []
    for domain in domains:
        for a in domain.children:
            if not a.string is None and a.string != ' ':
                i.append(a.string)
    return i


def structure_headers():
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/38.0.2125.111 Safari/537.36")

    request_header = {
        "User-Agent": user_agent,  # 伪装成浏览器访问
        "X-Requested-With": "XMLHttpRequest",
    }
    return request_header


if __name__ == '__main__':
    main()
