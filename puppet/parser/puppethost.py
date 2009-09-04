from django.conf import settings
#from parser.config import *
from parser.util import *

import os
import time
import yaml

class puppetHost:
	
	def __init__(self, hostname = '', yamlfiles = []):
		self.name = hostname
		self.yamlfiles = yamlfiles
		self.reportdir = settings.REPORTDIR

	def __init__(self, hostname = '', reportdir = ''):
		self.name = hostname
		self.reportdir = settings.REPORTDIR
		
	def __str__(self):
		return 'Hostname (reports: %s): %s' % (len(self.yamlfiles), self.name)
	
	def total_reports(self):
		return len(self.yamlfiles)
			
	def loadFacts(self):
		yamlfile = settings.YAMLDIR + "/facts/" + self.name + ".yaml"
		return load_yaml(yamlfile)
		
	#return a list of yaml files parsed to dict from a specific host
	def get_yamls(self):
		print 'getting yamsl for host %s' % self.name
		inicio = start_counter()
		self.yaml_files = os.listdir(self.reportdir + '/' + self.name)
		#TODO cachear o yamls
		yamls = []
		for yaml in self.yaml_files:
			yamls.append(load_yaml(self.reportdir + '/' + self.name + '/' + yaml))
		elapsed(inicio)
		return yamls

