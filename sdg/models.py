from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
# Create your models here.

class Article(models.Model):
    Author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    category = models.CharField(max_length=255)

    def serialize(self):
        return {
            "id": self.id,
            "Author": self.Author.username,
            "title": self.title,
            "date": self.date,
            "content": self.content, 
            "category": self.category
        }

class Project(models.Model):
    title = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    # made the model like this because I didn't understand how
    # to add a dictionay to a django model
    Incompletegoals = models.TextField(blank=True)
    Completegoals = models.TextField(blank=True)

    def serialize(self):
        return {
            "title": self.title,
            "category": self.category,
            "completedGoals": self.Completegoals 
        }