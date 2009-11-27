from django.utils import simplejson as json

def encode_json(obj):
	"""encode an object to json"""
	return json.dumps(obj)
