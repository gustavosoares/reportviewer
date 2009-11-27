from django.contrib.auth.models import User
from puppet.monitor.models import Monitor

def list_monitor():
	return Monitor.objects.all()
	
def find_monitor_by_user(user_obj):
	return Monitor.objects.filter(user=user_obj)
	
