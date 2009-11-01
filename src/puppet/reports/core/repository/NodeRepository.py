from core import util
from django.conf import settings

import os
import sys
import re
import logging


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

#returns json object
#TODO: rever, esta velho
def find_roles_json():
	roles_list = []
	role_to_host = {}
	host_to_id = {}
	util.test_path(NODES_FILE)
	start = 0
	count = 0
	host = ''
	#creates root node
	role_aux = {}
	role_aux['id'] = str(count)
	role_aux['name'] = 'roles'
	data = {}
	adjacencies = []
	data['url'] = '/puppet/'
	role_aux['data'] = data
	role_aux['adjacencies'] = adjacencies
	roles_list.append(role_aux)
	
	#children_host = {}
	for line in open(NODES_FILE, 'r'):
		line = line.strip()
		if start == 0:
			if line.startswith('node \''):
				start = 1
				matchobj = re.match('node.*\'(.*)\'', line)
				host = matchobj.group(1)
				if not host.endswith('.globoi.com'):
					host = host + '.globoi.com'
				host_to_id[host] = str(count)
				role_aux = {}
				role_aux['id'] = str(count)
				role_aux['name'] = host
				data = {}
				adjacencies = []
				data['url'] = '/puppet/viewlog/' + host + '/'
				role_aux['data'] = data
				role_aux['adjacencies'] = adjacencies
				roles_list.append(role_aux)
				
				'''
				id = host_to_id[host]
				name = host
				data = {}
				data['url'] = '/puppet/viewlog/' + host + '/'
				children_host['name'] = name
				children_host['id'] = id
				children_host['data'] = data
				'''
		elif start == 1:
			if line.startswith('}'):
				start = 0
				host = ''
				children_host = {}
			else:
				if line.startswith('include'):
					role = line.split()[1]
					role_aux = {}
					role_aux['id'] = str(count)
					role_aux['name'] = role
					data = {}
					adjacencies = []
					if host:
						#adjacencies.append(children_host)
						adjacencies.append(host_to_id[host])
					
					role_aux['data'] = data	
					role_aux['adjacencies'] = adjacencies
					roles_list.append(role_aux)
					
					#adds adjacency to root node
					roles_list[0]['adjacencies'].append(role_aux['id'])
					l = role_to_host.get(role, [])
					l.append(host)
					role_to_host[role] = l
		count = count + 1

	return util.enconde_json(roles_list)
	
def find_roles_by_host(): pass




