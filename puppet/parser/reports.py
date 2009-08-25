
import os

def parse_report(reportdir):
	print 'Parsing %s' % reportdir
	hosts = os.listdir(reportdir)
	print 'hosts: %s' % hosts
	host_to_yaml = {}
	for host in hosts:
		print 'reading dir: %s' % host
		yamls = os.listdir(reportdir + '/' + host)
		host_to_yaml[host] = yamls
	
	print host_to_yaml