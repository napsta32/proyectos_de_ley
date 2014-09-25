# -*- coding: utf-8 -*-
from datetime import datetime
import http.cookiejar
import re
import urllib.request

from bs4 import BeautifulSoup
from optparse import make_option
import short_url
import socks
import socket

from django.core.management.base import BaseCommand, CommandError

from pdl.models import Proyecto
from pdl.models import Slug
from pdl.models import Seguimientos
from pdl.views import convert_name_to_slug


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
                    choices=['True', 'False'],
                    ),
        make_option('-d',
                    '--debug',
                    action='store_true',
                    dest='debug',
                    default=False,
                    help='Usar cuando se ejecuten tests.',
                    ),
    )

    def handle(self, *args, **options):
        # print(options)
        url_inicio = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/' \
                     'CLProLey2011.nsf/PAporNumeroInverso?OpenView'
        self.urls = []
        self.mysocket = ""
        self.legislatura = "2011"

        if options['tor'] is False:
            raise CommandError("Usar argumento --tor True/False")
        elif options['tor'] == 'True':
            self.tor = True
        elif options['tor'] == 'False':
            self.tor = False

        if options['full_scrapping'] is True:
            # Do full scrapping since 2011-08-27
            # Loop 100 to 3900 to get from 0001/2011-CR
            for i in range(100, 3900, 100):
                self.urls.append(url_inicio + "&Start=" + str(i))
        else:
            # Scrape only first page that has around 100 items
            self.urls.append(url_inicio)

        if 'debug' in options and options['debug'] is not True:
            # Do scrapping
            # ============
            for url in self.urls:
                print(">> TOR: ", self.tor)
                soup = self.get(url)
                doc_links = self.extract_doc_links(soup)
                for obj in doc_links:
                    print("Working on %s:" % obj['numero_proyecto'])
                    obj = self.gather_all_metadata(obj)
                    if obj != "already in database":
                        # save
                        self.save_project(obj)
                        self.save_slug(obj)
                        print("Saved %s" % obj['codigo'])
                    else:
                        print("\t" + obj)

                    print("Working on seguimientos")
                    seguimientos_soup = self.get(obj['seguimiento_page'])
                    seguimientos = self.get_seguimientos(seguimientos_soup)
                    if seguimientos != '':
                        self.save_seguimientos(seguimientos, obj['codigo'])

                    if 'test' in options and options['test'] is True:
                        break

    def get(self, url):
        """
        Does a HTTP request for a webpage and returns a BeautifulSoup
        object."""
        if self.tor is True:
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.setdefaulttimeout(10)  # 10 seconds for timeout
            socket.socket = socks.socksocket
            self.mysocket = socket.socket.default_proxy
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj))
        req = opener.open(url)
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
                    if title is not None:
                        our_links.append({'numero_proyecto': numero_proyecto,
                                          'titulo': title,
                                          'seguimiento_page': our_link},
                                         )
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
            if item['name'] == "CodIni":
                this_metadata['codigo'] = item['value']
            if item['name'] == "CodIni_web_1":
                this_metadata['numero_proyecto'] = item['value']
            if item['name'] == "fechapre":
                this_metadata['fecha_presentacion'] = item['value']
            if item['name'] == "DesPropo":
                this_metadata['proponente'] = item['value']
            if item['name'] == "DesGrupParla":
                this_metadata['grupo_parlamentario'] = item['value']
            if item['name'] == "SumIni":
                this_metadata['titulo'] = item['value']
            if item['name'] == "NomCongre":
                this_metadata['congresistas'] = self.parse_names(item['value'])
            if item['name'] == "CodIniSecu":
                this_metadata['iniciativas_agrupadas'] = item['value']
            if item['name'] == "NumLey":
                this_metadata['numero_de_ley'] = item['value']
            if item['name'] == "TitLey":
                this_metadata['titulo_de_ley'] = item['value']
            if item['name'] == "NombreDeLaComision":
                this_metadata['nombre_comision'] = item['value']

        exp = 'http://www2.congreso.gob.pe/sicr/tradocestproc' \
              '/Expvirt_2011.nsf/visbusqptramdoc/'
        expediente = "%s%s%s" % (exp,
                                 this_metadata['codigo'],
                                 '?opendocument',
                                 )
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
        for the code in the PDF URL address.

        Some PDF filenames might have funny characters:
            - P´L03812220914.pdf
        """
        pdf_soup = self.get(expediente)

        pattern = re.compile("\$FILE/.+" + str(codigo) + "[0-9]+\.pdf$")
        for i in pdf_soup.find_all("a"):
            if re.search(pattern, i['href']):
                my_pdf_link = str(i['href'])
                return my_pdf_link
        # Algunos proyectos de ley no tienen link hacia PDFs
        return ''

    def get_seguimientos(self, soup):
        """Parses a ``seguimiento_page`` as BeautifulSoup object and returns
        a list of events extracted from the ``Seguimiento:`` section.

        :param: BeautifulSoup object
        :return: list of tuples (date object, event)
        """
        events = ''
        for i in soup.find_all(width='112'):
            if i.text == 'Seguimiento:':
                events = i.next_sibling.text

        if not events or events.strip() == '':
            return ''

        events_list = events.split("\n")

        # avoid dots when appending to list, it is more efficient:
        # http://bit.ly/1sVevk6
        new_list = []
        append = new_list.append
        for i in events_list:
            append(self.convert_line_to_date_event_tuple(i))
        return new_list

    def save_seguimientos(self, seguimientos, codigo):
        """
        Try to save a list of tuples to Seguimientos model if they don't
        exist already.
        :param seguimientos: list of tuples (date, event)
        :param codigo: codigo for Proyecto
        :return:
        """
        proyecto = Proyecto.objects.filter(codigo=codigo)[0]
        seguimientos_to_save = []
        append = seguimientos_to_save.append

        for i in seguimientos:
            try:
                Seguimientos.objects.get(
                    fecha=i[0],
                    evento=i[1],
                    proyecto=proyecto,
                )
            except Seguimientos.DoesNotExist:
                # not in database
                b = Seguimientos(fecha=i[0], evento=i[1], proyecto=proyecto)
                append(b)
        Seguimientos.objects.bulk_create(seguimientos_to_save)

    def convert_line_to_date_event_tuple(self, i):
        """
        :param i: string line for each event of Seguimiento
        :return: a tuple (date object, event string)
        """
        i_strip = i.strip()
        res = re.search('^([0-9]{2}/[0-9]{2}/[0-9]{4})\s+(.+)', i_strip)
        if res:
            d = datetime.strptime(res.groups()[0], '%d/%m/%Y')
            event = re.sub('\s+', ' ', res.groups()[1])
            return(datetime.date(d), event)

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
        try:
            mydate = datetime.date(datetime.strptime(string, '%m/%d/%Y'))
        except ValueError:
            mydate = datetime.date(datetime.strptime(string, '%d/%m/%Y'))
        return mydate

    def gather_all_metadata(self, obj):
        """
        Uses several functions to pull all metadata for a certain proyecto.
        :param obj: dict {'numero_proyecto', 'titulo', 'seguimiento_page'}
        :return: dict containing all needed metadata.
        """
        obj = self.extract_metadata(obj)
        if obj != "already in database":
            obj['short_url'] = self.create_shorturl(obj['codigo'])
            obj['fecha_presentacion'] = self.fix_date(
                obj['fecha_presentacion'],
            )
            return obj
        else:
            return "already in database"

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

    def save_slug(self, obj):
        for congre in obj['congresistas'].split(';'):
            congre = congre.strip()
            congre_slug = dict(nombre=congre)
            if congre is not None and congre != '':
                slug = convert_name_to_slug(congre)
                congre_slug['slug'] = slug

                try:
                    Slug.objects.get(slug=congre_slug['slug'])
                    return "slug already in database"
                except Slug.DoesNotExist:
                    b = Slug(**congre_slug)
                    b.save()
