#-*- coding:utf-8 -*-
from django.template.loader import render_to_string
import datetime
from puppet.core import json

class NoHiperbolico(object):
	
	def __init__(self):
		"""construtor"""
		self.id = 0
		self.name = ''
		self.data = {}
		self.children = []
		self.type = 'circle'
		self.color = '#f00'
		self.dim = 10
	
	def add_children(self, no):
		"""
		metodo para adicionar um nó filho
		recebe como parametro um objeto NoHiperbolico
		"""
		self.children.append(str(no))
		
	def add_data(self, key, value):
		"""
		permite adicionar um metadado ao nó
		"""
		self.data[key] = value
	
	def __repr__(self):
		return self.__str__()
		
	def __str__(self):
		"""
		método __str__ sobreescrito para retornar um objeto json (string) da
		representacao do objeto
		"""
		
		dict = {}
		
		self.add_data('$color', self.color)
		self.add_data('$dim', self.dim)
		self.add_data('$type', self.type)
		
		dict['id'] = self.id
		dict['name'] = self.name
		dict['data'] = self.data
		dict['children'] = self.children
		
		s = json.encode_json(dict)
		#replaces de lixos no json
		s = s.replace('\\"','"')
		s = s.replace('["{"','[{"')
		s = s.replace('"}"]','"}]')
		s = s.replace('"{"','{"')
		s = s.replace('}",','},')
		return s
		
