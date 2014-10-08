# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
player
~~~~~~~~~~~~~~

file commment here.

"""

import os
import urlparse
from scrapy import Spider, FormRequest, Request

class LocalRankSpider(Spider):

    name="local"

    allowed_domains = ["pc.sengoku-taisen.com"]

    def start_requests(self):
        return [FormRequest("http://pc.sengoku-taisen.com/Login.htm",
                                   formdata={'account': 'contee44', 'password': 'y84m6d29'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        for x in xrange(1, 48):
            yield Request(url="http://pc.sengoku-taisen.com/free/ranking/ranking_pref.html?s=1&e=200&p=" + str(x)
                , callback=self.parse_page)

    def parse_page(self, response):

        # 2014-09-26更新といった文字列を取得したい
        updated_time = response.xpath("//div[@id='main-inner']/text()")
        year, month, day = updated_time.re(ur'(\d{4})-(\d{2})-(\d{2})')
        sysdate = "".join([year, month, day])

        url = urlparse.urlparse(response.url)
        print(response.url)

        qs = urlparse.parse_qs(url.query)
        # htmlまるごとも保存しておきたい
        filename = "log/" + sysdate + "/local"\
                   "/ranking_pref" + "_" + qs['p'][0] + ".html"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'wb') as f:
            f.write(response.body)
