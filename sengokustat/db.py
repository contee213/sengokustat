# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
db
~~~~~~~~~~~~~~

file commment here.

"""

from pymongo import MongoClient

client = MongoClient("xxx.xxx.xxx.xxx")
db = client['sengokustat']