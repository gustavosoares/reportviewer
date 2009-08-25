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
		yamlfile = YAMLDIR + "/facts/" + self.hostname + ".yaml"
		if os.path.exists(yamlfile):
			self.facts = yaml.load(yamlfile)
			print self.facts
		else:
			print 'File %s does not exists' % yamlfile			

