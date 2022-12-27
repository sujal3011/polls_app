from django.db import models
from datetime import datetime
# from django.contrib.postgres.fields import ArrayField

class Poll(models.Model):
    question=models.TextField()
    option_one=models.CharField(max_length=20)
    option_two=models.CharField(max_length=20)
    option_three=models.CharField(max_length=20)
    option_one_count=models.IntegerField(default=0)
    option_two_count=models.IntegerField(default=0)
    option_three_count=models.IntegerField(default=0)

    deadline=models.DateField(default=datetime.now().today())

    # options= models.ArrayField(models.CharField(max_length=20),size=5)
    # options_count= models.ArrayField(models.IntegerField(default=0),size=5)

    created_by=models.CharField(max_length=20,default="user")


    def __str__(self):
         return self.question