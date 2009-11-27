from fabric.api import *
import setup

setup._config()

## STAGES ##
def lab():
	'''### Seta configuracoes de lab'''
	env.stage = 'lab'
	env.roledefs = {
    	'web': ['riovld48.globoi.com'],
    	'filer': ['riovld48.globoi.com']
	}

def homolog():
	'''### Seta configuracoes do ambiente de homologacao'''
	env.stage = 'homolog'
	env.roledefs = {
    	'web': ['riold133.globoi.com','riold134.globoi.com'],
    	'filer': ['riold133.globoi.com','riold134.globoi.com']
	}

def staging():
	'''### Seta configuracoes de staging'''
	env.stage = 'staging'
	env.roledefs = {
    	'web': ['riolb346.globoi.com','riolb347.globoi.com'],
    	'filer': ['riolb346.globoi.com','riolb347.globoi.com']
	}
	
def prod():
	'''### Seta configuracoes de prod'''
	env.stage = 'prod'
	env.roledefs = {
    	'web': ['riolb348.globoi.com','riolb349.globoi.com'],
    	'filer': ['riolb348.globoi.com','riolb349.globoi.com']
	}

## FIM STAGES ##
