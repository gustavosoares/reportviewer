import os, sys
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.abspath("%s/.." % PROJECT_ROOT))
#sys.path.insert(0, os.path.abspath("%s/../packages" % PROJECT_ROOT))
sys.path.insert(0, PROJECT_ROOT)


os.environ['DJANGO_SETTINGS_MODULE'] = 'puppet.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

print >> sys.stderr, sys.path

