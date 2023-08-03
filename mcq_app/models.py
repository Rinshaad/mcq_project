from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text
    
class Answer(models.Model):
    question= models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marks = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username
    
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)