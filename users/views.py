import json
import random

from ai_core import advisors, CategoryAdvisor, Tools
from events.models import Event
from users.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response as Res

# region Constants
RES_SUCCESS = 0
RES_FAILURE = 1
RES_BAD_REQUEST = -1


# endregion


def user_exists(username):
	return User.objects.filter(username=username).exists()


def is_user_valid(username, password):
	if user_exists(username):
		user = User.objects.get(username=username)
		return user.password == password
	return False


def init_category_advisors(user):
	if user not in advisors:
		temp = {}
		for category in Tools.cat_map:
			category_id = category['id']

			# create or load the advisor object from storage
			temp[category_id] = CategoryAdvisor.recover(user=user, category_id=category_id) if CategoryAdvisor.is_backed_up(user=user, category_id=category_id) else CategoryAdvisor.create(
				user=user, category_id=category_id)

			# populate data if not exists or lacks
			if not Event.objects.filter(user=user, category_id=category_id).exists() or len(Event.objects.filter(user=user, category_id=category_id)) < 10:
				day = category['day']
				start_time = category['time']
				for x in range(0, 10):
					Event.objects.create_event(user=user, day=day, start_time=start_time + random.randrange(-1, 2, 1), length=60, category_id=category['id'], is_active=False)

			# retrain the network completely
			data_hr = []
			data_dy = []
			for event in Event.objects.filter(user=user, category_id=category_id):
				data_hr.append(event.start_time)
				data_dy.append(event.day)

			temp[category_id].retrain_complete(data_hr, data_dy)
		# add the created bunch of advisors
		advisors[user] = temp


@api_view(['POST'])
def handle_login(request):
	req_body = request.body.decode('utf-8')
	json_body = json.loads(req_body)
	if 'username' in json_body and 'password' in json_body:
		if is_user_valid(json_body['username'], json_body['password']):
			user = User.objects.get(username=json_body['username'])
			init_category_advisors(user=user)
			return Res(data={'result': RES_SUCCESS})
		else:
			return Res(data={'result': RES_FAILURE})
	return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Username or Password was not passed as a POST argument!'})


@api_view(['POST'])
def handle_register(request):
	req_body = request.body.decode('utf-8')
	json_body = json.loads(req_body)

	if 'username' in json_body and 'password' in json_body and 'email' in json_body:
		username = json_body['username']
		password = json_body['password']
		email = json_body['email']

		if user_exists(username):
			return Res(data={'result': RES_FAILURE})
		else:
			User.objects.create_user(username=username, password=password, email=email)
			return Res(data={'result': RES_SUCCESS})
	else:
		return Res(data={'result': RES_BAD_REQUEST, 'reason': 'either of username, password, or email was not passed as a POST argument!'})
