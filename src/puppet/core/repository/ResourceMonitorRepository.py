from django.contrib.auth.models import User
from monitor.models import ResourceMonitor

def list_resource_monitor():
	return ResourceMonitor.objects.all()
	
def find_resource_monitor_by_user(id):
	return ResourceMonitor.objects.filter(user=id)
	
