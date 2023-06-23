from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    # Add more fields as per your requirements

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # Add more fields as per your requirements
