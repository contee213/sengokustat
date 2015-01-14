# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
esimport
~~~~~~~~~~~~~~

file commment here.

"""

from datetime import datetime
from elasticsearch import Elasticsearch

from pymongo import MongoReplicaSetClient

c = MongoReplicaSetClient("192.168.33.10:27017", replicaSet='rs0')
db = c['sengokustat']

# es = Elasticsearch()

# res = es.get(index="bank", doc_type='account', id=1)
# print(res['_source'])

for k in db.keiryaku.find():
    print(k['name'])