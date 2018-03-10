import string
import random
from django.contrib.auth.models import User

def generate_random_user(username_length=10, password_length=10, chars=string.ascii_lowercase + string.digits):
	username = ''.join(random.SystemRandom().choice(chars) for _ in range(username_length))
	password = ''.join(random.SystemRandom().choice(chars) for _ in range(password_length))
	if User.objects.filter(username=username).exists():
		generate_random_user(username_length, password_length, chars)
	else:
		User.objects.create_user(username=username, password=password)
		return (username, password)
		

# count = input("Enter the user count you want")

try:
	count = 150
	for i in range(count):
		user = generate_random_user()
		print("Username{0}: {1}".format(i+1, user[0]))
		print("Password{0}: {1}".format(i+1, user[1]))
		print("-----------------------")
except:
	print("That wasn't a valid number.")
