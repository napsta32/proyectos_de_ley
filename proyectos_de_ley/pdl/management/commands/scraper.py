# -*- coding: utf-8 -*-
from optparse import make_option
import codecs
import datetime
from datetime import date
from datetime import timedelta as td
import hashlib
import json
import re
import urllib.request

import os
from random import randint
from optparse import make_option
import requests
import socks
import socket
from bs4 import BeautifulSoup
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from pdl.models import Proyecto


class Command(BaseCommand):
    help = 'Hace scrapping de las páginas del servidor del Congreso.'
    option_list = BaseCommand.option_list + (
        make_option('-f',
                    '--full',
                    action='store_true',
                    dest='full_scrapping',
                    default=False,
                    help='Hace un scrapping total desde 27 de Julio del 2011.',
                    ),
    )

    def handle(self, *args, **options):
        url_inicio = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/' \
                     'CLProLey2011.nsf/PAporNumeroInverso?OpenView'
        self.urls = []

        if options['full_scrapping'] is True:
            # Do full scrapping since 2011-08-27
            # Loop 100 to 3900 to get from 0001/2011-CR
            for i in range(100, 3900, 100):
                self.urls.append(url_inicio + "&Start=" + str(i))
        else:
            # Scrape only first page that has around 100 items
            self.urls.append(url_inicio)

    def get(self, url):
        """Does a HTTP request for a webpage and returns a BeautifulSoup
        object. By default uses the *tor* network."""
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        req = urllib.request.urlopen(url)
        html = req.read()
        soup = BeautifulSoup(html)
        return soup

    def extract_doc_links(self, soup):
        """Parses a soup object from the Congress front pages and returns a
        list of objects containing link and title for each project.
        That link is actually the *Seguimiento* URL."""
        our_links = []
        for link in soup.find_all("a"):
            if re.search("[0-9]{5}/[0-9]{4}", link.get_text()):
                href = link.get("href")
                title = link.get("title")
                if href.endswith("ocument"):
                   our_link = "http://www2.congreso.gob.pe"
                   our_link += "/Sicr/TraDocEstProc/CLProLey2011.nsf/"
                   our_link += href
                   our_links.append({'titulo': title, 'seguimiento_page':
                       our_link})
        return our_links
