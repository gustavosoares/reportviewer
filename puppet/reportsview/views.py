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
	print 'report dir: %s' % settings.REPORTDIR
	#parse reportdir
	hosts_to_yaml = parse_report(settings.REPORTDIR)
	hosts = []

	for hostname in hosts_to_yaml.keys():
		yamlfiles = hosts_to_yaml[hostname]
		p = puppetHost(hostname, yamlfiles)
		hosts.append(p)

	return render_to_response('reports.html', { 'hosts' : hosts })
	
def facts(request, hostname=''):
	yamlfile = settings.YAMLDIR + "/facts/" + hostname + ".yaml"
	facts = load_yaml(yamlfile)
	return render_to_response('facts.html', { 'hostname' : hostname, 'facts' : facts })

def viewlog(request, hostname=''):
	#print 'view log for %s' % hostname
	logging.info('view log for %s' % hostname)
	p = puppetHost(hostname, settings.REPORTDIR)
	yamls_list = p.get_yamls()
	p.get_reportlist()
	return render_to_response('viewlog.html', 
		{ 'hostname' : hostname,
		'rrdroot' : settings.RRDROOT,
		'yamls' : yamls_list })	
