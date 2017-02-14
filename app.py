#!/usr/bin/env python3
# coding=utf-8
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver

import re


def main():
    driver = webdriver.PhantomJS()
    driver.get('') # edit the url here
    html = BeautifulSoup(driver.page_source, 'lxml')
    jobUrls = bsObj.findAll('a', {'href': re.compile('')})
    
    url = []
    for url in jobUrls:
        info.append() = getInfo(url)

def getInfo():
    pass

if __name__ == '__main__':
    main()
