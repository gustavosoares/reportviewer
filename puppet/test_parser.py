
from parser.reports import parse_report
from parser.config import *
from parser.puppethost import puppetHost




reports_dict = parse_report(REPORTDIR)
hosts = []
#print reports_dict

for hostname in reports_dict.keys():
	yamlfiles = reports_dict[hostname]
	hosts.append(puppetHost(hostname, yamlfiles))
	
puppet_host = hosts[0]

puppet_host.loadFacts()

