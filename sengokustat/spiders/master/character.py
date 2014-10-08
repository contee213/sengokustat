# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
character
~~~~~~~~~~~~~~

file commment here.

"""

import os, re
from scrapy import Spider, FormRequest, Request, Selector
from sengokustat.db import db

class CharacterSpider(Spider):

    name="character"

    allowed_domains = ["pc.sengoku-taisen.com"]

    def start_requests(self):
        self.parameters = dict()
        return [FormRequest("http://pc.sengoku-taisen.com/Login.htm",
                                   formdata={'account': 'contee44', 'password': 'y84m6d29'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback

        # 全消去
        db.busho.drop()

        card_version = dict()
        with open('log/master/character_list.txt', 'r') as f:
            for line in f:
                version, net_card_id = line.rstrip(u'\n').split(u'\t')
                card_version[net_card_id] = version
        self.parameters['card_version'] = card_version

        for net_card_id in card_version.iterkeys():
            yield Request(url="http://pc.sengoku-taisen.com/members/datalist/character/data.html?p=" + net_card_id
                , callback=self.parse_page)

    def parse_page(self, response):

        chara_data = dict()
        div_selector = [div for div in response.xpath("//div[@id='main-inner']/div")]

        net_card_id = re.search(ur"p=(\d+)", response.url).group(1)

        chara_data['net_card_id'] = net_card_id
        chara_data['game_version'] = self.parameters['card_version'][net_card_id]

        # 所属武家ー武将名
        chara_data['buke'], chara_data['card_id'], card_name = div_selector[0].xpath("string(.)").re(ur"\S+")
        chara_data['image_url'] = div_selector[1].xpath("img/@src").extract()[0]
        # UC織田信長 -> UC/織田信長
        m = re.match(ur"(EX|SSR|SS|SR|BSS|R|UC|C).*?", card_name)
        chara_data['card_name'] = card_name
        chara_data['rarity'] = m.group(1)

        # 武将スペック
        t_spec = div_selector[2].xpath("string(.)").re(ur"\S+")
        chara_data['heisyu'] = t_spec[0]
        chara_data['cost'] = re.search(ur"(\d+\.*\d*)", t_spec[1]).group(1)
        chara_data['buryoku'] = re.search(ur"(\d+)", t_spec[2]).group(1)
        chara_data['tousotsu'] = re.search(ur"(\d+)", t_spec[3]).group(1)
        tokugi_str = re.search(ur":(.*)", t_spec[4]).group(1)
        if tokugi_str.find(u"なし") < 0:
            chara_data['tokugi'] = list(tokugi_str)
        else:
            chara_data['tokugi'] = []

        # 計略
        keiryaku = dict()
        keiryaku['net_id'] = div_selector[2].xpath("./a/@href").re("\?p=(\d+)")[0]
        keiryaku['name'], keiryaku['shiki'] = re.search(ur"(.*?):必要士気(\d*)", t_spec[5]).groups()
        keiryaku['range_image_url'] = div_selector[3].xpath("img/@src").extract()[0]
        chara_data['keiryaku'] = keiryaku['name']

        # 武将列伝
        t_retuden = div_selector[4].xpath("string(.)").extract()[0]
        t_retuden = u"\n".join([line.strip() for line in t_retuden.split(u"\n") if line])
        chara_data['sengoku_name'] = re.search(
            ur"戦国名:(?P<sengoku_name>.*)\n", t_retuden).group(1)
        chara_data['birth_year'], chara_data['death_year'] = re.search(
            ur"生没年:(?P<birth_year>.*?)[\u301c|\uff5e](?P<death_year>.*)", t_retuden).groups()
        chara_data['buke'], chara_data['sub_buke'] = re.search(
            ur"武家:(?P<buke>[^\uff08\uff09\n]*)[\uff08]?(?P<sub_buke>.*?)[\uff09]?\n", t_retuden).groups()
        chara_data['syussin'], chara_data['now_pref'], chara_data['retuden'] = re.search(
            ur"出身地:(?P<syussin>[^\uff08\uff09]*)[\uff08]?(?P<now_pref>.*?)[\uff09]?\n"
            ur"(?P<retuden>[\s\S]*$)", t_retuden).groups()

        # イラストレーター
        chara_data['illustrator'] = response.xpath("string(//div[@id='main-inner'])").re(ur"ｲﾗｽﾄﾚｰﾀｰ:(.*)")[0]

        # for k, v in chara_data.iteritems():
        #      print k, v

        db.busho.insert(chara_data)