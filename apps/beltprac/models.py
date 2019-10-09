    
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-copyZ0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


now = str(datetime.now())

# VALIDATION
class LogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        try : 
            User.objects.get(email = postData["email"])
            errors["email"] = "This Email is in Use, please Login or Register a new email!"
        except:
            
            if len(postData["name"]) < 3:
                errors["name"] = "Name must be at least 3 characters"
            if len(postData["alias"]) < 3:
                errors["alias"] = "Alias must be at least 3 characters"
            if len(postData["password"]) < 8:
                errors["password"] = "Password must be at least 8 characters"
            if postData['password'] != postData['confirm']:
                errors['confirm'] = 'Password fields do NOT match!'
            print("this is the email--->", postData['email'])
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] ="Invalid email"
        return errors

    def login_validator(self, postData):
        errors = {}
        if not User.objects.filter(email = postData['loginEmail']):
            errors['loginEmail'] = "Email or Password invalid!"
        if len(postData['loginPassword']) < 8:
            errors['loginPassword'] = "Password or Email Invalid"

        return errors




# TABLES
class Author(models.Model):
    name = models.CharField(max_length=255)

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    alias = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = LogManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    user =  models.ForeignKey(User, related_name="books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = LogManager()

class Review(models.Model):
    desc = models.CharField(max_length=500)
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


#     #ONE TO MANY RELATIONSHIP
#     added_by = models.ForeignKey(User, related_name="plans", on_delete = models.CASCADE)

#     destination = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     description = models.CharField(max_length=255)

#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)

#     objects = PlanManager()

# #MANY TO MANY RELATIONSHIP
# class Favorite(models.Model):
#     user = models.ForeignKey(User, related_name="user_favorites", on_delete = models.CASCADE)
#     plan = models.ForeignKey(Plan, related_name="plan_favorites", on_delete = models.CASCADE)

# # END OF TABLES