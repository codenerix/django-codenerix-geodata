========================
django-codenerix-geodata
========================

GEODATA is a module that enables `CODENERIX.com <http://www.codenerix.com/>`_ to work with Geographical data. It includes models for geolocation (Continents, Countries, Regions, cities, time zones, etc) and data gotten from https://www.maxmind.com/

.. image:: http://www.centrologic.com/wp-content/uploads/2017/01/logo-codenerix.png
    :target: http://www.codenerix.com
    :alt: Try our demo with Centrologic Cloud

****
Demo
****

You can have a look to our `demo online <http://demo.codenerix.com>`_.

You can find some working examples in GITHUB at `django-codenerix-examples <https://github.com/centrologic/django-codenerix-examples>`_ project.

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

Coming soon... do you help us? `Centrologic <http://www.centrologic.com/>`_

******************
Commercial support
******************

This project is backed by `Centrologic <http://www.centrologic.com/>`_. You can discover more in `CODENERIX.com <http://www.codenerix.com/>`_.
If you need help implementing or hosting django-codenerix-geodata, please contact us:
http://www.centrologic.com/contacto/

.. image:: http://www.centrologic.com/wp-content/uploads/2015/09/logo-centrologic.png
    :target: http://www.centrologic.com
    :alt: Centrologic is supported mainly by Centrologic Computational Logistic Center

*******
Credits
*******

The geographical data are offered by `Maxmind <https://www.maxmind.com/>`_, which is made available under Creative Commons Attribution 3.0
