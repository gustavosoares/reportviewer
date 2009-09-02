
from parser.reports import parse_report
from parser.config import *
from parser.puppethost import puppetHost


#As definicoes do diretorios sao obtidas pelo import parser.config

reports_dict = parse_report(REPORTDIR)
hosts = []
#print reports_dict

for hostname in reports_dict.keys():
	yamlfiles = reports_dict[hostname]
	hosts.append(puppetHost(hostname, yamlfiles))
	
puppet_host = hosts[0]

facts = puppet_host.loadFacts()
print '*' * 60
print 'facts: %s\n' % facts
