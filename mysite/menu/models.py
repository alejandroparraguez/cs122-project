import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class addressQuestion(models.Model):
	question_text = models.CharField(max_length=200)

	def __str__(self):
		return self.question_text

class choiceQuestion(models.Model):
	question_text = models.CharField(max_length=200)

	def __str__(self):
		return self.question_text

class cityQuestion(models.Model):
	city_choices = (("chicago", u'Chicago'),
					("new_york", u'New York'),
					("san_francisco", u'San Francisco'))
	question_text = models.CharField(max_length=200)
	

	def __str__(self):
			return self.question_text

class Response(models.Model):
	question = models.ForeignKey(choiceQuestion, on_delete=models.CASCADE)
	response_text = models.CharField(max_length=200)

	def __str__(self):
		return self.response_text
