import os
import re
#from parser.reports import parse_report
from core import util
#from core.repository import noderepository
#from parser.puppethost import puppetHost


#As definicoes do diretorios sao obtidas pelo import parser.config

'''
print 'list dir performance'
inicio = start_counter()
yamlfiles = os.listdir('/opt/puppet/reports/riovld46.globoi.com/')
yamlfiles.sort()
elapsed(inicio)
print '*' * 60
print ''
print 'ls performance'
inicio = start_counter()
yamlfiles_ls = os.popen('ls /opt/puppet/reports/riovld46.globoi.com/').readlines()
elapsed(inicio)
print '*' * 60
print ''
print yamlfiles_ls
'''

#print noderepository.find_roles()

#yamlfile = '/opt/puppet/reports/riovld46.globoi.com/200909010020.yaml'
#yamlfile = '/tmp/teste.yaml'
#yaml = load_yaml(yamlfile)

p = re.compile('profil*')
print p
matchobj = p.search('/etc/profile')
if matchobj:
	print 'achouuu'
else:
	print 'nao achou'




