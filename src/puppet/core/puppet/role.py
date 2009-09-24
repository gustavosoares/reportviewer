from django.conf import settings
from django.core.cache import cache
from core import util

import os
import time
import logging

class role:
	
	def __init__(self, name = ''):
		self.name = name
		self.roles_file = settings.ROLES_FILE
		self.variables = {}
		self.includes = []
		start = 0
		#parses roles_file
		for line in open(self.roles_file, 'r'):
			line = line.strip()
			if start == 0:
				if line.startswith('class ' + self.name):
					start = 1
			elif start == 1:
				if line.startswith('}'):
					start = 2
					host = ''
					children_host = {}
				else:
					if line.startswith('$'):
						key, value = line.split('=')
						self.variables[key.strip()] = value.strip()
						logging.debug('key: %s, value: %s' % (key, value))
					elif line.startswith('include '):
						x, include = line.split()
						self.includes.append(include)
						
			elif start ==2:
				break

	def total_variables(self):
		return len(self.variables)

	def total_includes(self):
		return len(self.includes)