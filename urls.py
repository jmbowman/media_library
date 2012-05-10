from django.conf.urls import include, patterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', {}, 'login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login',
     {}, 'logout'),
    (r'^password/$', 'django.contrib.auth.views.password_change',
     {'post_change_redirect': '/library/'}, 'password'),
    (r'^library/', include('library.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
)
