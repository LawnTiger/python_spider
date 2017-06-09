#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import time
import socket
import queue
import http.cookiejar


__author__ = 'https://github.com/LawnTiger'

socket.setdefaulttimeout(5)


class Pa:
    """
        爬虫主类
        自带代理，异常处理
    """

    def __init__(self, is_proxy=False):
        self.proxy_queue = queue.Queue()
        if is_proxy is True:
            for proxy in self.get_proxy():
                self.proxy_queue.put(proxy)
        print('count of proxies : ' + str(self.proxy_queue.qsize()))

    def request(self, url):
        # set cookie
        # cookie = http.cookiejar.CookieJar()
        # cookie_pro = urllib.request.HTTPCookieProcessor(cookie)
        # opener = urllib.request.build_opener(cookie_pro)
        # urllib.request.install_opener(opener)
        if not self.proxy_queue.empty():
            self.add_proxy(url)
        result = self.make_request(url)
        return result

    def add_proxy(self, url):
        if 'https' in url[:5]:
            http_type = 'https'
        else:
            http_type = 'http'
        proxy = self.proxy_queue.get()
        print(proxy)
        self.proxy_queue.put(proxy)
        proxy = {http_type: proxy}
        proxy_support = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

    def make_request(self, url):
        try:
            req = urllib.request.Request(url, headers=self._headers())
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print(e.code + '---' + e.read())
            print('-------------------------- ' + url + ' ------------------------------')
            return -1
        except Exception as e:
            print(e)
            print('-------------------------- ' + url + ' ------------------------------')
            return -1
        return response

    def get_proxy(self):
        print('getting proxy from web ...')
        ips = list()
        for i in range(389, 391):
            try:
                req = urllib.request.Request('http://www.xicidaili.com/nt/' + str(i), headers=self._headers())
                response = urllib.request.urlopen(req)
                html = BeautifulSoup(response, 'html.parser')
                divs = html.find_all('tr', {'class': 'odd'})
                for div in divs:
                    bar = div.find_all('div', {'class': 'bar'})
                    num1 = float(bar[0].get('title')[:-1])
                    num2 = float(bar[1].get('title')[:-1])
                    if num1 > 0.5 or num2 > 0.5:
                        continue
                    ip = div.contents[3].string + ':' + div.contents[5].string
                    ips.append(ip)
                time.sleep(0.2)
            except Exception as e:
                print(e)
        if len(ips) is 0:
            print('-------------------------- get proxies from web site error -----------------------------')
            raise Exception
        return ips

    @staticmethod
    def _headers():
        user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/38.0.2125.111 Safari/537.36")
        request_header = {
            "User-Agent": user_agent,  # 伪装成浏览器访问
            "X-Requested-With": "XMLHttpRequest",
        }
        return request_header


def test():
    pass

if __name__ == '__main__':
    test()
