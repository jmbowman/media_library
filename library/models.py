from django.contrib.auth.models import User
from django.db import models

class MediaType(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Media(models.Model):
    title = models.CharField(max_length=200)
    type = models.ForeignKey(MediaType)
    owners = models.ManyToManyField(User)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False, auto_now=True)
    
    def sorted_owners(self):
        return self.owners.order_by('first_name')
    
    @models.permalink
    def get_absolute_url(self):
        return ('media-edit', (), {'pk': self.id})
    
    def __unicode__(self):
        return self.title
