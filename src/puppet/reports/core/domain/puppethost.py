import os
import time
import yaml
import logging

from django.conf import settings
from django.core.cache import cache
from puppet.core import util
from puppet.reports.core.domain.puppetreport import puppetReport


class puppetHost:
	
	def __init__(self, hostname = '', reportdir = ''):
		self.name = hostname
		self.reportdir = settings.REPORTDIR
		self.yamlfiles = []
		#list with dicts of yamls
		self.yamls = []
		self.reports_list = []

	#lists yamls files for the host
	def list_yamls(self):
		"""lists all yamlfiles"""
		self.yamlfiles = os.listdir(self.reportdir + '/' + self.name)
		self.yamlfiles.sort()
		return self.yamlfiles

	def get_last_yaml(self):
		"""returns last yaml file generated"""
		y = self.list_yamls()
		return y[len(y)-1]
	
	def __str__(self):
		return 'Hostname (reports: %s): %s' % (len(self.yamlfiles), self.name)
	
	def total_reports(self):
		return len(self.yamlfiles)
			
	def loadFacts(self):
		yamlfile = settings.YAMLDIR + "/facts/" + self.name + ".yaml"
		return util.load_yaml(yamlfile)

	def get_yaml(self, yamlfile):
		#return self.load_yaml(yamlfile)
		logging.debug('getting yamlfile %s' % yamlfile)
		inicio = util.start_counter()
		yaml_content = {}
		if yamlfile.endswith(".yaml"):
			yaml_content = cache.get(yamlfile)
			if not yaml_content:
				logging.debug('yamlfile %s not cached' % yamlfile)
				yaml_content = util.load_yaml(self.reportdir + '/' + self.name + '/' + yamlfile)
				cache.set(yamlfile, yaml_content)
			else:
				logging.debug('yamlfile %s returned from cache' % yamlfile)
				
			self.yamls.append(yaml_content)
		util.elapsed(inicio)
		return yaml_content

					
	#return a list of ALL yaml files parsed to dict from a specific host
	def get_all_yamls(self):

		if len(self.yamls) == 0:
			logging.debug('getting all yamls for host %s' % self.name)
			inicio = start_counter()
			for yaml in self.yamlfiles:
				util.load_yaml(yaml)
			elapsed(inicio)
		else:
			logging.debug("yamls returned from cache")
		
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
		'''
		logging.debug('*' * 70)
		logging.debug('time: %s' % r.formatted_datetime_gmt())	
		logging.debug('changes: %s' % r.count_changes)
		logging.debug('out_of_sync: %s' % r.out_of_sync)
	
		logging.debug('failed_restarts: %s' % r.failed_restarts)
		logging.debug('failed: %s' % r.failed)
		logging.debug('restarted: %s' % r.restarted)

		logging.debug('resources: %s' % r.count_resources)
		logging.debug('run_time: %s' % r.runtime())
		logging.debug('config_retrieval: %s' % r.configretrieval())
		logging.debug('yamlfile: %s' % r.yamlfile_name())
		'''
		return r
		
	#returns a report list
	def get_reportlist(self):
		if len(self.reports_list) == 0:
			logging.debug("getting report list for host %s" % self.name)
			for yaml in self.yamlfiles:
				r = self.get_report(yaml)
				if r.count_changes != 0:
					self.reports_list.append(r)

		return self.reports_list	


