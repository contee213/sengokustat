# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
player
~~~~~~~~~~~~~~

file commment here.

"""

import os, re, urlparse
from scrapy import Spider, FormRequest, Request, Selector

class RankerDeckSpider(Spider):

    name="deck"

    allowed_domains = ["pc.sengoku-taisen.com"]

    def start_requests(self):
        return [FormRequest("http://pc.sengoku-taisen.com/Login.htm",
                                   formdata={'account': 'contee44', 'password': 'y84m6d29'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        for x in xrange(1, 101):
            yield Request(url="http://pc.sengoku-taisen.com/free/ranking/ranking_player_deck.html?s=" + str(x)
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
        filename = "log/" + sysdate + "/deck"\
                   "/ranking_player_deck" + "_" + qs['s'][0] + ".html"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'wb') as f:
            f.write(response.body)

class RankerDeckParser():

    def parse(self, body):

        s_body = Selector(text=body)

        rankings = []
        for table in s_body.xpath("//div[@id='main-inner']/table"):
            player = dict()
            s_player = table.xpath("tr[1]/td[1]") # .extract()[0].encode('utf-8').strip()
            s_rank = s_player.xpath("b/text()").re(ur"第(\d+)位")
            if s_rank:
                player[u'rank'] = s_rank[0]
                player[u'name'] = s_player.xpath("font[1]/text()").extract()[0]
                title = s_player.xpath("string(font[2])").extract()[0].strip()
                title_match = re.search(ur"【(.*?)／(.*?)】", title)
                player[u'class'] = title_match.group(1)
                player[u'title'] = title_match.group(2)

                # 二行目以降
                player[u'score'] = table.xpath("string(tr[3]/td[1])").re(ur"戦働:(\d+)")[0]
                player[u'prefecture'] = table.xpath("string(tr[4]/td[1])").re(ur"都道府県:(.+)")[0]
                player[u'store'] = table.xpath("string(tr[5]/td[1])").re(ur"店舗名:\n\s*?(\S+.*)")[0]
                player[u'ranking_transition'] = table.xpath("string(tr[6]/td[1])").re(ur"順位変動:\n\s*?(\S+.*)")[0]

                for card in table.xpath("tr[7]/td[1]/span/text()").extract():
                    print card.strip()

                rankings.append(player)

        for player in rankings:
            print u"/".join(player.itervalues())