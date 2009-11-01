from django.conf.urls.defaults import *
from django.conf import settings
from puppet.reports import views



urlpatterns = patterns('',
    # Example:
    # (r'^puc/', include('puc.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^/?$', views.index),
    (r'^hosts/?$', views.list_hosts),
    (r'^roles/?$', views.list_roles),    
    (r'^facts/(?P<hostname>[^/]+)$', views.facts),
    (r'^graph/(?P<hostname>[^/]+)$', views.graph),
    (r'^viewlog/(?P<hostname>[^/]+)/(?P<yamlfile>[^/]+)?$', views.viewlog),
    (r'^viewrole/(?P<name>[^/]+)$', views.viewrole),
)

import os

path = os.path.dirname(__file__)
MEDIA_ROOT = (os.path.abspath(path + '/media'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s' % MEDIA_ROOT}),
    )
