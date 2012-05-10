"""
Database models for the library application.

.. module:: library.models
   :synopsis: Database models for the library application

.. moduleauthor:: Jeremy Bowman <jmbowman@alum.mit.edu>

"""

from django.contrib.auth.models import User
from django.db import models


class MediaType(models.Model):

    """A particular type of media (Blu-ray, CD, DVD, etc.)."""

    name = models.CharField(max_length=30)

    def __unicode__(self):
        """Use the name of the media type as its Unicode representation."""
        return self.name


class Media(models.Model):

    """An item of media owned by one or more users of the application."""

    title = models.CharField(max_length=200)
    type = models.ForeignKey(MediaType)
    owners = models.ManyToManyField(User)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False, auto_now=True)

    def sorted_owners(self):
        """List the item's owners in alphabetical order by first name."""
        return self.owners.order_by('first_name')

    @models.permalink
    def get_absolute_url(self):
        """Get the item's edit URL."""
        return ('media-edit', (), {'pk': self.id})

    def __unicode__(self):
        """Use the media item's title as its Unicode representation."""
        return self.title
