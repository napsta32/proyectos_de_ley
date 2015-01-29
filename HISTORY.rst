History
=======

v1.5.3 (2014-12-28)
~~~~~~~~~~~~~~~~~~~
Stats: fixing bug for "otros proyectos dispensados".

v1.5.2 (2014-12-24)
~~~~~~~~~~~~~~~~~~~
Adding respeto.pe logo, new proyectosdeley log and update "About" page.

v1.5.1 (2014-12-16)
~~~~~~~~~~~~~~~~~~~
Fixing create_stats custom command. The update_or_create
command was creating an extra set of items in the database instead of doing
an update. Fixed.

v1.5.0 (2014-12-11)
~~~~~~~~~~~~~~~~~~~
* Only accept as search keywords strings with len > 2.
* Sort simple search result by codigo desc.
* Fix bug on pagination links.
* Keywords were shown with brackets.
* Search box of simple search show user's query.
* Added links to PDF and Expediente in Seguimientos page.
* Added custom command in `stats` app: `create_stats` which should run once a day.
* Added charts to stats page: Number of projects in comisiones and Number of projects that
  did not go to 2nd round of votes. New table expedients to keep events and
  URLs from the `Expediente` page.

v1.4.1 (2014-11-11)
~~~~~~~~~~~~~~~~~~~
* Improved general search engine, also events in `seguimientos` are queried.
* Autofocus on search box when page loads.
* Better highlighting of keywords.
* Check errors in datefield widget (advanced search).
* Show error fields in datefield widget.
* Resize advanced search according to screen sizes.
* Add link to production site.

v1.4.0 (2014-11-08)
~~~~~~~~~~~~~~~~~~~
* Advanced search by *fecha presentación*.
* Stats.
* Improved RSS feed.
* Now we have our own `Seguimiento` page.
* Many more additional fields are scrapped (*seguimientos*, *iniciativas agrupadas*).
* Better scrapping of PDF urls.
* The scrapping functions have been moved to another project: `proyectos_de_ley_scraper`.
* Added version to footer of pages.

v1.2.0 (2014-09-24)
~~~~~~~~~~~~~~~~~~~
* Scrapping more metadata from seguimiento_page.
* Killed bug to get PDF url when the filename includes funny characters.
* Custom command to update `seguimiento` events for each project in our database.

v1.1.1 (2014-09-22)
~~~~~~~~~~~~~~~~~~~
* Favicon.
* Don't show navigation bar if there are no results.

v1.1.0 (2014-09-21)
~~~~~~~~~~~~~~~~~~~
Pagination for search results (40 items per page).

v1.0.1 (2014-09-20)
~~~~~~~~~~~~~~~~~~~
Own pagination for index and congresista pages.

v1.0.0 (2014-09-15)
~~~~~~~~~~~~~~~~~~~
Migrated to Django.
