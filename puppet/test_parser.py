
#from parser.reports import parse_report
from parser.util import *
#from parser.puppethost import puppetHost


#As definicoes do diretorios sao obtidas pelo import parser.config


yamlfile = '/opt/puppet/reports/riovld46.globoi.com/200909010020.yaml'
#yamlfile = '/tmp/teste.yaml'
yaml = load_yaml(yamlfile)
print yaml
