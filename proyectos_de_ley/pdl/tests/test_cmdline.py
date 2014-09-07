#-*- encoding: utf-8 -*-
import codecs
import os

from bs4 import BeautifulSoup

from django.test import TestCase
from pdl.management.commands.scraper import Command


class ScrapperTest(TestCase):
    def setUp(self):
        self.congreso_url = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/' \
                       'CLProLey2011.nsf/PAporNumeroInverso?OpenView'
    def test_url1(self):
        """Test when user does not enter any argument for the scrapper."""
        options = dict(full_scrapping = False)
        scrapper_cmd = Command()
        scrapper_cmd.handle(**options)
        expected = self.congreso_url
        self.assertEqual(expected, scrapper_cmd.urls[0])

    def test_url2(self):
        """Test when user enter argument for full scrapping, since 20110727."""
        options = dict(full_scrapping = True)
        scrapper_cmd = Command()
        scrapper_cmd.handle(**options)
        expected_last = self.congreso_url + '&Start=3800'
        self.assertEqual(expected_last, scrapper_cmd.urls[-1])

    def test_get(self):
        scrapper_cmd = Command()
        soup = scrapper_cmd.get("http://www.bbc.com/news/")
        result = soup.title.get_text()
        expected = "BBC News - Home"
        self.assertEqual(result, expected)

    def test_extract_doc_links(self):
        scrapper_cmd = Command()
        expected = [
            {
            #'codigo': u'03774',
            #'numero_proyecto': '03774/2014-CR',
            #'link': None,
            #'link_to_pdf': 'http://www2.congreso.gob.pe/sicr/tradocestproc/'
                           #'Expvirt_2011.nsf/visbusqptramdoc/03774?opendocument'
            #'pdf_url': 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/'
                       #'Contdoc02_2011_2.nsf/d99575da99ebfbe305256f2e006d1cf0'
                       #'dbc9030966aac60905257d4a007b75d9/$FILE
                       # /PL03774050914.pdf',
            'titulo': u'Propone establecer los lineamientos para la promoc'
                      u'i\xf3n de la eficiencia y competitividad en la '
                      u'actividad empresarial del Estado, garantizando su '
                      u'aporte estrat\xe9gico para el desarrollo'
                      u' descentralizado y la soberan\xeda nacional.',
            'seguimiento_page': 'http://www2.congreso.gob.pe/Sicr/TraDocEst'
                                'Proc/CLProLey2011.nsf/Sicr/TraDocEstProc/'
                                'CLProLey2011.nsf/PAporNumeroInverso/96091'
                                '30B9871582F05257D4A00752301?opendocument',
            }
        ]

        html_folder = os.path.abspath(os.path.dirname(__file__))
        html_file = os.path.join(html_folder, "frontweb.html")
        with codecs.open(html_file, "r", "utf-8") as f:
            html = f.read()
            soup = BeautifulSoup(html)
            our_links = scrapper_cmd.extract_doc_links(soup)
        self.assertEqual(expected, our_links)

