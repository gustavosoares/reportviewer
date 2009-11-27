from django.conf import settings

from time import gmtime, strftime
import os
import time
import yaml
import logging
from pytz import timezone
import pytz


class puppetReport:
	
	def __init__(self):
		self.count_changes = 0
		self.out_of_sync = 0
		self.failed_restarts = 0
		self.failed = 0
		self.restarted = 0
		self.count_resources = 0
		self.run_time = 0.0
		self.config_retrieval = 0.0
		self.log_lines = 0
		self.datetime = None
		self.datetime_gmt = None
		self.tzone = timezone(settings.TIME_ZONE)
		self.tzone_utc = pytz.utc
	
	def set_datetime(self, datetime):
		self.datetime = self.tzone_utc.localize(datetime)
		self.datetime_gmt = self.datetime.astimezone(self.tzone)

	def runtime(self):
		return '%.2f' % self.run_time

	def configretrieval(self):
		return '%.2f' % self.config_retrieval
		
	def formatted_datetime(self):
		return self.datetime.strftime('%d/%m/%Y %H:%M:%S')

	def formatted_datetime_gmt(self):
		return self.datetime_gmt.strftime('%d/%m/%Y %H:%M:%S')
			
	def yamlfile_name(self):
		n = '%s.yaml' % self.datetime.strftime('%Y%m%d%H%M')
		return n
