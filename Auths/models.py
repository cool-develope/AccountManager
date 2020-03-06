from django.db import models
import datetime
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, Group, PermissionsMixin
	)

class MyUserManager(BaseUserManager):
	def create_user(self, username, password = None):
		user = self.model(
			username = username, 
			)
		user.set_password(password)
		user.save(using = self._db)

		return user

	def create_superuser(self, username, password):
		user = self.create_user(username, password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using = self._db)
		return user

class MyUser(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length = 20, unique = True)

	is_virtual = models.BooleanField(default = False)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default = False)

	objects = MyUserManager()
	USERNAME_FIELD = 'username'
	REQUIRED_FIELD = []

	def __str__(self):
		return self.username

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	@property
	def is_staff(self):
		return self.is_admin