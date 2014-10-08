# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
force
~~~~~~~~~~~~~~

file commment here.

"""

import os
from sengokustat.settings import NET_ID, NET_PASS
from scrapy import Spider, FormRequest, Request, Selector

class ForceRankSpider(Spider):

    name = "force"

    allowed_domains = ["pc.sengoku-taisen.com"]

    def start_requests(self):
        return [FormRequest("http://pc.sengoku-taisen.com/Login.htm",
                                   formdata={'account': NET_ID, 'password': NET_PASS},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        return Request(url="http://pc.sengoku-taisen.com/free/ranking/ranking_card.html"
         , callback=self.parse_page)

    def parse_page(self, response):

        # 2014-09-26更新といった文字列を取得したい
        updated_time = response.xpath("//div[@id='main-inner']/text()")
        year, month, day = updated_time.re(ur'(\d{4})-(\d{2})-(\d{2})')
        sysdate = "".join([year, month, day])

        # htmlまるごとも保存しておきたい
        filename = "log/" + sysdate + \
                   "/ranking_force.html"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'wb') as f:
            f.write(response.body)


class ForceRankParser():

    def parse(self, body):

        sl = Selector(text=body)

        # 武家の順位と使用率を取得したい
        rankings = []
        for tr in sl.xpath("//div[@id='main-inner']/table//tr[1]"):
            rank = tr.xpath("td[1]/text()").re(ur"■(\d+)位")
            if not rank:
                continue
            buke = dict()
            buke['rank'] = rank[0].strip()
            buke['name'] = tr.xpath("td[2]/text()").extract()[0].strip()
            buke['ratio'] = tr.xpath("td[3]/text()").extract()[0].strip().replace("%", "")
            rankings.append(buke)

        for buke in rankings:
            print u"/".join(buke.itervalues)
