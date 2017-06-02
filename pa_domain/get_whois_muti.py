#!/usr/bin/python2
# -*- coding:utf-8 -*-

import uuid
import time
import sys
import hashlib
import hmac
from hashlib import sha1
import base64
import urllib, urllib2
import json
import threading

TIMEOUT = 5
THREAD_COUNT = 20
SOURCE = 'ename'

access_key_id = ''  # 填自己的 aliyun access_key
access_key_secret = ''  # key_secret
ecs_server_address = 'http://domain.aliyuncs.com'


def compose_url(domain):
    user_params = {}
    user_params['Action'] = 'GetWhoisInfo'
    user_params['DomainName'] = str(domain)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    parameters = { \
        'Format': 'JSON', \
        'Version': '2016-05-11', \
        'AccessKeyId': access_key_id, \
        'SignatureVersion': '1.0', \
        'SignatureMethod': 'HMAC-SHA1', \
        'SignatureNonce': str(uuid.uuid1()), \
        'Timestamp': timestamp, \
    }

    for key in user_params.keys():
        parameters[key] = user_params[key]

    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = ecs_server_address + "/?" + urllib.urlencode(parameters)
    return url


def percent_encode(str):
    res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def get_whois(domain):
    url = compose_url(domain)
    request = urllib2.Request(url)
    try:
        conn = urllib2.urlopen(request)
        response = conn.read()
    except urllib2.HTTPError, e:
        print(e.read().strip())
        print('-----------------------------------------------------' + str(domain))
        return {'status': 0}
    except Exception, e:
        print(e)
        print('-----------------------------------------------------' + str(domain))
        return {'status': 2}
    return {'status': 1, 'whois': str(response)}


def get_domains():
    domains = []
    for line in open('data/' + SOURCE + '/domain.txt', 'r'):
        line = line.replace('\n', '')
        if line is '':
            continue
        domains.append(line)
    return domains


def deal(domains, f):
    data = dict()
    for index, domain in enumerate(domains):
        data['domain'] = str(domain)
        data['result'] = get_whois(domain)
        try:
            f.write(json.dumps(data) + '\n')
        except:
            print('write error')
        if index % 50 == 0:
            print('--------' + str(index) + '--------')


def main():
    f = open('data/' + SOURCE + '/whois.txt', 'a')

    domains = get_domains()[10000:]
    threads = []

    # domain 分组
    interval = len(domains) / THREAD_COUNT + 1
    domain_group = [domains[i:i + interval] for i in xrange(0, len(domains), interval)]

    for i in xrange(THREAD_COUNT):
        threads.append(threading.Thread(target=deal, args=(domain_group[i], f)))

    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

    f.close()


if __name__ == '__main__':
    main()
