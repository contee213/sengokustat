# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
player
~~~~~~~~~~~~~~

file commment here.

"""

import os, re
from scrapy import Spider, FormRequest, Request, Selector
from ..items import BushoCard

class CardRankSpider(Spider):

    name="card"

    allowed_domains = ["pc.sengoku-taisen.com"]

    def start_requests(self):
        return [FormRequest("http://pc.sengoku-taisen.com/Login.htm",
                                   formdata={'account': 'contee44', 'password': 'y84m6d29'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        return Request(url="http://pc.sengoku-taisen.com/free/ranking/ranking_card.html?s=1&e=200"
         , callback=self.parse_page)

    def parse_page(self, response):

        # 2014-09-26更新といった文字列を取得したい
        updated_time = response.xpath("//div[@id='main-inner']/text()")
        year, month, day = updated_time.re(ur'(\d{4})-(\d{2})-(\d{2})')
        sysdate = "".join([year, month, day])

        # htmlまるごとも保存しておきたい
        filename = "log/" + sysdate + \
                   "/ranking_card.html"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'wb') as f:
            f.write(response.body)

        parser = CardRankParser()
        for item in parser.parse(response.body):
            yield item


class CardRankParser():

    def parse(self, body):

        rankings = []

        s_body = Selector(text=body)

        t_main = s_body.xpath("string(//div[@id='main-inner'])").extract()[0]
        t_main = "\n".join([line for line in t_main.strip().split("\n") if line])

        # ('先頭のゴミ', 'rank', 'point','name', 'win_rate', 'kill_count',
        #  'skill_count', 'inner_rank', 'ranking_transition', '', 'rank'...)
        l_card_ranks = re.split(ur"第(\d*?)位 (\d*?)pt.*?■(.*?)\n.*?(\d+\.\d+)％\n"
                           ur".*?(\d+\.\d+)部隊.*?(\d+\.\d+)回\n.*?武家別ﾗﾝｷﾝｸﾞ:(\d+)位\n"
                           ur"週間順位変動\n(.*?)", t_main, flags=re.DOTALL)
        l_card_ranks = l_card_ranks[1:]

        # 9個で周期的なリストになってるので分割したい
        _sub_rankings = []
        for i in (range(len(l_card_ranks)))[::9]:
            _sub_rankings.append(l_card_ranks[i:i+9])

        for e in _sub_rankings:
            card_data = BushoCard()
            card_data[u'rank'] = e[0]
            card_data[u'point'] = e[1]
            card_data[u'name'] = e[2]
            card_data[u'win_rate'] = e[3]
            card_data[u'kill_count'] = e[4]
            card_data[u'skill_count'] = e[5]
            card_data[u'inner_rank'] = e[6]
            card_data[u'ranking_transition'] = e[7]
            rankings.append(card_data)
            yield card_data

        # for card_data in rankings:
        #     print(u"{0:0>3}".format(card_data[u'rank']) + u" : " + u"{0:<10}".format(card_data[u'name'])
        #         + u" - " + card_data[u'win_rate'])
