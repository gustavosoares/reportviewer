from fabric.api import *

def rpm(name):
	'''testa se um rpm existe'''
	run("/opt/local/bin/testa_rpm.sh %s" % name)
	
def connects_to(host, port):
	'''testa conectividade'''
	run("/opt/local/bin/testa_tcp.sh %s %s" % (host, port))

def filer(mount_point):
	'''testa se mount point existe'''
	run("/opt/local/bin/testa_filer.sh %s" % (mount_point))
	
def is_entry_at_host(host_string):
	'''testa se uma entrada esta no hosts'''
	run("grep %s /etc/hosts" % (host_string))
