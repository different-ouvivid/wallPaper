#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from imp import reload

import requests
from requests.adapters import HTTPAdapter
# import gevent
# import gevent.monkey
from bs4 import BeautifulSoup as bs
import uuid
import os
import time
from multiprocessing import Process

# gevent.monkey.patch_all()
reload(sys)


headers = dict()
headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
headers["Accept-Encoding"] = "gzip, deflate, sdch"
headers["Accept-Language"] = "zh-CN,zh;q=0.8"
headers["Accept-Language"] = "zh-CN,zh;q=0.8"
request_retry = HTTPAdapter(max_retries=3)


def my_get(url, refer=None):
    session = requests.session()
    session.headers = headers
    if refer:
        headers["Referer"] = refer
    session.mount('https://', request_retry)
    session.mount('http://', request_retry)
    return session.get(url)


def get_type_content(page):
    if page < 2:
        url = 'http://www.netbian.com/index.htm'
    else:
        #  http://www.netbian.com/index_2.htm
        url = 'http://www.netbian.com/index_'+str(page)+'.htm'
    soup = bs(my_get(url).content, "lxml")
    li_list = soup.select("div#main div.list ul li")
    # li_list得到了很多的list，接下来是取出每一个list里面的img，当然title要有鬼刀2字
    for li in li_list:
        pic_url = li.select_one("img").attrs["src"]
        pic_title = li.select_one("img").attrs["alt"]
        key_word = '鬼刀'
        if key_word in pic_title :
            response = my_get(pic_url)
            i = 0
            while response.status_code != 200:
                i += 1
                if i > 5:
                    return
                time.sleep(0.8)
                response = my_get(pic_url)
            if not os.path.exists("wallpaper"):
                os.mkdir("wallpaper")
            with open("wallpaper/" + str(pic_title) + ".jpg", 'wb') as fs:
                fs.write(response.content)
                print("download success!:" + pic_title)

def main():
    for page in range(1, 1025):
        get_type_content(page)
if __name__ == "__main__":
    main()
