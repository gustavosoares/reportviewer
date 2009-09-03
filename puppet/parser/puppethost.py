from parser.config import *
from parser.util import *

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
		yamlfile = YAMLDIR + "/facts/" + self.name + ".yaml"
		return load_yaml(yamlfile)

