# -*- coding: utf-8 -*-
#
# django-codenerix-geodata
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from codenerix.models import CodenerixModel, GenInterface
from codenerix_extensions.helpers import get_language_database


class GenGeoName(CodenerixModel):  # META: Abstract class

    class Meta(CodenerixModel.Meta):
        abstract = True

    name = models.CharField(_('Name'), max_length=100, blank=False)

    def __str__(self):
        return u'{}'.format(smart_text(self.name))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        return [
            ('name', _('Name'), 100),
        ]


class Continent(CodenerixModel):
    code = models.CharField(_('Code'), max_length=2, unique=True, blank=False)

    def __str__(self):
        lang = get_language_database()
        lang_obj = getattr(self, '{}'.format(lang), None)
        if lang_obj and lang_obj.name:
            txt = lang_obj.name
        else:
            txt = self.code
        return u"{}".format(smart_text(txt))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        return [
            ('code', _('Code'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'code': models.Q(code__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['code'] = (_('Code'), lambda x: Q(code__icontains=x), 'input')
        return filters


class Country(CodenerixModel):
    code = models.CharField(_('Code'), max_length=2, unique=True, blank=False)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, verbose_name=_('Continent'), related_name='countries', null=False)

    def __str__(self):
        lang = get_language_database()
        lang_obj = getattr(self, '{}'.format(lang), None)
        if lang_obj and lang_obj.name:
            txt = lang_obj.name
        else:
            txt = self.code
        return u"{}".format(smart_text(txt))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        return [
            ('code', _('Code'), 100),
            ('continent', _('Continent'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'code': models.Q(code__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['code'] = (_('Code'), lambda x: Q(code__icontains=x), 'input')
        return filters


class TimeZone(CodenerixModel):
    name = models.CharField(_('Name'), max_length=50, unique=True, blank=False)

    def __str__(self):
        return u"{}".format(smart_text(self.name))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        return [
            ('name', _('Name'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'name': models.Q(name__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['name'] = (_('Name'), lambda x: Q(name__icontains=x), 'input')
        return filters


class Region(CodenerixModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Country'), null=False, related_name='regions')
    code = models.CharField(_('Code'), max_length=3, blank=False)

    def __str__(self):
        lang = get_language_database()
        lang_obj = getattr(self, '{}'.format(lang), None)
        if lang_obj and lang_obj.name:
            txt = lang_obj.name
        else:
            txt = self.code
        return u"{}".format(smart_text(txt))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        return [
            ('country', _('Country'), 100),
            ('code', _('Code'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'code': models.Q(code__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['code'] = (_('Code'), lambda x: Q(code__icontains=x), 'input')
        return filters


class Province(CodenerixModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_('Region'), null=False, related_name='provinces')
    code = models.CharField(_('Code'), max_length=3, blank=False)

    def __str__(self):
        lang = get_language_database()
        lang_obj = getattr(self, '{}'.format(lang), None)
        if lang_obj and lang_obj.name:
            txt = lang_obj.name
        else:
            txt = self.code
        return u"{}".format(smart_text(txt))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        return [
            ('region', _('Region'), 100),
            ('code', _('Code'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'code': models.Q(code__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['code'] = (_('Code'), lambda x: Q(code__icontains=x), 'input')
        return filters


class City(CodenerixModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Country'), null=False, related_name='cities')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_('Region'), null=True, related_name='cities')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_('Province'), null=True, related_name='cities')
    time_zone = models.ForeignKey(TimeZone, on_delete=models.CASCADE, verbose_name=_('Timezone'), null=False, related_name='cities')

    def __str__(self):
        lang = get_language_database()
        lang_obj = getattr(self, '{}'.format(lang), None)
        if lang_obj and lang_obj.name:
            txt = lang_obj.name
        else:
            txt = self.code
        return u"{}".format(smart_text(txt))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        return [
            ('country', _('Country'), 100),
            ('time_zone', _('Time zone'), 100),
        ]


class GeoAddress(GenInterface):  # META: Abstract class
    class Meta(GenInterface.Meta):
        abstract = True

    country = models.ForeignKey(Country, related_name='%(app_label)s_%(class)s_geo_addresses', verbose_name=_("Country"), blank=True, null=True, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, related_name='%(app_label)s_%(class)s_geo_addresses', verbose_name=_("Region"), blank=True, null=True, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, related_name='%(app_label)s_%(class)s_geo_addresses', verbose_name=_("Province"), blank=True, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='%(app_label)s_%(class)s_geo_addresses', verbose_name=_("City"), null=True, on_delete=models.CASCADE)
    town = models.CharField(_("Town"), max_length=250, blank=True, null=True)
    zipcode = models.CharField(_("Zip code"), max_length=6, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=250, blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=16, blank=True, null=True)

    def __str__(self):
        lang = get_language_database()
        lang_obj = getattr(self, '{}'.format(lang), None)
        if lang_obj and lang_obj.name:
            txt = lang_obj.name
        else:
            txt = self.code
        return u"{}".format(smart_text(txt))

    def __fields__(self, info):
        return [
            ('country', _("Country")),
            ('region', _("Region")),
            ('province', _("Province")),
            ('town', _("Town")),
            ('city', _('City')),
            ('zipcode', _('Zipcode')),
            ('address', _('Address')),
            ('phone', _('Phone')),
        ]

    def get_address(self):
        return self.address or ''

    def get_zipcode(self):
        return self.zipcode or ''

    def get_city(self):
        return self.city or ''

    def get_province(self):
        return self.province or ''

    def get_country(self):
        return self.country or ''


MODELS = (
    ('continent', 'Continent'),
    ('country', 'Country'),
    ('region', 'Region'),
    ('province', 'Province'),
    ('city', 'City'),
)

for field, model in MODELS:
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}GeoName{}(GenGeoName):\n".format(model, lang_code)
        query += "    {} = models.OneToOneField({}, on_delete=models.CASCADE, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
        exec(query)
