|Build Status| |Cover alls|


Proyectos de Ley del Congreso
=============================


Configuración
-------------

The steps below will get you up and running with a local development environment. We assume you have the following installed:

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


Ejecutar el scrapper
--------------------
* El comando ``python manage.py scrape`` se encarga de cosechar la 
información del servidor del congreso y almacernarla en una base de datos 
local.
* Toda la información cosechada se almancena en una base de datos SQLite3. 
Django se encarga de servir las páginas y motor de búsqueda.

Plantilla HTML
--------------
* El archivo ``base.html`` funciona como plantilla para crear las páginas HTML.
  Cualquier cambio al estilo se debe realizar en este archivo. Esta plantilla
  usa un estilo basado en Twitter Bootstrap con *responsive features* para que
  se vea bien en computadoras y dispositivos móbiles.
* Esos campos se usan para introducir en contenido en la plantilla y generar
  los archivos HTML.

.. |Build Status| image:: https://travis-ci.org/aniversarioperu/proyectos_de_ley.svg?branch=master
   :target: https://travis-ci.org/aniversarioperu/proyectos_de_ley
.. |Coverage alls| image:: https://coveralls.io/repos/aniversarioperu/proyectos_de_ley/badge.png
   :target: https://coveralls.io/r/aniversarioperu/proyectos_de_ley
