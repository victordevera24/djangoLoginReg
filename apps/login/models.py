from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3 and (postData['first_name'].isalpha() != True):
            errors['first_name'] = 'First name must be at least 2 characters and only letters'
        if len(postData['username']) < 3 and (postData['username'].isalpha() != True):
            errors['username'] = 'Username must be at least 2 characters and only letters'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords must match'
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(User.objects.filter(username = postData['username'])) < 1:
            errors['wrong_username'] = 'Incorrect username or password' 
        else:
            u = User.objects.get(username=postData['username'])
            if bcrypt.checkpw(postData['password'].encode(), u.password.encode()) != True:
                errors['wrong_password'] = 'Incorrect username or password'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()


class ItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}
        if len(postData['item_name']) < 3:
            errors['item_name'] = 'Item name must be at least 3 characters'
        if len(Item.objects.filter(item_name = postData['item_name'])) > 0:
            errors['doub_item'] = 'Item already in system' 
        return errors
        


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    wished_users = models.ManyToManyField(User, related_name='wished_items')
    adder = models.ForeignKey(User, related_name = 'added_items')
    objects = ItemManager()
    

