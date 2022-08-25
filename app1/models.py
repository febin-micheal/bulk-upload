from django.db import models

# Create your models here.

class Grade(models.Model):
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.code

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
