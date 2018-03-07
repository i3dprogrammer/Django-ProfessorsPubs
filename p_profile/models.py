from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Affiliation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProfessorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    affiliation = models.ForeignKey(Affiliation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name