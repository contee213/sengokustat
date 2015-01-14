# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
relation
~~~~~~~~~~~~~~

file commment here.

"""

from sengokustat.db import db

for busho in db.busho.find():
    # print(busho['keiryaku'])
    keiryaku = db.keiryaku_0302B.find_one({"name" : busho['keiryaku']})
    # print(keiryaku)
    # if 'busho' in keiryaku:
    #    keiryaku['busho'].append(busho)
    # else:
    #    keiryaku['busho'] = [busho]
    busho['keiryaku_data'] = keiryaku
    #db.keiryaku.save(keiryaku)
    db.busho.save(busho)