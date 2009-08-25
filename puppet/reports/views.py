# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

def reports(request):
	print 'report dir: %s' % settings.REPORTDIR
	#parse reportdir
	
	return render_to_response('reports.html')
