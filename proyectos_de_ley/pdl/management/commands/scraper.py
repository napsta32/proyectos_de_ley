# -*- coding: utf-8 -*-
import codecs
import datetime
from datetime import date
from datetime import timedelta as td
import hashlib
import json
from optparse import make_option
import os
from random import randint
import re
from time import sleep

from optparse import make_option

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
