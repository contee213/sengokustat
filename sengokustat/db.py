# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
db
~~~~~~~~~~~~~~

file commment here.

"""

from pymongo import MongoClient

client = MongoClient("192.168.33.10")
db = client['sengokustat']