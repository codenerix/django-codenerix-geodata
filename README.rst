========================
django-codenerix-geodata
========================

Codenerix Geodata is a module that enables `CODENERIX <https://www.codenerix.com/>`_ to work with Geographical data. It includes models for geolocation (Continents, Countries, Regions, cities, time zones, etc) and data gotten from https://www.maxmind.com/

.. image:: https://github.com/codenerix/django-codenerix/raw/master/codenerix/static/codenerix/img/codenerix.png
    :target: https://www.codenerix.com
    :alt: Try our demo with Codenerix Cloud

****
Demo
****

You can have a look to our `demo online <http://demo.codenerix.com>`_.

**********
Quickstart
**********

1. Install this package::

    For python 2: sudo pip2 install django-codenerix-geodata
    For python 3: sudo pip3 install django-codenerix-geodata

2. Add "codenerix_geodata" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'codenerix_geodata',
    ]

3. Add the param in setting:
	# list of languages available for the translation of the content of the models
	LANGUAGES_DATABASES = ['ES', 'EN']

4. Since Codenerix Geodata is a library, you only need to import its parts into your project and use them.

*************
Documentation
*************

Coming soon... do you help us?

You can get in touch with us `here <https://codenerix.com/contact/>`_.


*******
Credits
*******

The geographical data are offered by `Maxmind <https://www.maxmind.com/>`_, which is made available under Creative Commons Attribution 3.0
