
import os
import yaml

#Parses puppets reports dir
def parse_report(reportdir):
	hosts = os.listdir(reportdir)
	host_to_yaml = {}
	for host in hosts:
		yamls = os.listdir(reportdir + '/' + host)
		host_to_yaml[host] = yamls
	
	return host_to_yaml
	
#Parses a yaml file to a python dictionary
def load_yaml(yamlfile):
	yaml_dict = {}
	if os.path.exists(yamlfile):
		file = open(yamlfile, 'r')
		c = file.read()
		c = c.replace('--- !ruby/object:Puppet::Node::Facts','')
		yaml_dict = yaml.load(c)
	else:
		raise 'Cannot parse yaml file: %s does not exists' % yamlfile			
	
	return yaml_dict	
