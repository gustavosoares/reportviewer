from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class HostMonitor(models.Model):
	hostname = models.CharField('hostname', max_length=200)
	description = models.CharField(blank=True, null=True, max_length=500)
	def __unicode__(self):
		return u'%s' % (self.hostname)


class ResourceMonitor(models.Model):
	pattern = models.CharField(max_length=200)
	
	def __unicode__(self):
		return u'%s' % (self.pattern)
		
class Monitor(models.Model):
	user = models.ForeignKey(User)
	log_level = models.CharField(blank=True, null=True, max_length=100)
	last_run = models.DateTimeField(blank=True, null=True)
	host_monitors = models.ManyToManyField(HostMonitor)
	resource_monitors = models.ManyToManyField(ResourceMonitor)

	def get_host_monitors(self):
	    return self.host_monitors.all()

	def get_resource_monitors(self):
	    return self.resource_monitors.all()

	def get_hosts(self):
		hosts = []
		for host_monitor in self.get_host_monitors():
			hosts.append(host_monitor.hostname)
		return hosts
	
	def update_last_run(self):
		now = datetime.datetime.now()
		Monitor.objects.filter(id=self.id).update(last_run=now)
		
	def __unicode__(self):
		return u'Monitor for %s' % (self.user.username)
		

