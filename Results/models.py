from django.db import models
from django.contrib.auth import get_user_model

from Quiz.models import Quiz


UserModel = get_user_model()

# Create your models here.

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)