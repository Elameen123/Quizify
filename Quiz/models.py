from django.contrib.auth.models import AbstractUser
from django.db import models

import random

# Create your models here.

# difficulty levels of the quiz
DIFF_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
)


class Owner(AbstractUser):
    pass

# the Quiz table for the quiz App


class Quiz(models.Model):
    user = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    number_of_questions = models.IntegerField()
    duration = models.IntegerField(help_text='duration of the Quiz in minutes')
    Pass_score = models.IntegerField(
        help_text='Required score to pass the Quiz')
    quiz_difficulty = models.CharField(max_length=15, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    # A function to get the quiz questions
    def get_questions(self):
        questions = list(self.question_set.all())
        # choosing a random question from the list of questions
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizzes'
