
class puppetHost:
	
	def __init__(self, hostname = '', yamlfiles = [], reportdir = ''):
		self.hostname = hostname
		self.yamlfiles = yamlfiles
		self.reportdir = reportdir
		
	def __str__(self):
		return 'Hostname: %s' % (self.hostname)
		#return 'Hostname: %s\nyamlfiles: %s' % (self.hostname, self.yamlfiles)
		
		
