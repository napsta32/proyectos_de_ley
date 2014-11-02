|Build Status| |Cover alls|


Proyectos de Ley del Congreso
=============================


Configuración
-------------

Esta aplicación se basa en el siguiente *software*:

* pip
* virtualenv
* python v3
* django v1.7

Crear y un activar un virtualenv_ que use Python3. En un terminal, instalar 
las dependencias para desarrollo local::

    $ pip install -r requirements/dev.txt

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Para correr el software, reemplazar ``yourapp`` con el nombre
del folder que contiene el proyecto de Django::

    $ python yourapp/manage.py runserver --settings=yourapp.settings.local


Obteniendo información
----------------------
Toda la info se obtiene desde las páginas web del Congreso mediante el uso de
un *scraper* basado en el *framework* Scrapy. El *scraper* se encuentra en
este repositorio_.

.. _repositorio: https://github.com/proyectosdeley/proyectos_de_ley_scraper

Plantilla HTML
--------------
* El archivo ``base.html`` funciona como plantilla para crear las páginas HTML.
  Cualquier cambio al estilo se debe realizar en este archivo. Esta plantilla
  usa un estilo basado en Twitter Bootstrap con *responsive features* para que
  se vea bien en computadoras y dispositivos móbiles.
* Esos campos se usan para introducir en contenido en la plantilla y generar
  los archivos HTML.

.. |Build Status| image:: https://travis-ci.org/proyectosdeley/proyectos_de_ley.svg?branch=master
   :target: https://travis-ci.org/proyectosdeley/proyectos_de_ley
.. |Cover alls| image:: https://coveralls.io/repos/proyectosdeley/proyectos_de_ley/badge.png
   :target: https://coveralls.io/r/proyectosdeley/proyectos_de_ley
