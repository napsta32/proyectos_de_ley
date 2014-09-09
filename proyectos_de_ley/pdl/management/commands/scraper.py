# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
import re
import urllib.request

from bs4 import BeautifulSoup
from optparse import make_option
import short_url
import socks
import socket

from django.core.management.base import BaseCommand, CommandError

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
        make_option('-t',
                    '--tor',
                    action='store',
                    dest='tor',
                    default=False,
                    help='Hace pedidos HTTP detrás de *tor*. Usar --tor '
                         'True/False',
                    ),
    )

    def handle(self, *args, **options):
        url_inicio = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/' \
                     'CLProLey2011.nsf/PAporNumeroInverso?OpenView'
        self.urls = []
        self.legislatura = "2011"

        if 'tor' not in options:
            raise CommandError("Usar argumento --tor True/False")
        elif options['tor'] is True:
            self.tor = True
        elif options['tor'] is False:
            self.tor = False

        if options['full_scrapping'] is True:
            # Do full scrapping since 2011-08-27
            # Loop 100 to 3900 to get from 0001/2011-CR
            for i in range(100, 3900, 100):
                self.urls.append(url_inicio + "&Start=" + str(i))
        else:
            # Scrape only first page that has around 100 items
            self.urls.append(url_inicio)

    def get(self, url):
        """
        Does a HTTP request for a webpage and returns a BeautifulSoup
        object."""
        if self.tor is True:
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.setdefaulttimeout(10) # 10 seconds for timeout
            socket.socket = socks.socksocket
        req = urllib.request.urlopen(url)
        html = req.read()
        soup = BeautifulSoup(html)
        return soup

    def extract_doc_links(self, soup):
        """
        Parses a soup object from the Congress front pages and returns a
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
            #if item['name'] == "DesGrupParla":
                #metadata['grupo_parlamentario'] = item['value']
            #if item['name'] == "NombreDeLaComision":
                #metadata['comision'] = item['value']
            if item['name'] == "NomCongre":
                this_metadata['congresistas'] = self.parse_names(item['value'])
            if item['name'] == "CodIni":
                this_metadata['codigo'] = item['value']
            if item['name'] == "fechapre":
                this_metadata['fecha_presentacion'] = item['value']
        expediente = 'http://www2.congreso.gob.pe/sicr/tradocestproc' \
                      '/Expvirt_2011.nsf/visbusqptramdoc/'
        expediente += this_metadata['codigo'] + '?opendocument'
        this_metadata['expediente'] = expediente
        this_metadata['pdf_url'] = self.extract_pdf_url(
                                                    expediente,
                                                    this_metadata['codigo'],
                                                       )
        this_metadata['seguimiento_page'] = obj['seguimiento_page']
        return this_metadata

    def extract_pdf_url(self, expediente, codigo):
        """
        Try to get the URL for PDF of project from the "expediente" page.
        Such page might have many PDFs. Try to get the right one by looking
        for the code in the PDF URL address."""
        pdf_soup = self.get(expediente)

        pattern = re.compile("/PL" + str(codigo) + "[0-9]+\.pdf$")
        for i in pdf_soup.find_all("a"):
            if re.search(pattern, i['href']):
                my_pdf_link = str(i['href'])
                return my_pdf_link
        # Algunos proyectos de ley no tienen link hacia PDFs
        return "none"

    def parse_names(self, string):
        """
        :param string: Person names separated by commas.
        :return: String of person names separated by colons and family names
                 separated from given names by commas.
        """
        names = ""
        for i in string.split(","):
            i = re.sub("\s{2}", ", ", i)
            names += i + "; "
        names = re.sub(";\s$", "", names)
        return names

    def create_shorturl(self, codigo):
        """
        Use "legislatura" and codigo to build a short url.
        :param codigo: Code for Proyecto de ley "03774"
        :return: 4aw8ym
        """
        mystring = self.legislatura + codigo
        url = short_url.encode_url(int(mystring))
        return url

    def fix_date(self, string):
        """
        Takes an string date from Proyecto and converts it to Date object.
        :param string: "08/28/2014"
        :return: date(2014, 08, 28)
        """
        mydate = datetime.date(datetime.strptime(string, '%m/%d/%Y'))
        return mydate

    def gather_all_metadata(self, obj):
        """
        Uses several functions to pull all metadata for a certain proyecto.
        :param obj: dict {'numero_proyecto', 'titulo', 'seguimiento_page'}
        :return: dict containing all needed metadata.
        """
        obj = self.extract_metadata(obj)
        obj['short_url'] =self.create_shorturl(obj['codigo'])
        obj['fecha_presentacion'] = self.fix_date(obj['fecha_presentacion'])
        return obj

    def save_project(self, obj):
        """
        Saves all metadata for our project into our database.
        """
        try:
            Proyecto.objects.get(numero_proyecto=obj['numero_proyecto'])
            return "already in database"
        except Proyecto.DoesNotExist:
            # not in database
            b = Proyecto(**obj)
            b.save()
