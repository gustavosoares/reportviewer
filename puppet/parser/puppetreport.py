from django.conf import settings
#from parser.config import *
from parser.util import *

import os
import time
import yaml
import logging

class puppetReport:
	
	def __init__(self):
		self.count_changes = 0
		self.out_of_sync = 0
		self.count_resources = 0
		self.run_time = 0.0
