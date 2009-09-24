from django.contrib.auth.models import User


def list_user():
	return User.objects.all()
	
def find_user_by_id(user_id):
	return User.objects.get(id=user_id)
	
def find_user_by_name(user_name):
	return User.objects.get(username=user_name)


