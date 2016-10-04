#!/bin/env python2
# coding:utf-8
__author__ = 'liuzheng'
import urllib
import urllib2
import os
import socket

try:
    import simplejson as json
except:
    import json
# curl -X POST https://dnsapi.cn/Record.Modify -d 'login_email=api@dnspod.com&login_password=password&format=json&domain_id=2317346&record_id=16894439&sub_domain=www&value=3.2.2.2&record_type=A&record_line=默认'
def Step1(email, password):
    url = "https://dnsapi.cn/Domain.List"
    data = {
        "login_email": email,
        "login_password": password,
        "format": "json",
    }
    post_data = urllib.urlencode(data)
    f = urllib2.urlopen(url, post_data).read()
    for i in json.loads(f)['domains']:
        print i['id'], i['punycode']
    domain_id = raw_input("please choose one: ")
    create_or_choose = raw_input("Create(Y) or Choose one(n)?")
    create_or_choose = create_or_choose or 'Y'
    if create_or_choose in ['Y', 'Yes', 'yes', 'y']:
        url = "https://dnsapi.cn/Record.Create"
        sub_domain = raw_input("sub_domain:")
        if not sub_domain:
            print("Error")
            exit()
        else:
            ip = str(os.popen("curl ifconfig.me").read())
            data = {
                "login_email": email,
                "login_password": password,
                "domain_id": domain_id,
                "format": "json",
                "sub_domain": sub_domain,
                "record_type": "A",
                "record_line": "默认",
                "value": ip
            }
            post_data = urllib.urlencode(data)
            f = urllib2.urlopen(url, post_data).read()
            i = json.loads(f)
            print "status:", i['status']['message']
            print "record_id:", i['record']['id']
    else:
        url = "https://dnsapi.cn/Record.List"
        data = {
            "login_email": email,
            "login_password": password,
            "domain_id": domain_id,
            "format": "json",
        }
        post_data = urllib.urlencode(data)
        f = urllib2.urlopen(url, post_data).read()
        for i in json.loads(f)['records']:
            print i['id'], i['name'], i['value'], i['type'], i['ttl']


def main(email, password, domain_id, record_id,domain, sub_domain):
    if not domain_id or not record_id or not domain:
        print("Please Check your domain_id/record_id/domain")
        exit()
    ip = os.popen("curl ifconfig.me").read()
    ipd = socket.gethostbyname(domain)
    if ip == ipd:
        exit()
    url = "https://dnsapi.cn/Record.Modify"
    data = {
        "login_email": email,
        "login_password": password,
        "format": "json",
        "domain_id": domain_id,
        "record_id": record_id,
        "sub_domain": sub_domain,
        "value": ip,
        "record_type": "A",
        "record_line": "默认",
    }
    post_data = urllib.urlencode(data)
    urllib2.urlopen(url, post_data)


if __name__ == '__main__':
    email = ""
    password = ""
    # Step1(email, password)
    domain_id = ""
    record_id = ""
    domain = ''
    sub_domain = ''
    main(email, password, domain_id, record_id, domain, sub_domain)
