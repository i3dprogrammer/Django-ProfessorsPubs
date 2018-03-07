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
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    department = models.ForeignKey(Department)
    affiliation = models.ForeignKey(Affiliation)

    def __str__(self):
        return self.name