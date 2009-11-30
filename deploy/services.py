from fabric.api import *
import time

@roles('web')
def stop_httpd():
	'''####### stop httpd'''
	sudo('%s stop' % env.apachectl_be)

@roles('web')
def start_httpd():
	'''####### start httpd'''
	sudo('%s start' % env.apachectl_be)

@roles('web')
def graceful_httpd():
	'''####### graceful do httpd'''
	sudo('%s graceful' % env.apachectl_be)

@roles('web')
def restart_puppetmaster():
	'''####### restart puppet master'''
	stop_httpd()
	time.sleep(5)
	start_httpd()

