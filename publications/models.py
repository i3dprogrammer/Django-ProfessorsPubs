from django.db import models
from django.contrib.auth.models import User

class ResearchField(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Publication(models.Model):

    pub_type_choices = (
        ('1', 'Journal'),
        ('2', 'Confrance'),
        ('3', 'Book'),
    )

    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    research_field = models.ForeignKey(ResearchField)
    authors = models.CharField(max_length=100)
    national = models.BooleanField(default=False)
    date = models.IntegerField(default=0)
    pub_type = models.CharField(max_length=10, choices=pub_type_choices)
    details = models.CharField(max_length=500)
    identifier = models.CharField(max_length=50, null=True, blank=True)
    abstract = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.title