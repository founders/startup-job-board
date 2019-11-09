# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import CustomUser, Startup, Listing

admin.site.register(CustomUser)
admin.site.register(Startup)
admin.site.register(Listing)

"""

Generated token 0182c0ee92d7be9612001a1d1b3dbc4cd37c3c9b for user foundersadmin


"""