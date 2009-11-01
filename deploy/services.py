from fabric.api import *
import time

def stop_httpd():
	'''####### stop httpd'''
	sudo('%s stop' % env.apachectl_be)

def start_httpd():
	'''####### start httpd'''
	sudo('%s start' % env.apachectl_be)

def graceful_httpd():
	'''####### graceful do httpd'''
	sudo('%s graceful' % env.apachectl_be)
	
def restart_puppetmaster():
	'''####### restart puppet master'''
	stop_puppetmaster()
	time.sleep(5)
	start_puppetmaster()

