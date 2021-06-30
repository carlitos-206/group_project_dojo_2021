from django.db import models
from functools import total_ordering
from sre_constants import error
from django.db import models
import re
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import TimeField
import bcrypt
from datetime import datetime, time, date, timedelta

#---------------------The models below: Users and UserManager--------------------------------

class UserManager(models.Manager):
    def user_validation(request, postData):
        errors={}
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX= re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')
        email_exist=Users.objects.filter(email=postData['email'])
        username_exist=Users.objects.filter(username=postData['username'])
        special_char=['!', '@', '#', '$', '%', '&', '?' ]
        if len(postData['first_name'])<2:
            errors["first_name"]="First Name needs to be more than 2 character"
        if len(postData['last_name'])<2:
            errors["last_name"]="Last Name needs to be more than 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"]="Invalid Email"
        if email_exist:
            errors["email_exist"]="Email already exist"
        
        if not PASSWORD_REGEX.match(postData['password']):
            errors["password"]="Password invalid "
        if username_exist:
            errors["username_exist"]="Username is taken"
        if len(postData['password'])<8:
            errors["pw_too_short"]="Password too short needs to be least 8 characters"
        if len(postData['password'])>20:
            errors["pw_too_long"]="Keep password under 20 characters"
        if not any(char in special_char for char in postData['password']):
            errors['no_special_char_pw']=f"Password needs one special character: {special_char}"
        if not any(char.isdigit() for char in postData['password']):
            errors['no_int_pw']="Password needs least one number"
        if not any(char.isupper() for char in postData['password']):
            errors['no_upper_pw']="Password needs one uppercase letter"
        if not any(char.islower() for char in postData['password']):
            errors['no_lower_pw']="Password needs one lowercase letter"
        if postData['password'] != postData['pw_confirmation']:
            errors["pw_no_match"]='Password fields need to match'
        return errors
    def login_validation(request, password, username):
        existing_user=Users.objects.filter(username=username)
        if existing_user:
            existing_user[0]
            if bcrypt.checkpw(password.encode(), existing_user[0].password.encode()):
                return True
            else:
                return False
class Users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    profile_pic=models.FileField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

#---------------------------END-----------------------------------------

#---------------------The models below: Group and GroupManager--------------------------------
class GroupManager(models.Manager):
    def basic_validator(request, postData):
        errors= {}
        existing_group = Group.objects.filter(name=postData['name'])
        if existing_group:
            errors['group_exist'] = "Group already exist"
        if len(postData['name']) < 3:
            errors['group_name'] = "Group name must contain at least 3 characters"
        if len(postData['genre']) < 3:
            errors['group_genre'] = "Genre must contain at least 3 characters"
        if len(postData['desc']) < 10:
            errors['group_desc'] = "Description must contain least 10 characters"
        if len(postData['desc']) == 0:
            errors['group_desc'] = "Description Field Required"
        if len(postData['rules'])<1:
            errors['group_rules']="Group must have some form of rules"
        return errors

    def member_count(request, postData):
        members=len(postData['joined'])
        return members

class Group(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    desc = models.TextField()
    rules = models.TextField()
    owner = models.ForeignKey(Users, related_name = 'group_leader', on_delete=models.CASCADE)
    joined = models.ManyToManyField(Users, related_name='members')
    day = models.CharField(max_length=255)
    time=models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GroupManager()
#----------------------------END-----------------------------------------

#--------------The Models below: Wall_Message and wallManager-----------

class WallManager(models.Manager):
    def wall_validator(request, postData):
        errors={}
        if len(postData['message'])<1:
            errors['missing_message'] = "Need to write Something atleast"
        return errors

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(Users, related_name='user_messages', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='group_messages', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects= WallManager()