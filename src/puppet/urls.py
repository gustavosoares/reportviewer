from django.conf.urls.defaults import *
from puppet.reports.views import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^puppet/?$', list_roles),
    (r'^puppet/hosts/?$', list_hosts),
    (r'^puppet/roles/?$', list_roles),    
    (r'^puppet/facts/(?P<hostname>[^/]+)$', facts),
    (r'^puppet/viewlog/(?P<hostname>[^/]+)/(?P<yamlfile>[^/]+)?$', viewlog),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

from django.conf import settings
import os

path = os.path.dirname(__file__)
MEDIA_ROOT = (os.path.abspath(path + '/media'))

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s' % MEDIA_ROOT}),
    )
    

