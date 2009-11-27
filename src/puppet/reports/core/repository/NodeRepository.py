# -*- coding: utf-8 -*-
from puppet.core import util
from django.conf import settings
from puppet.reports.core.domain.nohiperbolico import NoHiperbolico

import os
import sys
import re
import logging
import copy

#NODES_FILE = "/etc/puppet/manifests/nodes.pp"
NODES_FILES = ""

def find_roles():
	roles = {}
	#Ex.: {'abc' : {'hosts' : [], 'nodefile' : 'filename'}}
	for NODES_FILE in NODES_FILES:
		#file with nodes definition existis?
		util.test_path(NODES_FILE)
		start = 0
		count = 0
		host = ''
		for line in open(NODES_FILE, 'r'):
			line = line.strip()
			if start == 0:
				if line.startswith('node \''):
					start = 1
					matchobj = re.match('node.*\'(.*)\'', line)
					host = matchobj.group(1)
					#is a server name?
					if not host.startswith('rio'):
						continue
					if not host.endswith('.globoi.com'):
						host = host + '.globoi.com'
						#hosts file existis?
						host_dir = settings.REPORTDIR + '/' + host
						logging.debug('host dir: %s' % host_dir)
						try:
							util.test_path(host_dir)
						except Exception, e:
							logging.warn(e)
							start = 0
			elif start == 1:
				if line.startswith('}'):
					start = 0
					host = ''
				else:
					if line.startswith('include'):
						role = line.split()[1]
						role_dict = roles.get(role, {})
						l = role_dict.get('hosts', [])
						l.append(host)
						role_dict['hosts'] = l
						role_dict['nodefile'] = NODES_FILE 
						roles[role] = role_dict
			count = count + 1
	return roles	


def get_tree():
	pass


def get_file_for_resource(resource):
	"""gets the name of the file which the resource is implemented"""
	filename_prefix = 'modules'
	filename = ''
	if resource.startswith('role_'):
		filename = 'manifests/classes/roles/' + resource[5:] + '.pp'
	elif resource.startswith('nodes_'):
		filename = 'manifests/' + resource + '.pp'
	else:
		if resource.find('::') == -1:
			if resource.endswith('.pp'):
				filename = 'manifests/' + resource
			else:
				filename = filename_prefix + '/' + resource + '/manifests/init.pp'
		else:
			l = resource.split('::')
			m = l[0]
			f = l[1]
			filename = filename_prefix + '/' + m + '/manifests/classes/' + f + '.pp'
	
	return filename
	
def get_includes(include_name):
	"""returns list of includes"""
	filename_prefix = '/mnt/puppet/conf'
	filename = filename_prefix + '/' + get_file_for_resource(include_name)
	
	logging.debug('filename: %s'% filename)	
	
	if not os.path.exists(filename):
		logging.warn('file %s not found on the system' % filename)
		return None
	else:
		includes = []
		for line in open(filename, 'r'):
			line = line.strip()
			if line.startswith('include'):
				l = line.split()
				if l[1] not in includes:
					includes.append(l[1])
			elif line.startswith('import'):
				l = line.split()
				import_ = l[1]
				import_ = import_[1:len(import_)-1]
				#print g[1:len(g)-1]
				if import_ not in includes:
					includes.append(import_)
		return includes

def map_dependencies_from_start_point(start):
	"""maps dependencies from a start point"""
	dependencies = {}
	tree_nodes = {}
	
	raiz = NoHiperbolico()
	raiz.id = 0
	raiz.name = '/etc/puppet'
	raiz.dim = 10
	counter = 1
	
	#DFS
	stack_open = []
	stack_closed = []
	stack_open.append(start)
	
	first = get_file_for_resource(start)
	h = NoHiperbolico()
	h.id = counter
	h.name = first
	raiz.add_children(h)
	
	tree_nodes['/etc/puppet'] = raiz
	tree_nodes[first] = h

	counter = counter + 1
	#create graph with dependencies
	while (len(stack_open) != 0):
	
		logging.debug('stack open: %s' % stack_open)
		logging.debug('stack closed: %s' % stack_closed)
		
		first = stack_open.pop()
		includes = get_includes(first)
		if includes != None:	
			
			for include in includes:
				if include not in stack_open:
					stack_open.append(include)
			
			includes_aux = []
			for include in includes:
				includes_aux.append(get_file_for_resource(include))
				
				h = tree_nodes.get(get_file_for_resource(first), None)
				if h == None:
					logging.debug('criando no para %s' % get_file_for_resource(first))
					h = NoHiperbolico()
					h.id = counter
					h.dim = 10
					h.name = get_file_for_resource(first)
					tree_nodes[get_file_for_resource(first)] = h
					print tree_nodes[get_file_for_resource(first)]
					counter = counter + 1
				else:
					logging.debug('#### no encontrado para %s' % get_file_for_resource(first))

				child = tree_nodes.get(get_file_for_resource(include), None)
				if child == None:
					logging.debug('criando no para %s' % get_file_for_resource(include))
					child = NoHiperbolico()
					child.id = counter
					child.dim = 10
					child.name = get_file_for_resource(include)
					tree_nodes[get_file_for_resource(include)] = child
					counter = counter + 1


			dependencies[get_file_for_resource(first)] = includes_aux
			stack_closed.append(first)
		else:
			dependencies[get_file_for_resource(first)] = 'ERROR'
		counter = counter + 1
	
	start_point = get_file_for_resource(start)
	
	#######################
	#Updates the tree nodes
	#REVERSE DFS
	stack_leafs = []
	for father,childs in dependencies.items():
		if len(childs) == 0:
			stack_leafs.append(father)

	logging.debug('*' * 50)
	logging.debug('\n### folhas: %s\n' % stack_leafs)
	logging.debug('*' * 100)

	logging.debug('@' * 70)
	logging.debug('start_point: %s' % start_point)
	logging.debug('@' * 70)
	
	######################
	#acha o caminho das folhas para a raiz
	for leaf in stack_leafs:
		paths = search_graph(start_point, leaf, dependencies)
		logging.debug('## caminho partindo de %s para %s' % (start_point, leaf))
		for path in paths:
			logging.debug('\t %s' % path)
		logging.debug('\n')
		logging.debug('## atualizando a arvore hiperbolica')
		for path in paths:
			count = len(path)
			last_index = count - 1
			while (last_index > 0):
				previous = last_index - 1
				tree_nodes[path[previous]].add_children(tree_nodes[path[last_index]])
				last_index = last_index - 1
		logging.debug('## done')
	
	#######################
	raiz.add_children(tree_nodes[start_point])

	return dependencies, raiz

def map_dependencies():
	
	return map_dependencies_from_start_point('nodes.pp')

def find_roles_by_host(): pass

def search_graph(start, goal, graph):
	"""searchs a path in a graph"""
	solns = []
	generate([start], goal, solns, graph)
	return solns

def generate(path, goal, solns, graph):
	state = path[-1]
	#print 'path: %s' % path
	if state == goal:
		solns.append(path)
	else:
		for arc in graph[state]:
			if arc not in path:
				generate(path + [arc], goal, solns, graph )


