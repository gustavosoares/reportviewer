# -*- coding: utf-8 -*-

import sys
import os
import logging
import re

#INITIAL SETUP
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = "%s/../.." % PROJECT_ROOT

print 'PROJECT_ROOT: %s' % PROJECT_ROOT

sys.path.insert(0, PROJECT_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.chdir(PROJECT_ROOT)

from django.conf import settings

#if settings.DATABASE_ENGINE == 'sqlite3':
#	settings.DATABASE_NAME = PROJECT_ROOT + '/puppet_django.db'

from django.core.mail import EmailMessage
from django.core.cache import cache
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from monitor.models import ResourceMonitor
from core.repository import ResourceMonitorRepository
from core.repository import UserRepository
from core import util
from core.puppet.puppethost import puppetHost


def send_email(subject, message, from_email, to):
	email = EmailMessage(subject, message, from_email, to)
	email.content_subtype = "html"
	email.send()


inicio = util.start_counter()

print 'listing monitors and users...'

user_list = UserRepository.list_user()
monitor_list = ResourceMonitorRepository.list_resource_monitor()

print monitor_list
print user_list

print 'done...'

hosts =  os.listdir(settings.REPORTDIR)
email_sent = 0
from_email='puppetmonitor@no-reply'
for host in hosts:
	if email_sent == 1:
		break
	print 'Reading host: %s' % host
	puppet_host = puppetHost(host, settings.REPORTDIR)
	yamlfiles = puppet_host.list_yamls()
	for yamlfile in yamlfiles:
		if email_sent == 1:
			break	
		yaml = puppet_host.get_yaml(yamlfile)
		logs = yaml['logs']
		if len(logs) == 0:
			continue
		#print yamlfile
		for monitor in monitor_list:
			email_body = ''
			for log in logs:
				source = log['source']
				#print 'pattern: %s' % monitor.pattern
				#regex = re.compile(monitor.pattern)
				#matchobj = regex.search(source)
				matchobj = source.find(monitor.pattern)
				if matchobj != -1:
					email_body_aux = '''
<tr class=""><td>%s</td><td colspan=6>%s</td></tr>
<tr class=""><td></td><td colspan=6>&nbsp;&nbsp;%s</td></tr>
''' % (log['level'], log['message'], source)
					email_body_aux = email_body_aux.replace(monitor.pattern,'<b><font color=red>'+monitor.pattern+'</b></font>')
					email_body = email_body + email_body_aux
						
			#sends email if not already sent
			if (len(email_body) != 0):
				md5_body = util.md5(email_body)
				key_cache = monitor.user.email+'_'+md5_body
				print 'MD5 key cache: %s' % key_cache
				cached = cache.get(key_cache)
				if cached:
					print 'email com o conteudo do report %s ja enviado: %s' % (yamlfile, key_cache)
				else:
					to = [monitor.user.email]
					user = monitor.user
					subject = '[GLB-PUPPET] - Modificação em recurso monitorado'
					message = u'''
	<center>
	<font color="red">E-mail automatico, por favor nao responder</font><br><br>
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
	</center>			
	''' % (host, email_body)
					email = EmailMessage(subject, message, from_email, to)
					email.content_subtype = "html"
					email.send()
					print 'Usuario notificado %s (%s)' % (user.username, user.email)
					cache.set(key_cache, 'ok')
					email_body = ''
	print '*' * 60

gen_time = '%.2f' % util.elapsed(inicio)
print '%s min' % gen_time
