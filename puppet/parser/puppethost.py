from django.conf import settings
#from parser.config import *
from parser.util import *
from parser.puppetreport import puppetReport

import os
import time
import yaml
import logging

class puppetHost:
	
	def __init__(self, hostname = '', yamlfiles = []):
		self.name = hostname
		self.yamlfiles = yamlfiles
		self.reportdir = settings.REPORTDIR

	def __init__(self, hostname = '', reportdir = ''):
		self.name = hostname
		self.reportdir = settings.REPORTDIR
		self.yamls = []
		self.reports_list = []
		
	def __str__(self):
		return 'Hostname (reports: %s): %s' % (len(self.yamlfiles), self.name)
	
	def total_reports(self):
		return len(self.yamlfiles)
			
	def loadFacts(self):
		yamlfile = settings.YAMLDIR + "/facts/" + self.name + ".yaml"
		return load_yaml(yamlfile)
		
	#return a list of yaml files parsed to dict from a specific host
	def get_yamls(self):
		#print 'getting yamls for host %s' % self.name
		if len(self.yamls) == 0:
			logging.debug('getting yamls for host %s' % self.name)
			inicio = start_counter()
			self.yaml_files = os.listdir(self.reportdir + '/' + self.name)
			#TODO cachear o yamls
			for yaml in self.yaml_files:
				if yaml.endswith(".yaml"):
					self.yamls.append(load_yaml(self.reportdir + '/' + self.name + '/' + yaml))
			elapsed(inicio)
			#logging.debug('yamls: %s' % self.yamls[0])
		else:
			logging.debug("yamls returned")
		return self.yamls

	def clear_yamls(self):
		self.yamls = []
		logging.debug('yamls list cleared')

	#returns a report list
	def get_reportlist(self):
		yamls = self.get_yamls()
		if len(self.reports_list) == 0:
			logging.debug("getting report list for host %s" % self.name)
			for yaml in yamls:
				r = puppetReport()
				r.count_changes = yaml['metrics']['changes']['values'][0][2]
				r.out_of_sync = yaml['metrics']['resources']['values'][3][2]
				r.count_resources = yaml['metrics']['resources']['values'][7][2]
				r.run_time = yaml['metrics']['time']['values'][1][2]
				logging.debug('changes: %s' % r.count_changes)
				logging.debug('out_of_sync: %s' % r.out_of_sync)
				logging.debug('resources: %s' % r.count_resources)
				logging.debug('run_time: %s' % r.run_time)