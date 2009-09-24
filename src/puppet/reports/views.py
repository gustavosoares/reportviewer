# -*- coding: utf-8 -*-
# Create your views here.
import logging
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.shortcuts import render_to_response
from django.core.cache import cache

from core import util
from core.puppet.puppethost import puppetHost
from core.puppet.role import role
from core.repository import NodeRepository

import os

def list_hosts(request):

	logging.debug('listing reports in %s for hosts' % settings.REPORTDIR)
	
	hosts_dir = os.listdir(settings.REPORTDIR)
	hosts = []
	for host in hosts_dir:
		p = puppetHost(host, settings.REPORTDIR)
		p.list_yamls()
		hosts.append(p)

	logging.debug('done listing reports for hosts')
	
	return render_to_response('list_hosts.html', { 'hosts' : hosts })

def list_roles(request):

	logging.debug('listing roles in %s' % settings.NODES_FILE)
	
	role_to_host = NodeRepository.find_roles()
	#json_obj = NodeRepository.find_roles_json()
	#json_obj = util.enconde_json(role_to_host)
	#logging.debug('json object: %s' % json_obj)
	logging.debug('done listing roles')
	
	return render_to_response('list_roles.html', 
			{ 'roles' : role_to_host })
	
def facts(request, hostname=''):
	yamlfile = settings.YAMLDIR + "/facts/" + hostname + ".yaml"
	facts = util.load_yaml(yamlfile)
	return render_to_response('facts.html', 
				{ 'hostname' : hostname, 'facts' : facts })

def graph(request, hostname=''):
	return render_to_response('graph.html', 
				{ 'hostname' : hostname, 'rrd_dir' : settings.RRDDIR })

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
	
		inicio = util.start_counter()
		logging.info('getting info for hostname %s' % hostname)
		p = puppetHost(hostname, settings.REPORTDIR)
		p.list_yamls()
		reports = p.get_reportlist()
		gen_time = '%.2f' % util.elapsed(inicio)

		return render_to_response('viewhosts.html', 
			{ 'hostname' : hostname,
			'rrdroot' : settings.RRDROOT,
			'gen_time' : gen_time,
			'reports' : reports })

def viewrole(request, name=''):

	inicio = util.start_counter()
	logging.info('getting role %s' % name)
	r = role(name)
	logging.debug('variaveis(%s): %s' % (r.total_variables(),r.variables))
	logging.debug('includes(%s): %s' % (r.total_includes(),r.includes))

	gen_time = '%.2f' % util.elapsed(inicio)

	return render_to_response('viewrole.html', 
		{ 'role' : r,
		'roles_file' : settings.ROLES_FILE,
		'gen_time' : gen_time})
