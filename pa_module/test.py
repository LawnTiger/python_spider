#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pa import Pa
from bs4 import BeautifulSoup
import json
import queue
import threading

SOURCE = 'ename'
THREAD_COUNT = 3
DOMAIN_Q = queue.Queue()


def get_domains():
    for line in open('data/' + SOURCE + '/domain.txt', 'r'):
        line = line.strip()
        if line is '':
            continue
        DOMAIN_Q.put(line)


def get_rank(pa, domain):
    response = pa.request('https://www.baidu.com/s?wd=site%3A' + domain)
    if response is -1:
        return -1
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


def deal(pa, f):
    while not DOMAIN_Q.empty():
        print('thread   ' + threading.current_thread().name)
        domain = DOMAIN_Q.get()
        num = get_rank(pa, domain)
        num = str(num)
        result = {'domain': str(domain), 'num': num}
        try:
            f.write(json.dumps(result) + '\n')
        except Exception as e:
            print('write error')
            print(e)


def main():
    pa = Pa()
    get_domains()
    threads = list()
    with open('data/' + SOURCE + '/rank.txt', 'a') as f:
        for i in range(THREAD_COUNT):
            threads.append(threading.Thread(target=deal, args=(pa, f)))

        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()



if __name__ == '__main__':
    main()
