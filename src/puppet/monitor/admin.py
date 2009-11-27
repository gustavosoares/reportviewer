from django.contrib import admin
from django.contrib.auth.models import User
from puppet.monitor.models import Monitor, HostMonitor, ResourceMonitor


class ResourceMonitorAdmin(admin.ModelAdmin):
	search_fields = ('pattern',)
	list_display = ('pattern',)
	list_filter = ('pattern',)
	ordering = ('-pattern',)
	
class HostMonitorAdmin(admin.ModelAdmin):
	search_fields = ('hostname',)
	list_display = ('hostname','description')
	list_filter = ('hostname',)
	ordering = ('-hostname',)


class MonitorAdmin(admin.ModelAdmin):
	list_display = ('user', 'last_run', 'log_level', 'get_host_monitors', 'get_resource_monitors')
	list_filter = ('user', 'host_monitors', 'resource_monitors')
	ordering = ('-user',)
	fields = ('user', 'log_level', 'host_monitors', 'resource_monitors')
	filter_horizontal = ('host_monitors', 'resource_monitors',)
	

admin.site.register(Monitor, MonitorAdmin)
admin.site.register(HostMonitor, HostMonitorAdmin)
admin.site.register(ResourceMonitor, ResourceMonitorAdmin)
