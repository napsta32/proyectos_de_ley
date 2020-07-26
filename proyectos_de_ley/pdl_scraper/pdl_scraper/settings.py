# -*- coding: utf-8 -*-

# Scrapy settings for pdl_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('.')))
print(sys.path)
# Do not forget the change iCrawler part based on your project name
os.environ['DJANGO_SETTINGS_MODULE'] = 'proyectos_de_ley.settings.local'

# This is required only if Django Version > 1.8
import django
django.setup()

LEGISLATURE = '2016'

BOT_NAME = 'pdl_scraper'

SPIDER_MODULES = ['pdl_scraper.spiders']
NEWSPIDER_MODULE = 'pdl_scraper.spiders'

ITEM_PIPELINES = {
    'pdl_scraper.pipelines.PdlScraperPipeline': 300,
    'pdl_scraper.pipelines.SeguimientosPipeline': 400,
    'pdl_scraper.pipelines.IniciativasPipeline': 500,
    'pdl_scraper.pipelines.PdlPdfurlPipeline': 600,
    'pdl_scraper.pipelines.UpdaterPipeline': 700,
    'pdl_scraper.pipelines.ExpedientePipeline': 800,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'pdl_scraper (+http://www.yourdomain.com)'
# be nice
CONCURRENT_REQUESTS = 10
CONCURRENT_REQUESTS_PER_DOMAIN = 10
DOWNLOAD_DELAY = 2


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
}
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36"

LOG_LEVEL = 'DEBUG'
LOG_ENABLED = True
