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

""" Populate geographic data using the free database provided by MaxMind.

Two different databases were used:
    - GeoLite2 City: http://geolite.maxmind.com/download/geoip/database/GeoLite2-City-CSV.zip
    - GeoLite2 Country: http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country-CSV.zip
"""

import sys
import time
from os.path import dirname, join
from csv import reader

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist

from codenerix_lib.debugger import Debugger
from codenerix_extensions.helpers import FileBZ2
from codenerix_geodata.models import (
    Continent,
    Country,
    Region,
    Province,
    City,
    TimeZone,
)


BASE_LANGUAGE = "EN"

COUNTRY_DATA_FILES = {
    "ES": "GeoLite2-Country-Locations-es.csv.bz2",
    "EN": "GeoLite2-Country-Locations-en.csv.bz2",
}

CITY_DATA_FILES = {
    "ES": "GeoLite2-City-Locations-es.csv.bz2",
    "EN": "GeoLite2-City-Locations-en.csv.bz2",
}

LANGUAGES = set(
    [
        code
        for code in settings.LANGUAGES_DATABASES
        if code in COUNTRY_DATA_FILES
    ]
)


def clean(name):
    if name:
        try:
            name = name.decode("utf-8")
        except Exception:
            pass
        if name[0] == '"' and name[-1] == '"':
            return name[1:-1]
    return name


def populate_missing_names(data):
    for lang in LANGUAGES:
        for d in data.values():
            if lang not in d or d[lang] == "":
                for other_lang in LANGUAGES - {lang}:
                    if d[other_lang] != "":
                        d[lang] = d[other_lang]
                        break


