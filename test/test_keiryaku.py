# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
test_keiryaku
~~~~~~~~~~~~~~

file commment here.

"""

import unittest

import os
import sys
sys.path.append('..')

from sengokustat.spiders.master import keiryaku
from scrapy.http import HtmlResponse

class test_keiryaku(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_keiryaku_data(self):

        with open("../log/master/keiryaku_data.html", "r") as f:
            response = HtmlResponse(encoding='cp932',
                                    url='http://pc.sengoku-taisen.com/members/datalist/keiryaku/data.html?p=1234',
                                    body=f.read())
            spider = keiryaku.KeiryakuSpider()
            spider.parameters = dict()
            categories = dict()
            categories['1234'] = '2'
            spider.parameters['category'] = categories
            spider.parse_page(response=response)

    @unittest.skipIf('SKIP_SLOW_TESTS' in os.environ, 'Requested fast tests')
    def test_XXX_Slow_Test_Name(self):
        pass
        # raise NotImplementedError('Insert test code here.')

if __name__ == '__main__':
    unittest.main()