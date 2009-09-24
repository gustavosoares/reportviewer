from django.contrib import admin
from django.contrib.auth.models import User
from puppet.monitor.models import ResourceMonitor

class ResourceMonitorAdmin(admin.ModelAdmin):
	list_display = ('user', 'pattern')
	list_filter = ('user',)
	ordering = ('-user',)

admin.site.register(ResourceMonitor, ResourceMonitorAdmin)
#admin.site.register(ResourceMonitor)