from parser.config import *

import os
import yaml

class puppetHost:
	
	def __init__(self, hostname = '', yamlfiles = []):
		self.name = hostname
		self.yamlfiles = yamlfiles
		self.reportdir = REPORTDIR
		
	def __str__(self):
		return 'Hostname (reports: %s): %s' % (len(self.yamlfiles), self.name)
	
	def total_reports(self):
		return len(self.yamlfiles)
			
	def loadFacts(self):
		self.facts = {}
		yamlfile = YAMLDIR + "/facts/" + self.name + ".yaml"
		if os.path.exists(yamlfile):
			file = open(yamlfile, 'r')
			c = file.read()
			c = c.replace('--- !ruby/object:Puppet::Node::Facts','')
			self.facts = yaml.load(c)
		else:
			raise 'File %s does not exists' % yamlfile			
		
		return self.facts