def continents_lines(filename):
    with FileBZ2(filename, "rb") as data_file:
        csv_file = reader(data_file, delimiter=",", quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            _, _, continent_code, continent_name, _, _ = line
            if continent_code.strip() != "" and continent_name.strip() != "":
                yield continent_code, clean(continent_name)


def country_lines(filename):
    with FileBZ2(filename, "rb") as data_file:
        csv_file = reader(data_file, delimiter=",", quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            geoid, _, continent_code, _, country_code, country_name = line
            if (
                continent_code.strip() != ""
                and country_code.strip() != ""
                and country_name.strip() != ""
            ):
                yield int(geoid), continent_code, country_code, clean(
                    country_name
                )


def region_lines(filename):
    with FileBZ2(filename, "rb") as data_file:
        csv_file = reader(data_file, delimiter=",", quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            (
                geoid,
                _,
                _,
                _,
                country_code,
                _,
                region_code,
                region_name,
                province_code,
                province_name,
                city_name,
                _,
                _,
            ) = line
            if (
                country_code != ""
                and region_code != ""
                and region_name.strip() != ""
            ):
                yield int(geoid), country_code, region_code, clean(region_name)


def province_lines(filename):
    with FileBZ2(filename, "rb") as data_file:
        csv_file = reader(data_file, delimiter=",", quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            (
                geoid,
                _,
                _,
                _,
                country_code,
                _,
                region_code,
                _,
                province_code,
                province_name,
                _,
                _,
                _,
            ) = line
            if (
                country_code != ""
                and region_code != ""
                and province_code != ""
                and province_name != ""
            ):
                yield int(
                    geoid
                ), country_code, region_code, province_code, clean(
                    province_name
                )


def city_lines(filename):
    with FileBZ2(filename, "rb") as data_file:
        csv_file = reader(data_file, delimiter=",", quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            (
                geoid,
                _,
                _,
                _,
                country_code,
                _,
                region_code,
                _,
                province_code,
                _,
                city_name,
                _,
                time_zone,
            ) = line
            if geoid != "" and city_name.strip() != "" and time_zone != "":
                yield int(
                    geoid
                ), country_code, region_code, province_code, clean(
                    city_name
                ), clean(
                    time_zone
                )


class Command(BaseCommand, Debugger):
    help = _("Populates Continent, Country and City models")
    __percent = None

    def percent_init(self, text, total):
        self.__percent = {}
        self.__percent["text"] = text
        self.__percent["last"] = time.time() - 6
        self.__percent["counter"] = 0
        self.__percent["total"] = total
        self.percent()

    def percent(self):
        last = (self.__percent["counter"] + 1) == self.__percent["total"]
        now = time.time()
        if (self.__percent["last"] + 6 < now) or last:
            self.__percent["last"] = now
            if self.__percent["counter"]:
                delstr = ""
                for i in range(0, 200):
                    delstr += "\b"
                sys.stdout.write(delstr)
            if not last:
                text = "{}/{}".format(
                    self.__percent["counter"], self.__percent["total"]
                )
                percent = (
                    100 * self.__percent["counter"] / self.__percent["total"]
                )
                self.debug(
                    "{}: ".format(self.__percent["text"]),
                    color="blue",
                    tail=False,
                )
                self.debug(
                    "{}".format(text), color="cyan", head=False, tail=False
                )
                self.debug(
                    " - {:.1f}%      ".format(percent),
                    color="white",
                    head=False,
                    tail=False,
                )
            else:
                self.debug(self.__percent["text"], color="blue", tail=False)
                self.debug(
                    " ... Done                     ", head=False, color="green"
                )
            sys.stdout.flush()
        self.__percent["counter"] += 1

    def handle(self, *args, **options):

        # Autoconfigure Debugger
        self.set_name("CODENERIX-GEODATA")
        self.set_debug()

        # print('Erasing existing data ...')
        # City.objects.all().delete()
        # TimeZone.objects.all().delete()
        # Province.objects.all().delete()
        # Region.objects.all().delete()
        # Country.objects.all().delete()
        # Continent.objects.all().delete()

        print("Importing new data ... This action may take some minutes.")
        print("")
        data_path = join(dirname(dirname(dirname(__file__))), "data")

        # Importing language generated models
        for lang in LANGUAGES:
            exec(
                "from codenerix_geodata.models import ContinentGeoName{}".format(
                    lang
                )
            )
            exec(
                "from codenerix_geodata.models import CountryGeoName{}".format(
                    lang
                )
            )
            exec(
                "from codenerix_geodata.models import RegionGeoName{}".format(
                    lang
                )
            )
            exec(
                "from codenerix_geodata.models import ProvinceGeoName{}".format(
                    lang
                )
            )
            exec(
                "from codenerix_geodata.models import CityGeoName{}".format(
                    lang
                )
            )

        self.debug("Importing ...", color="yellow", tail=False)
        self.debug(" Continents", color="purple", head=False, tail=False)
        self.debug(
            " Countries Regions Provinces Cities", color="grey", head=False
        )
        continents = {}
        for lang in LANGUAGES:
            filename = join(data_path, COUNTRY_DATA_FILES[lang])
            lines = list(continents_lines(filename))
            self.percent_init("    > Prepare data {}".format(lang), len(lines))
            for code, name in lines:
                if code not in continents:
                    continents[code] = {"model": Continent(code=code)}
                continents[code][lang] = name
                self.percent()

        items = continents.items()
        self.percent_init("    > Link", len(items))
        for code, continent in items:
            try:
                model = Continent.objects.get(code=code)
                continent["model"] = model
            except ObjectDoesNotExist:
                continent["model"].save()
            self.percent()

        for lang in LANGUAGES:
            model_type = eval("ContinentGeoName{}".format(lang))
            items = continents.values()
            self.percent_init("    > Fill {}".format(lang), len(items))
            for continent in items:
                try:
                    model = model_type.objects.get(
                        continent=continent["model"]
                    )
                except ObjectDoesNotExist:
                    model = model_type()
                    model.continent = continent["model"]
                model.name = continent[lang]
                model.save()
                self.percent()

        self.debug("Importing ...", color="yellow", tail=False)
        self.debug(" Continents", color="simplepurple", head=False, tail=False)
        self.debug(" Countries", color="purple", head=False, tail=False)
        self.debug(" Regions Provinces Cities", color="grey", head=False)
        countries = {}
        for lang in LANGUAGES:
            filename = join(data_path, COUNTRY_DATA_FILES[lang])
            items = list(country_lines(filename))
            self.percent_init("    > Prepare data {}".format(lang), len(items))
            for geoid, continent, code, name in items:
                if code not in countries:
                    countries[code] = {
                        "model": Country(
                            pk=geoid,
                            code=code,
                            continent=continents[continent]["model"],
                        )
                    }
                countries[code][lang] = name
                self.percent()

        values = countries.values()
        self.percent_init("    > Link", len(values))
        for country in values:
            try:
                model = Country.objects.get(code=country["model"].code)
                country["model"] = model
            except ObjectDoesNotExist:
                country["model"].save()
            self.percent()

        for lang in LANGUAGES:
            model_type = eval("CountryGeoName{}".format(lang))
            self.percent_init("    > Fill {}".format(lang), len(values))
            for country in values:
                try:
                    model = model_type.objects.get(country=country["model"])
                except ObjectDoesNotExist:
                    model = model_type()
                    model.country = country["model"]
                model.name = country[lang]
                model.save()
                self.percent()

        self.debug("Importing ...", color="yellow", tail=False)
        self.debug(
            " Continents Countries",
            color="simplepurple",
            head=False,
            tail=False,
        )
        self.debug(" Regions", color="purple", head=False, tail=False)
        self.debug(" Provinces Cities", color="grey", head=False)
        regions = {}
        for lang in LANGUAGES:
            filename = join(data_path, CITY_DATA_FILES[lang])
            lines = list(region_lines(filename))
            self.percent_init("    > Prepare data {}".format(lang), len(lines))
            for geoid, country_code, region_code, region_name in lines:
                region_key = "{}_{}".format(country_code, region_code)
                if region_key not in regions:
                    regions[region_key] = {
                        "model": Region(
                            pk=geoid,
                            code=region_code,
                            country=countries[country_code]["model"],
                        )
                    }
                regions[region_key][lang] = region_name
                self.percent()

        items = regions.values()
        self.percent_init("    > Link", len(items))
        for region in items:
            try:
                model = Region.objects.get(pk=region["model"].pk)
                region["model"] = model
            except ObjectDoesNotExist:
                region["model"].save()
            self.percent()

        self.debug("    > Populate missing", color="blue", tail=False)
        populate_missing_names(regions)
        self.debug(" ... Done", color="green", head=False)

        for lang in LANGUAGES:
            model_type = eval("RegionGeoName{}".format(lang))
            items = regions.values()
            self.percent_init("    > Fill {}".format(lang), len(items))
            for region in items:
                try:
                    model = model_type.objects.get(region=region["model"])
                except ObjectDoesNotExist:
                    model = model_type()
                    model.region = region["model"]
                    model.name = region[lang]
                model.save()
                self.percent()

        self.debug("Importing ...", color="yellow", tail=False)
        self.debug(
            " Continents Countries Regions",
            color="simplepurple",
            head=False,
            tail=False,
        )
        self.debug(" Provinces", color="purple", head=False, tail=False)
        self.debug(" Cities", color="grey", head=False)
        provinces = {}
        for lang in LANGUAGES:
            filename = join(data_path, CITY_DATA_FILES[lang])
            lines = list(province_lines(filename))
            self.percent_init("    > Prepare data {}".format(lang), len(lines))
            for (
                geoid,
                country_code,
                region_code,
                province_code,
                province_name,
            ) in lines:
                region_key = "{}_{}".format(country_code, region_code)
                province_key = "{}_{}_{}".format(
                    country_code, region_code, province_code
                )
                if province_key not in provinces:
                    provinces[province_key] = {
                        "model": Province(
                            pk=geoid,
                            code=province_code,
                            region=regions[region_key]["model"],
                        )
                    }
                provinces[province_key][lang] = province_name
                self.percent()

        items = provinces.values()
        self.percent_init("    > Link", len(items))
        for province in items:
            try:
                model = Province.objects.get(pk=province["model"].pk)
                province["model"] = model
            except ObjectDoesNotExist:
                province["model"].save()
            self.percent()

        self.debug("    > Populate missing", color="blue", tail=False)
        populate_missing_names(provinces)
        self.debug(" ... Done", color="green", head=False)

        for lang in LANGUAGES:
            model_type = eval("ProvinceGeoName{}".format(lang))
            items = provinces.values()
            self.percent_init("    > Fill {}".format(lang), len(items))
            for province in items:
                try:
                    model = model_type.objects.get(province=province["model"])
                except ObjectDoesNotExist:
                    model = model_type()
                    model.province = province["model"]
                model.name = province[lang]
                model.save()
                self.percent()

        self.debug("Importing ...", color="yellow", tail=False)
        self.debug(
            " Continents Countries Regions Provinces",
            color="simplepurple",
            head=False,
            tail=False,
        )
        self.debug(" Cities", color="purple", head=False, tail=False)
        cities = {}
        timezones = {}
        for lang in LANGUAGES:
            filename = join(data_path, CITY_DATA_FILES[lang])
            lines = list(city_lines(filename))
            self.percent_init("    > Prepare data {}".format(lang), len(lines))
            for (
                city_id,
                country_code,
                region_code,
                province_code,
                city_name,
                time_zone,
            ) in lines:
                if time_zone not in timezones:
                    try:
                        model = TimeZone.objects.get(name=time_zone)
                        timezones[time_zone] = model
                    except ObjectDoesNotExist:
                        timezones[time_zone] = TimeZone(name=time_zone)
                        timezones[time_zone].save()

                if city_id not in cities:
                    city = City(
                        pk=city_id,
                        country=countries[country_code]["model"],
                        time_zone=timezones[time_zone],
                    )
                    if region_code != "":
                        region_key = "{}_{}".format(country_code, region_code)
                        city.region = regions[region_key]["model"]

                    if province_code != "":
                        province_key = "{}_{}_{}".format(
                            country_code, region_code, province_code
                        )
                        city.province = provinces[province_key]["model"]

                    cities[city_id] = {"model": city}

                cities[city_id][lang] = city_name
                self.percent()

        items = cities.values()
        self.percent_init("    > Link", len(items))
        for city in items:
            try:
                model = City.objects.get(pk=city["model"].pk)
                city["model"] = model
            except ObjectDoesNotExist:
                city["model"].save()
            self.percent()

        self.debug("    > Populate missing", color="blue", tail=False)
        populate_missing_names(cities)
        self.debug(" ... Done", color="green", head=False)

        for lang in LANGUAGES:
            model_type = eval("CityGeoName{}".format(lang))
            items = cities.values()
            self.percent_init("    > Fill {}".format(lang), len(items))
            for city in items:
                try:
                    model = model_type.objects.get(city=city["model"])
                except ObjectDoesNotExist:
                    model = model_type()
                    model.city = city["model"]
                model.name = city[lang]
                model.save()
                self.percent()

        self.debug(
            "Removing regions without cities ...", color="yellow", tail=False
        )
        for region in Region.objects.all():
            if region.cities.count() == 0:
                region.delete()
        self.debug(" ... Done", color="green", head=False)

        self.debug(
            "Removing provinces without cities ...", color="yellow", tail=False
        )
        for province in Province.objects.all():
            if province.cities.count() == 0:
                province.delete()
        self.debug(" ... Done", color="green", head=False)

        self.debug("All done !!!", color="green")
