# -*- coding: utf-8 -*-
# Create your views here.
import logging
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.shortcuts import render_to_response
from django.core.cache import cache

from puppet.core import util
from puppet.reports.core.domain.puppethost import puppetHost
from puppet.reports.core.domain.role import role
from puppet.reports.core.repository import NodeRepository

import os

NodeRepository.NODES_FILES = settings.NODES_FILES

def index(request):
	return list_roles(request)

def list_roles(request):
	"""retorna lista de roles"""
	logging.debug('listing roles...')
	roles = NodeRepository.find_roles()
	logging.debug('done listing roles')
	logging.info(roles)
	return render_to_response('reports/list_roles.html', { 'roles' : roles })

def view_tree(request):
	"""retorna a arvore hiperbolica com as dependencias"""
	#print 'common: %s' % NodeRepository.get_includes('common')
	#print 'puppet::comon: %s' % NodeRepository.get_includes('puppet::common')
	#print 'nodes.pp: %s' % NodeRepository.get_includes('nodes.pp')
	
	deps, json = NodeRepository.map_dependencies()
	
	#return HttpResponse('teste')
		
	return render_to_response('reports/tree.html', 
		{ 'arvore_json' : json })
	
def viewrole(request, name=''):

	inicio = util.start_counter()
	logging.info('getting information for role %s' % name)
	r = role(name)
	logging.debug('variaveis(%s): %s' % (r.total_variables(),r.variables))
	logging.debug('includes(%s): %s' % (r.total_includes(),r.includes))

	gen_time = '%.2f' % util.elapsed(inicio)

	return render_to_response('reports/viewrole.html', 
		{ 'role' : r,
		'gen_time' : gen_time})

def list_hosts(request):
	"""list informations for hosts in the report dir"""
	logging.debug('listing reports in %s for hosts' % settings.REPORTDIR)
	
	hosts_dir = os.listdir(settings.REPORTDIR)
	hosts = []
	for host in hosts_dir:
		p = puppetHost(host, settings.REPORTDIR)
		p.list_yamls()
		hosts.append(p)

	logging.debug('done listing reports for hosts')
	
	return render_to_response('reports/list_hosts.html', { 'hosts' : hosts })
	
def facts(request, hostname=''):
	yamlfile = settings.YAMLDIR + "/facts/" + hostname + ".yaml"
	facts = util.load_yaml(yamlfile)
	return render_to_response('reports/facts.html', 
				{ 'hostname' : hostname, 'facts' : facts })

def graph(request, hostname=''):
	return render_to_response('reports/graph.html', 
				{ 'hostname' : hostname, 'rrd_dir' : settings.RRDDIR })

def viewlog(request, hostname='', yamlfile=None):
	"""view log information for host in the specified yamlfile"""
	if yamlfile != None:
		logging.info('getting yamlfile %s for host %s' % (yamlfile, hostname))
		p = puppetHost(hostname, settings.REPORTDIR)
		yaml = p.get_yaml(yamlfile)
		logs = yaml['logs']
		logcount = len(logs)
		r = p.get_report(yamlfile)
		return render_to_response('reports/viewlog.html',
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

		return render_to_response('reports/viewhosts.html', 
			{ 'hostname' : hostname,
			'rrdroot' : settings.RRDROOT,
			'gen_time' : gen_time,
			'reports' : reports })

