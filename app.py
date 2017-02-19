#!/usr/bin/env python3
# coding=utf-8
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver

import re


driver = webdriver.PhantomJS()

def main():
    driver.get('http://search.51job.com/list/030200%252C00,000000,0000,00,9,07,php,2,1.html?lang=c&degreefrom=99&stype=1&workyear=99&cotype=99&jobterm=99&companysize=99&radius=-1&address=&lonlat=&postchannel=&list_type=&ord_field=&curr_page=&dibiaoid=0&landmark=&welfare=') # edit the url here
    html = BeautifulSoup(driver.page_source, 'html5lib')
    jobUrls = html.findAll('a', {'href': re.compile('http://jobs.51job.com/guangzhou*')})

    info = []
    for url in jobUrls:
        content = getInfo(url['href'])
        content = content.replace('\t', '').replace('举报', '').replace('分享', '')
        info.append(content)
        print(info)
        return
    print(info[0])

def getInfo(url):
    driver.get(url)
    html = BeautifulSoup(driver.page_source, 'html5lib')
    requirement = html.find('div', {'class': re.compile('bmsg job_msg inbox')})

    tmp = ''
    for content in requirement:
        if content.string is not None:
            tmp += content.string
        
    return tmp


if __name__ == '__main__':
    main()
