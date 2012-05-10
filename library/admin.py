"""
Admin app configuration for the library application.

.. module:: library.admin
   :synopsis: Admin app configuration for the library application

.. moduleauthor:: Jeremy Bowman <jmbowman@alum.mit.edu>

"""

from django.contrib import admin

from library.models import Media, MediaType

admin.site.register(Media)
admin.site.register(MediaType)
