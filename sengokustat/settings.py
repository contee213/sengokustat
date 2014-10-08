# -*- coding: utf-8 -*-

# Scrapy settings for sengokustat project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
from ConfigParser import SafeConfigParser

BOT_NAME = 'sengokustat'

SPIDER_MODULES = ['sengokustat.spiders']
NEWSPIDER_MODULE = 'sengokustat.spiders'
DOWNLOAD_DELAY = 1
ROBOTSTXT_OBEY = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sengokustat (+http://www.yourdomain.com)'

# .NET ACCOUNT

_sengoku_filebase = os.path.dirname(os.path.abspath(__file__))
_sengoku_filename = os.path.normpath(os.path.join(_sengoku_filebase, '../sengoku.cfg'))

_config = SafeConfigParser()
_config.read(_sengoku_filename)

NET_ID = _config.get('account', 'id')
NET_PASS = _config.get('account', 'pass')