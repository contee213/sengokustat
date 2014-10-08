# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
council
~~~~~~~~~~~~~~

file commment here.

"""

import os, re, json
from datetime import datetime, timedelta
from scrapy import Spider, FormRequest, Request

update_time_list = (u"0430", u"1000", u"1100", u"1200", u"1300", u"1400", u"1500", u"1600", u"1700"
u"1800", u"1900", u"2000", u"2030", u"2100", u"2200", u"2300")

class CouncilDataSpider(Spider):

    name="council"

    allowed_domains = ["pc.sengoku-taisen.com"]

    def start_requests(self):
        return [FormRequest("http://pc.sengoku-taisen.com/Login.htm",
                                   formdata={'account': 'contee44', 'password': 'y84m6d29'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        return Request(url="http://pc.sengoku-taisen.com/members/player/council/council_data.json"
         , callback=self.parse_page)

    def parse_page(self, response):

        # json
        jd = json.loads(response.body)

        # "next_update": "09/27 04:30",
        now = datetime.now()
        mo, d, h, mi  = re.match(r"(\d{2})/(\d{2}) (\d{2}):(\d{2})",
                                 jd['council']['common']['next_update']).groups()
        next_update = datetime(now.year, int(mo), int(d), int(h), int(mi))
        # 10時未満の更新は先日分のデータ
        if int(h) < 10:
            st = next_update + timedelta(days=-1)
        else:
            st = next_update
        sysdate = st.strftime("%Y%m%d")
        next_period = st.strftime("%H%M")
        now_period = update_time_list[update_time_list.index(next_period) - 1]

        # responseも保存しておきたい
        filename = "log/" + sysdate + \
                   "/council/council_data" + "_" + now_period + ".json"
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'wb') as f:
            f.write(response.body)
