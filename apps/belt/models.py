from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        users = User.objects.filter(email = postData['email'])
        if len(users) > 0:
            errors["email"] = "This email has already existed"
        if len(postData['fname']) < 2:
            errors["fname"] = "Your first name is too small"
        if len(postData['lname']) < 2:
            errors["lname"] = "Your last name is too small"    
        if not EMAIL_REGEX.match(postData['email']): 
            errors["email"] = "Email must be valid"
        if len(postData['pcode']) < 8:
            errors["pcode"] = "Password is too small"
        if postData['pcode'] != postData['pcodeCon']:
            errors["pcode"] = "Password does not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if len(user) == 0: 
            errors["email"] = "This email does not exist"
        elif not bcrypt.checkpw(postData['pcode'].encode(), user[0].password.encode()):
            errors["pcode"] = "No Password found"
        return errors


class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Your job title is less than 3 characters"
        if len(postData['description']) < 3:
            errors['description'] = "Your job description is too small"
        if len(postData['location']) < 3:
            errors['location'] = "Job location is required"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Job(models.Model):
    job = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    description = models.TextField()
    user = models.ForeignKey(User, related_name = "job")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = JobManager()
