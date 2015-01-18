# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
keiryaku
~~~~~~~~~~~~~~

計略詳細取得

"""

import os, re
from scrapy import Spider, FormRequest, Request, Selector
from sengokustat.settings import NET_ID, NET_PASS
from sengokustat.db import db

class KeiryakuSpider(Spider):

    name="keiryaku"

    allowed_domains = ["pc.sengoku-taisen.com"]

    def start_requests(self):
        self.parameters = dict()
        return [FormRequest("http://pc.sengoku-taisen.com/Login.htm",
                                   formdata={'account': NET_ID, 'password': NET_PASS},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback

        # 全消去
        db.keiryaku.drop()

        categories = dict()
        with open('log/master/keiryaku_list.txt', 'r') as f:
            for line in f:
                category, net_keiryaku_id = line.rstrip(u'\n').split(u'\t')
                categories[net_keiryaku_id] = category
        self.parameters['category'] = categories

        for net_keiryaku_id in categories.iterkeys():
            yield Request(url="http://pc.sengoku-taisen.com/members/datalist/keiryaku/data.html?p="
                              + net_keiryaku_id
                , callback=self.parse_page)


    def parse_page(self, response):

        keiryaku_data = dict()
        div_selector = [div for div in response.xpath("//div[@id='main-inner']/div")]

        net_keiryaku_id = re.search(ur"p=(\d+)", response.url).group(1)

        keiryaku_data['net_keiryaku_id'] = net_keiryaku_id
        keiryaku_data['category'] = self.parameters['category'][net_keiryaku_id]

        # 計略情報
        keiryaku_data['name'] = div_selector[0].xpath("string(.)").re(ur"〔(.*?)〕")[0]

        t_detail = div_selector[1].xpath("string(.)").re(ur"\S+")
        keiryaku_data['shiki'] = re.search(ur":(.*)", t_detail[0]).group(1)
        keiryaku_data['time_type'] = re.search(ur":(.*)", t_detail[1]).group(1)
        keiryaku_data['range_image_url'] = div_selector[2].xpath("img/@src").extract()[0]

        t_explain = div_selector[3].xpath("string(.)").extract()[0]
        t_explain = u"\n".join([line.strip() for line in t_explain.split(u"\n") if line])
        keiryaku_data['detail'] = re.search(ur"説明:(?P<sengoku_name>.*)\n", t_explain).group(1)

        db.keiryaku.insert(keiryaku_data)


