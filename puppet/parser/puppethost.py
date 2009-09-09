from django.conf import settings
#from parser.config import *
from parser.util import *
from parser.puppetreport import puppetReport

import os
import time
import yaml
import logging

class puppetHost:
	
	#def __init__(self, hostname = '', yamlfiles = []):
	#	self.name = hostname
	#	self.yamlfiles = yamlfiles
	#	self.reportdir = settings.REPORTDIR

	def __init__(self, hostname = '', reportdir = ''):
		self.name = hostname
		self.reportdir = settings.REPORTDIR
		self.yamlfiles = []
		#list with dicts of yamls
		self.yamls = []
		self.reports_list = []

	#lists yamls files for the host
	def list_yamls(self):
		self.yamlfiles = os.listdir(self.reportdir + '/' + self.name)
	
	def __str__(self):
		return 'Hostname (reports: %s): %s' % (len(self.yamlfiles), self.name)
	
	def total_reports(self):
		return len(self.yamlfiles)
			
	def loadFacts(self):
		yamlfile = settings.YAMLDIR + "/facts/" + self.name + ".yaml"
		return load_yaml(yamlfile)
		
	#return a list of yaml files parsed to dict from a specific host
	def get_yamls(self, yamlfile=None):

		if not yamlfile:
			if len(self.yamls) == 0:
				logging.debug('getting yamls for host %s' % self.name)
				inicio = start_counter()
				self.list_yamls()
				#TODO cachear o yamls
				for yaml in self.yamlfiles:
					if yaml.endswith(".yaml"):
						yaml_content = load_yaml(self.reportdir + '/' + self.name + '/' + yaml)
						self.yamls.append(yaml_content)
				elapsed(inicio)
			else:
				logging.debug("yamls returned")
		else:
			logging.debug("loading yaml %s" % yamlfile)
			inicio = start_counter()
			if yamlfile.endswith(".yaml"):
				yaml_content = load_yaml(self.reportdir + '/' + self.name + '/' + yamlfile)
				self.yamls.append(yaml_content)
			elapsed(inicio)
			
		return self.yamls

	def clear_yamls(self):
		self.yamls = []
		logging.debug('yamls list cleared')

	#gets a report for a specific yamlfile
	def get_report(self, yamlfile):
		yaml = self.get_yaml(yamlfile)
		r = puppetReport()
		r.count_changes = yaml['metrics']['changes']['values'][0][2]
		
		r.out_of_sync = yaml['metrics']['resources']['values'][3][2]
		r.failed_restarts = yaml['metrics']['resources']['values'][0][2]
		r.failed = yaml['metrics']['resources']['values'][1][2]
		r.restarted = yaml['metrics']['resources']['values'][6][2]
		r.count_resources = yaml['metrics']['resources']['values'][7][2]
		
		r.run_time = yaml['metrics']['time']['values'][1][2]
		r.config_retrieval = yaml['metrics']['time']['values'][0][2]
		r.set_datetime(yaml['time'])
		logging.debug('*' * 70)
		logging.debug('time: %s' % r.formatted_datetime())	
		logging.debug('changes: %s' % r.count_changes)
		logging.debug('out_of_sync: %s' % r.out_of_sync)
	
		logging.debug('failed_restarts: %s' % r.failed_restarts)
		logging.debug('failed: %s' % r.failed)
		logging.debug('restarted: %s' % r.restarted)

		logging.debug('resources: %s' % r.count_resources)
		logging.debug('run_time: %s' % r.runtime())
		logging.debug('config_retrieval: %s' % r.configretrieval())
		logging.debug('yamlfile: %s' % r.yamlfile_name())
		return r
		
	#returns a report list
	#TODO: remove redudancies
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
				r.set_datetime(yaml['time'])
				#commented cause it seems to be the same of changes
				#r.log_lines = len(yaml['logs'])
				self.reports_list.append(r)
				logging.debug('*' * 70)
				logging.debug('time: %s' % r.formatted_datetime())	
				logging.debug('changes: %s' % r.count_changes)
				logging.debug('out_of_sync: %s' % r.out_of_sync)
				logging.debug('resources: %s' % r.count_resources)
				logging.debug('run_time: %s' % r.runtime())
				logging.debug('yamlfile: %s' % r.yamlfile_name())

		return self.reports_list


	#returns a report list
	'''
	def get_reportlist(self):
		yamls = self.get_yamls()
		if len(self.reports_list) == 0:
			logging.debug("getting report list for host %s" % self.name)
			for yaml in self.yamlfiles:
				r = self.get_report(yaml)
				self.reports_list.append(r)

		return self.reports_list
		
	'''
	
	def get_yaml(self, yamlfile):
		logging.debug('getting log lines from yamlfile %s' % yamlfile)
		return self.get_yamls(yamlfile)[0]
		
		
		
		
		
		
		
		
		
		
		
