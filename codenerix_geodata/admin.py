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

from django.conf import settings
from django.contrib import admin

from .models import Continent, Country, Region, Province, TimeZone, City, MODELS

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Province)
admin.site.register(TimeZone)
admin.site.register(City)

for field, model in MODELS:
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_geodata.models import {}GeoName{}\n".format(model, lang_code)
        query += "admin.site.register({}GeoName{})\n".format(model, lang_code)
        exec(query)
