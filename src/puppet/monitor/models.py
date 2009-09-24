from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResourceMonitor(models.Model):
	user = models.ForeignKey(User)
	pattern = models.CharField(max_length=200)
	
	def __unicode__(self):
		return u'%s is monitoring the pattern \"%s\"' % (self.user.username, self.pattern)