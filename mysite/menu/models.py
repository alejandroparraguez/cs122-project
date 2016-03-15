'''
import datetime

from django.db import models
from django.utils import timezone
#Created by Django, classes written by us


class addressQuestion(models.Model):
	
	Creates class for address question with question text.
	
	question_text = models.CharField(max_length=200)

	def __str__(self):
		return self.question_text

class choiceQuestion(models.Model):

	Creates class for address question with question text.

	question_text = models.CharField(max_length=200)

	def __str__(self):
		return self.question_text

class cityQuestion(models.Model):
	
	Creates class for city question with question text.
	
	question_text = models.CharField(max_length=200)
	

	def __str__(self):
			return self.question_text

class Response(models.Model):
	
	Creates class for response to choice question with response text.
	
	question = models.ForeignKey(choiceQuestion, on_delete=models.CASCADE)
	response_text = models.CharField(max_length=200)

	def __str__(self):
		return self.response_text

'''
