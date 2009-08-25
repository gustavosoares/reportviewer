
import os

def parse_report(reportdir):
	hosts = os.listdir(reportdir)
	host_to_yaml = {}
	for host in hosts:
		yamls = os.listdir(reportdir + '/' + host)
		host_to_yaml[host] = yamls
	
	return host_to_yaml
