# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import User, Startup, Listing

admin.site.register(User)
admin.site.register(Startup)
admin.site.register(Listing)