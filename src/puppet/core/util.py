import time
import os
import yaml
import hashlib
import logging

#Parses puppets reports dir
'''
def parse_report(reportdir):
	hosts = os.listdir(reportdir)
	host_to_yaml = {}
	for host in hosts:
		yamls = os.listdir(reportdir + '/' + host)
		host_to_yaml[host] = yamls
	
	return host_to_yaml
'''
	
#Parses a yaml file to a python dictionary
def load_yaml(yamlfile):
	yaml_dict = {}
	test_path(yamlfile)
	file = open(yamlfile, 'r')
	c = file.read()
	#replaces some weirdness
	c = c.replace('--- !ruby/object:Puppet::Node::Facts','')
	c = c.replace('--- !ruby/object:Puppet::Transaction::Report','')
	c = c.replace(' !ruby/object:Puppet::Util::Log','')
	c = c.replace('!ruby/object:Puppet::Util::Metric','')
	c = c.replace('!ruby/object:RRDtool','')
	c = c.rstrip('\n')	
	yaml_dict = yaml.load(c)
	
	return yaml_dict
	
def start_counter():
	return time.time()
	
def elapsed(inicio):
	fim = time.time()
	elapsed = (fim - inicio) / 60
	#print 'duracao: %f min' % elapsed
	logging.debug('duracao: %.2f min' % elapsed)
	return elapsed

def test_path(filename):
	"""test if a path exist"""
	if not os.path.exists(filename):
		raise Exception, 'Path %s does not exists' % filename
		
def md5(raw_text):
	return hashlib.md5(raw_text).hexdigest()
