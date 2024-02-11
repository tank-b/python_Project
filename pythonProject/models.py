from django.db import models
from datetime import datetime

from django.utils.timezone import now
import time


class Students(models.Model):
    student_id = models.AutoField(primary_key=True, auto_created=True, default = "1")
    login = models.CharField(max_length=15,unique=True, null=False)
    first_name= models.CharField(max_length=120, null=False)
    last_name = models.CharField(max_length=120, null=False)
    email = models.CharField(max_length=120,unique=True,)
    hashed = models.CharField(max_length=120, null=False, default = "0")
    salt = models.CharField(max_length=120, null=False, default = "O")

class Sessions(models.Model):
    session_id = models.AutoField(primary_key=True, auto_created=True)
    date = models.DateField(default = datetime.now)
    opening_hour = models.TimeField(default = datetime.now)
    closing_hour = models.TimeField(default = datetime.now)

class SurveyResults(models.Model):
    poll_id = models.AutoField(primary_key=True, auto_created ="true")
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    advancement = models.DecimalField(max_digits=3, decimal_places=0, null=False)
    difficulty = models.CharField(max_length=15, null=False)
    progression = models.CharField(max_length=15, null=False)
