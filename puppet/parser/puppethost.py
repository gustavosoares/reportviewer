from parser.config import *
import os
import yaml

class puppetHost:
	
	def __init__(self, hostname = '', yamlfiles = []):
		self.hostname = hostname
		self.yamlfiles = yamlfiles
		self.reportdir = REPORTDIR
		
	def __str__(self):
		return 'Hostname: %s' % (self.hostname)
		#return 'Hostname: %s\nyamlfiles: %s' % (self.hostname, self.yamlfiles)
		
	def loadFacts(self):
		self.facts = {}
		yamlfile = YAMLDIR + "/facts/" + self.hostname + ".yaml"
		if os.path.exists(yamlfile):
			file = open(yamlfile, 'r')
			c = file.read()
			c = c.replace('--- !ruby/object:Puppet::Node::Facts','')
			self.facts = yaml.load(c)
		else:
			raise 'File %s does not exists' % yamlfile			
		
		return self.facts
