"""
URL mapping for the library application.

.. module:: library.urls
   :synopsis: URL mapping for the library application

.. moduleauthor:: Jeremy Bowman <jmbowman@alum.mit.edu>

"""

from django.conf.urls.defaults import patterns
from django.contrib.auth.decorators import login_required

from library.views import MediaCreateView, MediaDeleteView, MediaUpdateView

urlpatterns = patterns('library.views',
    (r'^$', 'media_list', {}, 'media-list'),
    (r'^add/$', login_required(MediaCreateView.as_view()), {}, 'media-add'),
    (r'^(?P<pk>\d+)/edit/$', login_required(MediaUpdateView.as_view()),
     {}, 'media-edit'),
    (r'^(?P<pk>\d+)/delete/$', login_required(MediaDeleteView.as_view()),
     {}, 'media-delete'),
    (r'^row_count/$', 'row_count_preference', {}, 'row-count-pref'),
)
