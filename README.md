[![Build Status](https://travis-ci.org/aniversarioperu/proyectos_de_ley.svg?branch=master)](https://travis-ci.org/aniversarioperu/proyectos_de_ley)
[![Coverage Status](https://coveralls.io/repos/aniversarioperu/proyectos_de_ley/badge.png)](https://coveralls.io/r/aniversarioperu/proyectos_de_ley)

# Dependencias
Estos scripts ha sido probados en una computadora usando Ubuntu 13.10 y
necesitan que las siguientes dependencias estén instaladas.

* Python3, django1.7
* pip: ``sudo apt-get install python-pip``
* > pip install -r requirements/dev.txt

# Modo de ejecución

## Custom django command

* El comando ``python manage.py scrape`` se encarga de cosechar la 
información del servidor del congreso y almacernarla en una base de datos 
local.
* Toda la información cosechada se almancena en una base de datos SQLite3. 
Django se encarga de servir las páginas y motor de búsqueda.

## script do_ocr.py
[We don't want OCR yet]

Esto se ha implentado al incio del proyecto pero es posible que no funcione
ya que no se ha actualizado recientemente.
* El script ``do_ocr.py`` se encarga de convertir los PDFs del folder ``pdf/``
  a HTML previo proceso OCR usando ``tesseract``.
* También crea un ATOM Feed ``feed.xml`` conteniendo los proyectos de ley que
  han sido convertidos de PDF a HTML.
* Si un PDF ya ha sido procesado por OCR y convertido a HTML, este script
  evitará volverlo a procesar en futuras corridas.
* Los archivos HTML y el ``feed.xml`` son creados con info contenida en la
  "base de datos" ``proyectos_data.json``.

## plantilla HTML

* El archivo ``base.html`` funciona como plantilla para crear las páginas HTML.
  Cualquier cambio al estilo se debe realizar en este archivo. Esta plantilla
  usa un estilo basado en Twitter Bootstrap con *responsive features* para que
  se vea bien en computadoras y dispositivos móbiles.
* Esos campos se usan para introducir en contenido en la plantilla y generar
  los archivos HTML.
