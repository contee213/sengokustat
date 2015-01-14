# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
db
~~~~~~~~~~~~~~

file commment here.

"""

from pymongo import MongoClient

client = MongoClient("54.65.219.104")
db = client['sengokustat']