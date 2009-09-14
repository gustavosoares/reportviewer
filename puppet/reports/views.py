# -*- coding: utf-8 -*-
# Create your views here.
import logging
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.shortcuts import render_to_response

from parser.util import *
from parser.puppethost import puppetHost

def reports(request):

	logging.debug('listing reports in %s for hosts' % settings.REPORTDIR)
	
	hosts_dir = os.listdir(settings.REPORTDIR)
	hosts = []
	for host in hosts_dir:
		p = puppetHost(host, settings.REPORTDIR)
		p.list_yamls()
		hosts.append(p)

	logging.debug('done listing reports for hosts')
	
	return render_to_response('reports.html', { 'hosts' : hosts })
	
def facts(request, hostname=''):
	yamlfile = settings.YAMLDIR + "/facts/" + hostname + ".yaml"
	facts = load_yaml(yamlfile)
	return render_to_response('facts.html', { 'hostname' : hostname, 'facts' : facts })

def viewlog(request, hostname='', yamlfile=None):
	
	if yamlfile != None:

		logging.info('getting yamlfile %s for host %s' % (yamlfile, hostname))
		p = puppetHost(hostname, settings.REPORTDIR)
		yaml = p.get_yaml(yamlfile)
		logs = yaml['logs']
		logcount = len(logs)
		r = p.get_report(yamlfile)
		return render_to_response('viewlog.html',
			{ 'yamlfile' : yamlfile,
			  'logcount' : logcount,
			  'logs' : logs,
			  'report' : r,
			  'hostname' : hostname,
			})

	else:
		inicio = start_counter()
		logging.info('getting info for hostname %s' % hostname)
		p = puppetHost(hostname, settings.REPORTDIR)
		p.list_yamls()
		reports = p.get_reportlist()
		gen_time = '%.2f' % elapsed(inicio)

		return render_to_response('viewhosts.html', 
			{ 'hostname' : hostname,
			'rrdroot' : settings.RRDROOT,
			'gen_time' : gen_time,
			'reports' : reports })			
