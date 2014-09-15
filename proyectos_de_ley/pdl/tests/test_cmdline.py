# -*- encoding: utf-8 -*-
import codecs
from datetime import datetime
from datetime import date
import os
import unittest

from bs4 import BeautifulSoup

from django.test import TestCase
from pdl.management.commands.scraper import Command
from pdl.models import Proyecto


class ScrapperTest(TestCase):
    def setUp(self):
        args = ()
        options = {
            'settings': 'proyectos_de_ley.settings.local',
            'no_color': False, 'full_scrapping': False, 'verbosity': '1',
            'traceback': None, 'tor': 'False', 'debug': True,
            'pythonpath': None}
        self.congreso_url = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/' \
                            'CLProLey2011.nsf/PAporNumeroInverso?OpenView'
        self.scrapper_cmd = Command()
        self.scrapper_cmd.handle(self, *args, **options)
        self.maxDiff = None

    def test_tor1(self):
        args = ()
        options = {
            'settings': 'proyectos_de_ley.settings.local',
            'full_scrapping': False, 'verbosity': '2',
            'traceback': None, 'tor': 'False', 'debug': True,
            'pythonpath': None}
        scrapper_cmd = Command()
        scrapper_cmd.handle(*args, **options)
        result = scrapper_cmd.tor
        expected = False
        self.assertEqual(expected, result)

    @unittest.expectedFailure
    def test_tor2(self):
        """If user does not enter argument for tor, exit with error."""
        args = ()
        options = {
            'settings': 'proyectos_de_ley.settings.local',
            'full_scrapping': False, 'verbosity': '2',
            'traceback': None, 'debug': True,
            'pythonpath': None}
        scrapper_cmd = Command()
        scrapper_cmd.handle(*args, **options)

    @unittest.expectedFailure
    def test_tor3(self):
        args = ()
        options = {
            'settings': 'proyectos_de_ley.settings.local',
            'full_scrapping': False, 'verbosity': '2',
            'traceback': None, 'debug': True, 'tor': False,
            'pythonpath': None}
        scrapper_cmd = Command()
        scrapper_cmd.handle(*args, **options)

    @unittest.expectedFailure
    def test_scraping(self):
        args = ()
        options = {
            'settings': 'proyectos_de_ley.settings.local',
            'full_scrapping': False, 'verbosity': '2',
            'traceback': None, 'debug': False, 'test': True,
            'tor': 'False', 'pythonpath': None}
        scrapper_cmd = Command()
        scrapper_cmd.handle(*args, **options)
        res = Proyecto.objects.all()
        self.assertEqual(1, len(res))

        # Test when already in db
        scrapper_cmd = Command()
        scrapper_cmd.handle(*args, **options)
        res = Proyecto.objects.all()
        self.assertEqual(2, len(res))

    def test_url1(self):
        """Test when user does not enter any argument for the scrapper."""
        args = ()
        options = {
            'settings': 'proyectos_de_ley.settings.local',
            'full_scrapping': False, 'verbosity': '2',
            'traceback': None, 'tor': 'False', 'debug': True,
            'pythonpath': None}
        scrapper_cmd = Command()
        scrapper_cmd.handle(*args, **options)
        expected = self.congreso_url
        self.assertEqual(expected, scrapper_cmd.urls[0])

    def test_url2(self):
        """Test when user enter argument for full scrapping, since 20110727."""
        args = ()
        options = {
            'settings': 'proyectos_de_ley.settings.local',
            'full_scrapping': True, 'verbosity': '2',
            'traceback': None, 'tor': 'False', 'debug': True,
            'pythonpath': None}
        scrapper_cmd = Command()
        scrapper_cmd.handle(*args, **options)
        expected_last = self.congreso_url + '&Start=3800'
        self.assertEqual(expected_last, scrapper_cmd.urls[-1])

    def test_get1(self):
        soup = self.scrapper_cmd.get("http://aniversarioperu.me/")
        result = soup.title.get_text()
        expected = "Aniversario Peru"
        self.assertEqual(result, expected)

    @unittest.expectedFailure
    def test_get2(self):
        """Test if we get a tor proxy for get request when tor is TRUE."""
        options = {
            'settings': 'proyectos_de_ley.settings.local',
            'full_scrapping': False, 'verbosity': '2',
            'traceback': None, 'tor': 'True', 'debug': True,
            'pythonpath': None}
        new_scrapper_cmd = Command()
        new_scrapper_cmd.handle(**options)
        new_scrapper_cmd.get("http://aniversarioperu.me/")
        self.assertEqual(b'127.0.0.1', new_scrapper_cmd.mysocket[1])

    def test_extract_doc_links(self):
        expected = [{
            'numero_proyecto': '03774/2014-CR',
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
            our_links = self.scrapper_cmd.extract_doc_links(soup)
        self.assertEqual(expected, our_links)

    def test_extract_metadata1(self):
        obj = {'numero_proyecto': '03774/2014-CR', 'test': 'test',
               'titulo': 'hola',
               'seguimiento_page': 'http://aniversarioperu.me/utero/test_pdl/'
                                   'seguimiento_03774.html',
               }
        result = self.scrapper_cmd.extract_metadata(obj)
        expected = {
            'numero_proyecto': '03774/2014-CR',
            'codigo': '03774',
            'titulo': u'Propone establecer los lineamientos para la promoc'
                      u'i\xf3n de la eficiencia y competitividad en la '
                      u'actividad empresarial del Estado, garantizando su '
                      u'aporte estrat\xe9gico para el desarrollo'
                      u' descentralizado y la soberan\xeda nacional.',
            'fecha_presentacion': '05/09/2014',
            'expediente': 'http://www2.congreso.gob.pe/sicr/tradocestproc/'
                          'Expvirt_2011.nsf/visbusqptramdoc/03774?opendocu'
                          'ment',
            'congresistas': 'Dammert Ego Aguirre, Manuel Enrique Ernesto; '
                            'Lescano Ancieta, Yonhy; Merino De Lama, Manue'
                            'l; Guevara Amasifuen, Mesias Antonio; Mavila '
                            'Leon, Rosa Delsa; Mendoza Frisch, Veronika Fanny',
            'seguimiento_page': 'http://aniversarioperu.me/utero/test_pdl/'
                                'seguimiento_03774.html',
            'pdf_url': 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Cont'
                       'doc02_2011_2.nsf/d99575da99ebfbe305256f2e006d1cf0/'
                       'dbc9030966aac60905257d4a007b75d9/$FILE/PL037740509'
                       '14.pdf',
        }
        self.assertEqual(expected, result)

    def test_extract_metadata2(self):
        obj = {
            'numero_proyecto': '03774/2014-CR', 'titulo': 'hola',
            'seguimiento_page': 'http://aniversarioperu.me/utero/test_pdl/'
                                'seguimiento_03774.html',
            'test': 'test',
            'fecha_presentacion': datetime.now(),
        }
        b = Proyecto(numero_proyecto='03774/2014-CR', titulo='hola',
                     seguimiento_page=obj['seguimiento_page'],
                     fecha_presentacion=datetime.now())
        b.save()
        result = self.scrapper_cmd.extract_metadata(obj)
        self.assertEqual("already in database", result)

    def test_extract_pdf_url1(self):
        expediente = 'http://aniversarioperu.me/utero/test_pdl/expediente_' \
                     '02764.html'
        codigo = '02764'
        result = self.scrapper_cmd.extract_pdf_url(expediente, codigo)
        expected = 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc0' \
                   '2_2011_2.nsf/d99575da99ebfbe305256f2e006d1cf0/2a89be59a1' \
                   'a3966b05257c01000a5cd5/$FILE/PL02764101013.pdf'
        self.assertEqual(expected, result)

    def test_extract_pdf_url2(self):
        expediente = 'http://aniversarioperu.me/utero/test_pdl/expediente_' \
                     '02764_no_pdf_url.html'
        codigo = '02764'
        result = self.scrapper_cmd.extract_pdf_url(expediente, codigo)
        expected = ''
        self.assertEqual(expected, result)

    def test_parse_names(self):
        congresistas = "Dammert Ego Aguirre  Manuel Enrique Ernesto,Lescano" \
                       " Ancieta  Yonhy,Merino De Lama  Manuel,Guevara " \
                       "Amasifuen  Mesias Antonio,Mavila Leon  Rosa Delsa," \
                       "Mendoza Frisch  Veronika Fanny"
        expected = "Dammert Ego Aguirre, Manuel Enrique Ernesto; Lescano " \
                   "Ancieta, Yonhy; Merino De Lama, Manuel; Guevara " \
                   "Amasifuen, Mesias Antonio; Mavila Leon, Rosa Delsa; " \
                   "Mendoza Frisch, Veronika Fanny"
        result = self.scrapper_cmd.parse_names(congresistas)
        self.assertEqual(expected, result)

    def test_create_shorturl(self):
        codigo = "03774"
        expected = "4aw8ym"
        result = self.scrapper_cmd.create_shorturl(codigo)
        self.assertEqual(expected, result)

    def test_fix_date(self):
        date_string = "08/28/2014"
        expected = date(2014, 8, 28)
        result = self.scrapper_cmd.fix_date(date_string)
        self.assertEqual(expected, result)

    def test_gather_all_metadata(self):
        obj = {
            'numero_proyecto': '02764/2013-CR',
            'titulo': 'Propone Ley Universitaria',
            'seguimiento_page': 'http://aniversarioperu.me/utero/test_pdl/'
                                'seguimiento_02764.html',
            'test': 'test',
        }
        expected = {
            'numero_proyecto': '02764/2013-CR',
            'titulo': 'Propone Ley Universitaria',
            'seguimiento_page': 'http://aniversarioperu.me/utero/test_pdl/'
                                'seguimiento_02764.html',
            'codigo': '02764',
            'fecha_presentacion': date(2013, 10, 10),
            'expediente': 'http://www2.congreso.gob.pe/sicr/tradocestproc/'
                          'Expvirt_2011.nsf/visbusqptramdoc/02764?opendocu'
                          'ment',
            'pdf_url': 'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Cont'
                       'doc02_2011_2.nsf/d99575da99ebfbe305256f2e006d1cf0/2'
                       'a89be59a1a3966b05257c01000a5cd5/$FILE/PL02764101013'
                       '.pdf',
            'congresistas': 'Elias Avalos, Jose Luis; Chávez Cossío, Martha;'
                            ' Salgado Rubianes, Luz; Tait Villacorta, Cecilia;'
                            ' Chacón de Vettori, Cecilia Isabel; Aguinaga '
                            'Recuenco, Alejandro Aurelio; Cuculiza Torre, '
                            'Luisa María; García Belaunde, Víctor Andrés; '
                            'Bedoya de Vivanco, Javier Alonso; Galarreta '
                            'Velarde, Luis Fernando; Abugattás Majluf, Daniel '
                            'Fernando; Fujimori Higuchi, Kenji Gerardo; Acuña '
                            'Nuñez, Richard Frank; Acuña Peralta, Virgilio; '
                            'Bardalez Cochagne, Aldo Maximiliano; Cabrera '
                            'Ganoza, Eduardo Felipe; Ccama Layme, Francisco; '
                            'Chihuan Ramos, Leyla Felicita; Cordero Jon Tay, '
                            'Maria Del Pilar; Diaz Dios, Juan Jose; Gagó '
                            'Perez, Julio César; Hurtado Zamudio, Jesus '
                            'Panfilo; Lopez Cordova, Maria Magdalena; Medina '
                            'Ortiz, Antonio; Melgar Valdez, Elard Galo; Neyra '
                            'Olaychea, Angel; Pariona Galindo, Federico; '
                            'Ramirez Gamarra, Reber Joaquin; Rondon Fudinaga, '
                            'Gustavo Bernardo; Rosas Huaranga, Julio Pablo; '
                            'Salazar Miranda, Octavio Edilberto; Sarmiento '
                            'Betancourt, Freddy Fernando; Schaefer Cuculiza, '
                            'Karla Melissa; Spadaro Philipps, Pedro Carmelo; '
                            'Tan De Inafuko, Aurelia; Tapia Bernal, Segundo '
                            'Leocadio; Tubino Arias Schreiber, Carlos Mario '
                            'Del Carmen; Vacchelli Corbetto, Gian Carlo; '
                            'Valqui Matos, Nestor Antonio; Iberico Nuñez, '
                            'Luis',
            'short_url': '4zhube',
        }
        result = self.scrapper_cmd.gather_all_metadata(obj)
        self.assertEqual(expected, result)

        # Test when item already in db.
        b = Proyecto(**expected)
        b.save()
        result = self.scrapper_cmd.gather_all_metadata(obj)
        self.assertEqual("already in database", result)

    def test_save_project1(self):
        """Item is not in the database"""
        obj = dict(numero_proyecto="03774/2014-CR", short_url="4aw8ym",
                   fecha_presentacion=date.today(),
                   )
        self.scrapper_cmd.save_project(obj)
        item = Proyecto.objects.get(short_url="4aw8ym")
        result = item.fecha_presentacion
        expected = date.today()
        self.assertEqual(expected, result)

    def test_save_project2(self):
        """Item is already in the database"""
        obj = dict(numero_proyecto="03774/2014-CR", short_url="4aw8ym",
                   fecha_presentacion=date.today(),
                   )
        self.scrapper_cmd.save_project(obj)

        obj['short_url'] = "another url"
        result = self.scrapper_cmd.save_project(obj)

        expected = "already in database"
        self.assertEqual(expected, result)
