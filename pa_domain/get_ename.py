#!/usr/bin/python2
# -*- coding:utf-8 -*-

import urllib, urllib2
import socket
import datetime
import json
import threading

TIMEOUT = 5
THREAD_COUNT = 1

socket.setdefaulttimeout(TIMEOUT)


def get_domain(page):
    url = 'http://auction.ename.com/tao/buynow?ajax=1&domainsld=&domaintld[]=0&domainlenstart=1&domainlenend=\
&domaingroup=0&bidpricestart=0&bidpriceend=&finishtime=0&registrar=0&sort=1&hidenobider=0&inhidenobider=0\
&bidstartone=0&sldtypestart=0&sldtypeend=0&transtype=1&type=0&per_page=3&is_index=1&flag=&skipword1=&skipstart1=0\
&skipend1=0&skipword2=undefined&skipstart2=0&skipend2=0&domain=2&exptime=0&selectTwo=&page=' + str(page)
    try:
        req = urllib2.Request(url, headers=structure_headers())
        result = urllib2.urlopen(req, timeout=TIMEOUT)
        respone = result.read()
    except urllib2.HTTPError, e:
        print(e.read().strip())
        return
    except Exception, e:
        print(e)
        return

    try:
        data = json.loads(respone)
    except Exception, e:
        print(e)
        return
    if data.has_key('data'):
        return [item['t_dn'] for item in data['data']]


def structure_headers():
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/38.0.2125.111 Safari/537.36")
    request_header = {
        "User-Agent": user_agent,  # 伪装成浏览器访问
        "X-Requested-With": "XMLHttpRequest",
    }
    return request_header


def deal(page, f):
    for p in page:
        if p % 300 == 0:
            print('-----------' + str(p))
        page_domains = get_domain(p)
        if page_domains is None:
            continue
        for domain in page_domains:
            try:
                f.write(str(domain) + '\n')
            except Exception, e:
                print(e)
                print(domain)
                print('write error-----------' + str(p))


def main():
    print(datetime.datetime.now().strftime('%X'))

    f = open('data/ename.txt', 'a')
    pages = range(199810)
    deal(pages, f)

    # threads = []

    # # page 分组
    # interval = len(pages) / THREAD_COUNT + 1
    # pages_group = [pages[i:i+interval] for i in xrange(0, len(pages), interval)]

    # for i in xrange(THREAD_COUNT):
    #     threads.append(threading.Thread(target=deal, args=(pages_group[i],f)))

    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # for t in threads:
    #     t.join()

    f.close()
    print(datetime.datetime.now().strftime('%X'))


if __name__ == '__main__':
    main()
