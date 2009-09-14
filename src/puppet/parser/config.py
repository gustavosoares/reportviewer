from django.conf import settings


# where your reports are stored, same as reportdir in puppet.conf
#REPORTDIR = "/opt/puppet/reports"

# where your rrd files are stored, same as rrddir in puppet.conf
#RRDDIR = "/opt/puppet/rrd"

# where to find the rrd's on the web, can be full url or relative
#RRDROOT = "/rrd"

# where the puppetmaster yaml directory is
#YAMLDIR = "/var/lib/puppet/yaml"


# where your reports are stored, same as reportdir in puppet.conf
REPORTDIR = settings.REPORTDIR

# where your rrd files are stored, same as rrddir in puppet.conf
RRDDIR = settings.RRDDIR

# where to find the rrd's on the web, can be full url or relative
RRDROOT = settings.RRDROOT

# where the puppetmaster yaml directory is
YAMLDIR = settings.YAMLDIR
