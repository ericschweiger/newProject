from django.db import models
from datetime import datetime
import bcrypt, re


class UserManager(models.Manager):
    def registration_validator(self, data):
        errors = {}

        if len(data['name']) < 3:
            errors['name'] = "Your name must be at least 3 characters long (sorry RJ...)"
        if len(data['username']) < 3:
            errors['username'] = "Your username must be at least 3 characters long"
        if len(data['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters long"
        elif data['password'] != data['password_confirm']:
            errors['password'] = "Your passwords to not match! Please try again"

        return errors
    
    def login_validator(self,data):
        errors = {}

        if len(data['username']) < 1:
            errors['username'] = "Your username can not be blank"
        elif len(User.objects.filter(username = data['username'])) < 1:
            errors['username'] = "Please register with us before attempting to login"
        else:
            user = User.objects.get(username = data['username'])
            if not bcrypt.checkpw(data['password'].encode(), user.password.encode()):
                errors['password'] = "Your password was entered incorrectly, please try again"

        return errors

class TripManager(models.Manager):
    def trip_validator(self, data):
        errors = {}

        if len(data['destination']) < 1:
            errors['destination'] = "Please enter a destination"
        if len(data['description']) < 1:
            errors['description'] = "Please enter a description"
        if len(str(data['trip_start'])) < 1:
            errors['trip_start'] = "Pleae enter a start date"
        elif datetime.strptime(data['trip_start'], '%Y-%m-%d') < datetime.now():
            errors['trip_start'] = "You cant go on a trip in the past"
        if len(str(data['trip_end'])) < 1:
            errors['trip_end'] = "Please enter an end date"
        elif datetime.strptime(data['trip_end'], '%Y-%m-%d') < datetime.strptime(data['trip_start'], '%Y-%m-%d'):
            errors['trip_end'] = "Your trip can't end before it begins!"

        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    trip_start = models.DateField()
    trip_end = models.DateField()
    trips = models.ManyToManyField(User, related_name = "trips")
    creator = models.ForeignKey(User, related_name = "trip", on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = TripManager()

