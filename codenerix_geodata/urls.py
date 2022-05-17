# -*- coding: utf-8 -*-
#
# django-codenerix-geodata
#
# Codenerix GNU
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

from django.urls import re_path

from .views import ContinentList, ContinentCreate, ContinentCreateModal, ContinentUpdate, ContinentUpdateModal, ContinentDelete
from .views import CountryList, CountryCreate, CountryCreateModal, CountryUpdate, CountryUpdateModal, CountryDelete, CountryForeign
from .views import RegionList, RegionCreate, RegionCreateModal, RegionUpdate, RegionUpdateModal, RegionDelete, RegionForeign
from .views import ProvinceList, ProvinceCreate, ProvinceCreateModal, ProvinceUpdate, ProvinceUpdateModal, ProvinceDelete, ProvinceForeign
from .views import TimeZoneList, TimeZoneCreate, TimeZoneCreateModal, TimeZoneUpdate, TimeZoneUpdateModal, TimeZoneDelete
from .views import CityList, CityCreate, CityCreateModal, CityUpdate, CityUpdateModal, CityDelete, CityForeign


urlpatterns = [
    re_path(r'^continents$', ContinentList.as_view(), name='CDNX_geodata_continents_list'),
    re_path(r'^continents/add$', ContinentCreate.as_view(), name='CDNX_geodata_continents_add'),
    re_path(r'^continents/addmodal$', ContinentCreateModal.as_view(), name='CDNX_geodata_continents_addmodal'),
    re_path(r'^continents/(?P<pk>\w+)/edit$', ContinentUpdate.as_view(), name='CDNX_geodata_continents_edit'),
    re_path(r'^continents/(?P<pk>\w+)/editmodal$', ContinentUpdateModal.as_view(), name='CDNX_geodata_continents_editmodal'),
    re_path(r'^continents/(?P<pk>\w+)/delete$', ContinentDelete.as_view(), name='CDNX_geodata_continents_delete'),

    re_path(r'^countrys$', CountryList.as_view(), name='CDNX_geodata_countries_list'),
    re_path(r'^countrys/add$', CountryCreate.as_view(), name='CDNX_geodata_countries_add'),
    re_path(r'^countrys/addmodal$', CountryCreateModal.as_view(), name='CDNX_geodata_countries_addmodal'),
    re_path(r'^countrys/(?P<pk>\w+)/edit$', CountryUpdate.as_view(), name='CDNX_geodata_countries_edit'),
    re_path(r'^countrys/(?P<pk>\w+)/editmodal$', CountryUpdateModal.as_view(), name='CDNX_geodata_countries_editmodal'),
    re_path(r'^countrys/(?P<pk>\w+)/delete$', CountryDelete.as_view(), name='CDNX_geodata_countries_delete'),
    re_path(r'^countrys/foreign/(?P<search>[\w\W]+|\*)$', CountryForeign.as_view(), name='CDNX_ext_location_country_foreign'),

    re_path(r'^countries$', CountryList.as_view(), name='CDNX_geodata_countries_list'),
    re_path(r'^countries/add$', CountryCreate.as_view(), name='CDNX_geodata_countries_add'),
    re_path(r'^countries/addmodal$', CountryCreateModal.as_view(), name='CDNX_geodata_countries_addmodal'),
    re_path(r'^countries/(?P<pk>\w+)/edit$', CountryUpdate.as_view(), name='CDNX_geodata_countries_edit'),
    re_path(r'^countries/(?P<pk>\w+)/editmodal$', CountryUpdateModal.as_view(), name='CDNX_geodata_countries_editmodal'),
    re_path(r'^countries/(?P<pk>\w+)/delete$', CountryDelete.as_view(), name='CDNX_geodata_countries_delete'),
    re_path(r'^countries/foreign/(?P<search>[\w\W]+|\*)$', CountryForeign.as_view(), name='CDNX_ext_location_country_foreign'),

    re_path(r'^regions$', RegionList.as_view(), name='CDNX_geodata_regions_list'),
    re_path(r'^regions/add$', RegionCreate.as_view(), name='CDNX_geodata_regions_add'),
    re_path(r'^regions/addmodal$', RegionCreateModal.as_view(), name='CDNX_geodata_regions_addmodal'),
    re_path(r'^regions/(?P<pk>\w+)/edit$', RegionUpdate.as_view(), name='CDNX_geodata_regions_edit'),
    re_path(r'^regions/(?P<pk>\w+)/editmodal$', RegionUpdateModal.as_view(), name='CDNX_geodata_regions_editmodal'),
    re_path(r'^regions/(?P<pk>\w+)/delete$', RegionDelete.as_view(), name='CDNX_geodata_regions_delete'),
    re_path(r'^regions/foreign/(?P<search>[\w\W]+|\*)$', RegionForeign.as_view(), name='CDNX_ext_location_regions_foreign'),

    re_path(r'^provinces$', ProvinceList.as_view(), name='CDNX_geodata_provinces_list'),
    re_path(r'^provinces/add$', ProvinceCreate.as_view(), name='CDNX_geodata_provinces_add'),
    re_path(r'^provinces/addmodal$', ProvinceCreateModal.as_view(), name='CDNX_geodata_provinces_addmodal'),
    re_path(r'^provinces/(?P<pk>\w+)/edit$', ProvinceUpdate.as_view(), name='CDNX_geodata_provinces_edit'),
    re_path(r'^provinces/(?P<pk>\w+)/editmodal$', ProvinceUpdateModal.as_view(), name='CDNX_geodata_provinces_editmodal'),
    re_path(r'^provinces/(?P<pk>\w+)/delete$', ProvinceDelete.as_view(), name='CDNX_geodata_provinces_delete'),
    re_path(r'^provinces/foreign/(?P<search>[\w\W]+|\*)$', ProvinceForeign.as_view(), name='CDNX_ext_location_provinces_foreign'),

    re_path(r'^timezones$', TimeZoneList.as_view(), name='CDNX_geodata_timezones_list'),
    re_path(r'^timezones/add$', TimeZoneCreate.as_view(), name='CDNX_geodata_timezones_add'),
    re_path(r'^timezones/addmodal$', TimeZoneCreateModal.as_view(), name='CDNX_geodata_timezones_addmodal'),
    re_path(r'^timezones/(?P<pk>\w+)/edit$', TimeZoneUpdate.as_view(), name='CDNX_geodata_timezones_edit'),
    re_path(r'^timezones/(?P<pk>\w+)/editmodal$', TimeZoneUpdateModal.as_view(), name='CDNX_geodata_timezones_editmodal'),
    re_path(r'^timezones/(?P<pk>\w+)/delete$', TimeZoneDelete.as_view(), name='CDNX_geodata_timezones_delete'),

    re_path(r'^citys$', CityList.as_view(), name='CDNX_geodata_cities_list'),
    re_path(r'^citys/add$', CityCreate.as_view(), name='CDNX_geodata_cities_add'),
    re_path(r'^citys/addmodal$', CityCreateModal.as_view(), name='CDNX_geodata_cities_addmodal'),
    re_path(r'^citys/(?P<pk>\w+)/edit$', CityUpdate.as_view(), name='CDNX_geodata_cities_edit'),
    re_path(r'^citys/(?P<pk>\w+)/editmodal$', CityUpdateModal.as_view(), name='CDNX_geodata_cities_editmodal'),
    re_path(r'^citys/(?P<pk>\w+)/delete$', CityDelete.as_view(), name='CDNX_geodata_cities_delete'),
    re_path(r'^citys/foreign/(?P<search>[\w\W]+|\*)$', CityForeign.as_view(), name='CDNX_ext_location_citys_foreign'),

    re_path(r'^cities$', CityList.as_view(), name='CDNX_geodata_cities_list'),
    re_path(r'^cities/add$', CityCreate.as_view(), name='CDNX_geodata_cities_add'),
    re_path(r'^cities/addmodal$', CityCreateModal.as_view(), name='CDNX_geodata_cities_addmodal'),
    re_path(r'^cities/(?P<pk>\w+)/edit$', CityUpdate.as_view(), name='CDNX_geodata_cities_edit'),
    re_path(r'^cities/(?P<pk>\w+)/editmodal$', CityUpdateModal.as_view(), name='CDNX_geodata_cities_editmodal'),
    re_path(r'^cities/(?P<pk>\w+)/delete$', CityDelete.as_view(), name='CDNX_geodata_cities_delete'),
    re_path(r'^cities/foreign/(?P<search>[\w\W]+|\*)$', CityForeign.as_view(), name='CDNX_ext_location_citys_foreign'),
]
