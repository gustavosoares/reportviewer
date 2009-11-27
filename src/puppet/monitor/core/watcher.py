# -*- coding: utf-8 -*-

import sys
import os
import logging
import re
import datetime

#INITIAL SETUP
#cache timeout to store email body to prevent from sending the same email twice
CACHE_TIMEOUT = 86400 * 2 #48horas
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = "%s/../../.." % PROJECT_ROOT

sys.path.insert(0, PROJECT_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'puppet.settings'
os.chdir(PROJECT_ROOT)

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from puppet.monitor.models import Monitor
from puppet.monitor.core.repository import MonitorRepository
from puppet.core.repository import UserRepository
from puppet.core import util
from puppet.reports.core.domain.puppethost import puppetHost

'''
def send_email(subject, message, from_email, to):
	email = EmailMessage(subject, message, from_email, to)
	email.content_subtype = "html"
	email.send()
'''
 
email_buffer = {}

def run():

	"""start program run"""

	print 'PROJECT_ROOT: %s' % PROJECT_ROOT
	print 'CACHE_TIMEOUT: %s' % CACHE_TIMEOUT

	inicio = util.start_counter()
	
	print 'listing monitors and users...'
	user_list = UserRepository.list_user()
	monitor_list = MonitorRepository.list_monitor()

	print 'monitor list: %s' % monitor_list
	print 'user list: %s' % user_list

	print 'done...'

	user_hosts_dict = {}
	hosts =  os.listdir(settings.REPORTDIR)
	#lista com os emails para serem enviados
	
	for monitor in monitor_list:
		print '#' * 80
		print '##Checking monitors for user %s' % monitor.user.email
		print 'email buffer: %s' % email_buffer
		host_monitors = monitor.get_host_monitors()
		#check if the user has a monitor for the host, if he has then it means that he wants everything from host
		monitoring_host = False
		#caches the hosts for the user
		hosts_for_user = user_hosts_dict.get(monitor.user.email,None)
		if not hosts_for_user:
			hosts_for_user = monitor.get_hosts()
			user_hosts_dict[monitor.user.email] = hosts_for_user

		for host in hosts:
			print 'Reading host: %s' % host
			puppet_host = puppetHost(host, settings.REPORTDIR)
			yamlfile = puppet_host.get_last_yaml()
			if not yamlfile:
				continue
				
			print 'last yamlfile: %s' % yamlfile
			yaml = puppet_host.get_yaml(yamlfile)
			logs = yaml['logs']
			if len(logs) == 0:
				continue		
			
			##
			for host_ in hosts_for_user:
				if host.startswith(host_):
					monitoring_host = True
					break
			
			if monitoring_host:
				print '####user %s is monitoring %s' % (monitor.user.email, host)
				email_body = ''
				for log in logs:
					source = log['source']
					email_body_aux = '''
	<tr class=""><td>%s</td><td colspan=6>%s</td></tr>
	<tr class=""><td></td><td colspan=6>&nbsp;&nbsp;%s</td></tr>
	''' % (log['level'], log['message'], source)
					email_body = email_body + email_body_aux
					
				key_cache = monitor.user.email + '_' + host
				#key_cache = monitor.user.email + '_' + email
				#send_email(email_body, monitor, yamlfile, key_cache, host)
				add_to_email_buffer(email_body, monitor, yamlfile, key_cache, host)
			
			else:
				resource_monitors = monitor.get_resource_monitors()
				for resource_monitor in resource_monitors:
					pattern = resource_monitor.pattern
					email_body = ''
					for log in logs:
						source = log['source']
						#print 'pattern: %s' % monitor.pattern
						#regex = re.compile(monitor.pattern)
						#matchobj = regex.search(source)
						matchobj = source.find(pattern)
						if matchobj != -1:
							email_body_aux = '''
		<tr class=""><td>%s</td><td colspan=6>%s</td></tr>
		<tr class=""><td></td><td colspan=6>&nbsp;&nbsp;%s</td></tr>
		''' % (log['level'], log['message'], source)
							#red color on the pattern
							email_body_aux = email_body_aux.replace(pattern,'<b><font color=red>'+pattern+'</b></font>')
							email_body = email_body + email_body_aux
							
					#sends email if not already sent
					key_cache = monitor.user.email
					#send_email(email_body, monitor, yamlfile, key_cache, host)
					add_to_email_buffer(email_body, monitor, yamlfile, key_cache, host)
			
			#send_email_from_buffer
			print 'sending email from buffer'
			send_email_from_buffer(monitor)
		monitor.update_last_run()
		print '*' * 60

	gen_time = '%.2f' % util.elapsed(inicio)
	print '%s min' % gen_time	

def send_email(email_body='', monitor=None, yamlfile='', key_cache='', host=''):
	"""process the email to be sent"""
	if (len(email_body) != 0):
		md5_body = util.md5(email_body)
		key_cache = key_cache + '_' + md5_body
		print 'MD5 key cache: %s' % key_cache
		cached = cache.get(key_cache)
		if cached:
			print 'email com o conteudo do report %s ja enviado. key cache: %s' % (yamlfile, key_cache)
		else:
			to = [monitor.user.email]
			user = monitor.user
			subject = '[GLB-PUPPET] - Modificação em recurso monitorado'
			message = get_email_message_in_html(host, email_body, yamlfile)
			try:
				from_email='puppetmonitor@no-reply'
				email = EmailMessage(subject, message, from_email, to)
				email.content_subtype = "html"
				email.send()
				print 'Usuario notificado %s (%s)' % (user.username, user.email)
				cache.set(key_cache, 'ok', CACHE_TIMEOUT)
				email_body = ''
			except Exception, e:
				print 'ERRO: %s ao enviar email para %s' % (sys.exc_info(), user.email)

def add_to_email_buffer(email_body='', monitor=None, yamlfile='', key_cache='', host=''):
	"""adds an entry to the email buffer"""
	if (len(email_body) != 0):
		md5_body = util.md5(email_body)
		key_cache = key_cache + '_' + md5_body
		print 'MD5 key cache: %s' % key_cache
		cached = cache.get(key_cache)
		if cached:
			print 'email com o conteudo do report %s ja enviado. key cache: %s' % (yamlfile, key_cache)
		else:
			message = get_email_message_in_html(host, email_body, yamlfile)
			try:
				cache.set(key_cache, 'ok', CACHE_TIMEOUT)
				email_body = ''
				a_buffer = email_buffer.get(monitor.user.email,{})
				a_buffer['monitor'] = monitor
				a_buffer['message'] = message
				email_buffer[monitor.user.email] = a_buffer
			except Exception, e:
				print 'ERRO: %s adicionar email no buffer %s' % (sys.exc_info(), user.email)	

def send_email_from_buffer(monitor):
	"""send email from buffer"""
	global email_buffer
	print 'email buffer: %s' % email_buffer
	a_buffer = email_buffer.get(monitor.user.email,None)
	if a_buffer != None:
		to = [monitor.user.email]
		user = monitor.user
		subject = '[GLB-PUPPET] - Modificação em recurso monitorado'
		message = email_buffer[monitor.user.email]['message']
		if len(message) > 0:
			try:
				from_email='puppetmonitor@no-reply'
				email = EmailMessage(subject, message, from_email, to)
				email.content_subtype = "html"
				email.send()
				print 'email enviado para %s (%s)' % (user.username, user.email)
				#nao precisa cachear pois o cache e por email
				email_body = ''
				#limpo o buffer
				email_buffer = None
			except Exception, e:
				print 'ERRO: %s ao enviar email para %s' % (sys.exc_info(), user.email)
	

def get_email_message_in_html(host, email_body, yamlfile):
	"""returns the email message in html format with the email_body passed"""
	p = puppetHost(host, settings.REPORTDIR)
	report = p.get_report(yamlfile)
	message = u'''
		<center>
		<font color="red">E-mail automatico, por favor nao responder</font><br><br>
		Report obtido no arquivo <b>%s</b>, gerado as <b>%s</b><br><br>
		Alteração no host <b>%s</b> detectada.<br>
		<hr>
		<br>
		<table>
		<tr>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td colspan=2><b><font size=+1>Change Logs</font></b></td>
		</tr>
		<tr>
			<td><b>Level</b></td>
			<td colspan=6><b>Message</b></td>
		</tr>
		%s
		</table>
		<hr>
		</center><br>		
	''' % (yamlfile, report.formatted_datetime_gmt(), host, email_body)
	
	return message

if __name__ == "__main__":
	run()

