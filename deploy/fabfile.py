from fabric.api import *
from fabric import state
from stages import *
from services import *
from setup import *
import services
#import setup
import datetime
import time
import os

state.output['debug'] = True
state.aborts = True

env.timestamp = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
env.release_sufix = 'releases/' + env.timestamp 

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
 
@roles('web')
def deploy_be():
	'''###### Deploy para o ambiente escolhido com o comando fab [AMB] deploy'''
	#update_be()
	check_be()
	os.chdir(PROJECT_ROOT + '/../src')
	#criaco e upload
	print local('pwd && ls -l')
	local('tar --exclude=.git/* --exclude=.git* --exclude=*.unfiltered --exclude=*.rb --exclude=deploy/* --exclude=deploy* -cvzf /tmp/package-%s.tar.gz .' % env.application)
	env.deploy_release_dir = env.filer_dir + '/' + env.release_sufix + '/' + env.application
	print run('umask 002 && mkdir -p %s' % env.deploy_release_dir)
	print put('/tmp/package-%s.tar.gz' % env.application,'%s/package-%s.tar.gz' % (env.deploy_release_dir, env.application))
	
	#abrindo pacote e criando link de current de cada um
	cmd = '''
		cd %s && umask 002 && 
		tar -xzf %s/package-%s.tar.gz && 
		rm -f %s/package-%s.tar.gz
	''' % (env.deploy_release_dir, env.deploy_release_dir, env.application, env.deploy_release_dir, env.application)
	run(cmd)

	cmd = '''
		rm -f %s/current && 
		umask 002 && 
		ln -s %s %s/current
	''' % (env.filer_dir, env.deploy_release_dir, env.filer_dir)
	run(cmd)
	local("rm /tmp/package-%s.tar.gz" % env.application)
	
	#link para a pasta current
	output = run('cd /opt/puppet/django && rm -rf puppet > /dev/null && ln -s %s/current/puppet' % env.filer_dir)
	print 'dando graceful no httpd'
	services.graceful_httpd()

@roles('web')
def deploy():
	'''###### Deploy para o ambiente escolhido'''
	deploy_be()

@roles('web')
def releases():
	'''#### Lista os releases disponiveis no servidor'''
	run("ls -lad %s/current | awk -F 'releases/' '{print $2}' > /tmp/release.current; for x in `ls -r %s/releases`; do if [ \"$x\" == \"`cat /tmp/release.current`\" ]; then echo \"$x <- current\"; else echo $x; fi; done; rm /tmp/release.current" % (env.filer_dir, env.filer_dir))

@roles('web')
def syncbd():
	'''### Sincroniza o banco de dados'''
	print run("cd /opt/puppet/django/puppet; python2.5 manage.py loaddata monitor/fixtures/initial_data.json")

@roles('web')
def reset_bd():
	'''### Reseta o banco de dados'''
	apps = ['monitor', 'reports']
	for app in apps:
		cmd = "cd /opt/puppet/django/puppet; python2.5 manage.py sqlclear %s | python2.5 manage.py dbshell" % app
		print run(cmd)
	print run("cd /opt/puppet/django/puppet; python2.5 manage.py syncdb")
	print 'dando graceful no httpd'
	services.graceful_httpd()

def help():
	'''##### Ajuda do fabric'''
	print ''
	print '#' * 60
	print ''
	print '#### Deploy para o backend'
	print '\tfab lab deploy'
	print '#### Setup no backend'
	print '\tfab lab setup'
	print '#### Sync do banco de dados'
	print '\tfab lab syncbd'
	print '#### Reset do banco de dados'
	print '\tfab lab reset_bd'
	print '#### Restart do puppet master'
	print '\tfab lab restart_puppetmaster'
