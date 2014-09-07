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
        socket.setdefaulttimeout(10) # 10 seconds for timeout
        socket.socket = socks.socksocket
        req = urllib.request.urlopen(url)
        html = req.read()
        soup = BeautifulSoup(html)
        return soup

    def extract_doc_links(self, soup):
        """Parses a soup object from the Congress front pages and returns a
        list of objects containing project_number, link and title for each
        project.
        That link is actually the *Seguimiento* URL."""
        our_links = []
        for link in soup.find_all("a"):
            if re.search("[0-9]{5}/[0-9]{4}", link.get_text()):
                numero_proyecto = link.get_text()
                href = link.get("href")
                title = link.get("title")
                if href.endswith("ocument"):
                   our_link = "http://www2.congreso.gob.pe"
                   our_link += "/Sicr/TraDocEstProc/CLProLey2011.nsf/"
                   our_link += href
                   our_links.append({'numero_proyecto': numero_proyecto,
                                     'titulo': title,
                                     'seguimiento_page': our_link})
        return our_links

    def extract_metadata(self, obj):
        """
        Using the ``numero_proyecto`` finds out if already in database. If
        false, it will try to download the metadata for such a project and
        return it. If we already have that data in the database, will will
        return "done_already"
        :param obj: {'numero_proyecto', 'titulo', 'seguimiento_page'}
        :return: metadata for proyecto de ley, "done_already"
        """
        try:
            Proyecto.objects.get(numero_proyecto=obj['numero_proyecto'])
            return "already in database"
        except Proyecto.DoesNotExist:
            # not in database
            pass

        project_soup = self.get(obj['seguimiento_page'])

        this_metadata = dict()
        for item in project_soup.find_all("input"):
            if item['name'] == "SumIni":
                this_metadata['titulo'] = item['value']
            if item['name'] == "CodIni_web_1":
                this_metadata['numero_proyecto'] = item['value']
                #print "* numero_proyecto: %s" % this_metadata['numero_proyecto']
            #if item['name'] == "DesGrupParla":
                #metadata['grupo_parlamentario'] = item['value']
            #if item['name'] == "NombreDeLaComision":
                #metadata['comision'] = item['value']
            #if item['name'] == "NomCongre":
                #this_metadata['congresistas'] = parse_names(item['value'])
            if item['name'] == "CodIni":
                this_metadata['codigo'] = item['value']
            if item['name'] == "fechapre":
                this_metadata['fecha_presentacion'] = item['value']
                #print "* fecha_presentacion: %s" % this_metadata['fecha_presentacion']
        link_to_pdf = 'http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/' + this_metadata['codigo'] + '?opendocument'
        try:
            this_metadata['link_to_pdf'] = link_to_pdf
            print(this_metadata['link_to_pdf'])

            #this_metadata['pdf_url'] = extract_pdf_url(link_to_pdf)
        except:
            print("no link to pdf")

        return this_metadata
