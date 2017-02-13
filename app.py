#!/usr/bin/env python3
# coding=utf-8

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver

import re


def main():
    driver = webdriver.PhantomJS()
    driver.get()
