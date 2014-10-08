# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
keiryaku_list
~~~~~~~~~~~~~~

file commment here.

"""

import os, re
from scrapy import Spider, FormRequest, Request, Selector
from sengokustat.db import db

class KeiryakuListSpider(Spider):

    name="keiryakulist"

    allowed_domains = ["pc.sengoku-taisen.com"]

    def start_requests(self):
        return [FormRequest("http://pc.sengoku-taisen.com/Login.htm",
                                   formdata={'account': 'contee44', 'password': 'y84m6d29'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        for c in range(10):
            yield Request(url="http://pc.sengoku-taisen.com/members/datalist/keiryaku/list.html?c=" + str(c)
                , callback=self.parse_offset)

    def parse_offset(self, response):
        # find offset

        to_last_link = response.css('table.linklist').xpath("tr/td//a[@class='tolast']/@href").extract()
        if to_last_link:
            offset, c = re.search(ur"offset=(\d+)&c=(\d+)", to_last_link[0]).groups()
            for x in range(0, int(offset) + 1):
                yield Request(url="http://pc.sengoku-taisen.com/members/datalist/keiryaku/list.html?c="
                                  + str(c) + "&offset=" + str(x)
                    , callback=self.parse_page)
        else:
            self.parse_page(response)


    def parse_page(self, response):

        c = re.search(ur"c=(\d+)", response.url).group(1)

        filename = "log/" + "master" + \
                   "/keiryaku_list.txt"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'a') as f:
            for no in response.css('table.touch').xpath('tr/td//a/@href').re(ur'data\.html\?p\=(.*)'):
                f.write(c + "\t" + no)
                f.write(u'\n')
