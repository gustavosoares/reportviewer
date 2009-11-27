# Django settings for puppet project.
import logging
import os


LOG_FILENAME = '/tmp/django-puppet.log'

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = LOG_FILENAME,
    filemode = 'a'
)



# where your reports are stored, same as reportdir in puppet.conf
REPORTDIR = "/mnt/puppet/reports"

# where your rrd files are stored, same as rrddir in puppet.conf
RRDDIR = "/mnt/puppet/rrd"

# where to find the rrd's on the web, can be full url or relative
RRDROOT = "/rrd"

# where the puppetmaster yaml directory is
YAMLDIR = "/mnt/puppet/yaml"

#NODES_FILE = "/etc/puppet/manifests/nodes.pp"

NODES_FILES = (
    '/mnt/puppet/conf/manifests/nodes.pp',
    '/mnt/puppet/conf/manifests/nodes_lab.pp',
    '/mnt/puppet/conf/manifests/nodes_homolog.pp',
    '/mnt/puppet/conf/manifests/nodes_staging.pp',
    '/mnt/puppet/conf/manifests/nodes_prod.pp',
)

ROLES_DIR = "/mnt/puppet/conf/manifests/classes/roles"

#7 days cache
CACHE_BACKEND = "memcached://localhost:11211/?timeout=604800"

EMAIL_HOST = "localhost"
EMAIL_PORT = 25

path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIRS = (os.path.abspath(path + '/templates'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = PROJECT_ROOT + '/puppet_django.db'
DATABASE_NAME = '/opt/puppet/puppet_django.db'
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
path = os.path.dirname(__file__)
MEDIA_ROOT = (os.path.abspath(path + '/media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'm+kvg6fo+coof2@6e+(b32etsuc#5867qz0!7_!)65sk=63is7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'puppet.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'puppet.memcache_status',
    'puppet.reports',
    'puppet.monitor',
)
