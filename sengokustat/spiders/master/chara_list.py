# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
character
~~~~~~~~~~~~~~

file commment here.

"""

import os, re
from scrapy import Spider, FormRequest, Request, Selector
from sengokustat.settings import NET_ID, NET_PASS
from sengokustat.db import db

class CharaListSpider(Spider):

    name="charalist"

    allowed_domains = ["pc.sengoku-taisen.com"]

    def start_requests(self):
        self.parameters = dict()
        return [FormRequest("http://pc.sengoku-taisen.com/Login.htm",
                                   formdata={'account': NET_ID, 'password': NET_PASS},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        for v in [1000 , 1100, 1200, 2000, 2100, 2200, 3000]:
            yield Request(url="http://pc.sengoku-taisen.com/members/datalist/character/list.html?v=" + str(v)
                , callback=self.parse_offset)

    def parse_offset(self, response):
        # find offset
        to_last_link = response.css('table.linklist').xpath("tr/td//a[@class='tolast']/@href").extract()
        if to_last_link:
            offset, v = re.search(ur"offset=(\d+)&v=(\d+)", to_last_link[0]).groups()
            for x in range(0, int(offset) + 1):
                yield Request(url="http://pc.sengoku-taisen.com/members/datalist/character/list.html?v="
                                  + str(v) + "&offset=" + str(x)
                    , callback=self.parse_page)
        else:
            self.parse_page(response)


    def parse_page(self, response):

        c = re.search(ur"v=(\d+)", response.url).group(1)

        filename = "log/" + "master" + \
                   "/character_list.txt"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'a') as f:
            for no in response.css('table.datalist_character').xpath('tr/td//a/@href').re(ur'data\.html\?p\=(.*)'):
                f.write(c + "\t" + no)
                f.write(u'\n')
