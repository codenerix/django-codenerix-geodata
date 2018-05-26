========================
django-codenerix-geodata
========================

Codenerix Geodata is a module that enables `CODENERIX <http://www.codenerix.com/>`_ to work with Geographical data. It includes models for geolocation (Continents, Countries, Regions, cities, time zones, etc) and data gotten from https://www.maxmind.com/

.. image:: http://www.codenerix.com/wp-content/uploads/2018/05/codenerix.png
    :target: http://www.codenerix.com
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

Coming soon... do you help us? `Codenerix <http://www.codenerix.com/>`_

You can chat with us `here <https://goo.gl/NgpzBh>`_.


*******
Credits
*******

This project has been possible thanks to `Centrologic <http://www.centrologic.com/>`_.

The geographical data are offered by `Maxmind <https://www.maxmind.com/>`_, which is made available under Creative Commons Attribution 3.0
