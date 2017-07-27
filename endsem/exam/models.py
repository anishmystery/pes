from django.db import models

class Exam(models.Model):
	p=models.FloatField()
	k=models.FloatField()
	p_k=models.FloatField()