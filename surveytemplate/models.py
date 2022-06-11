from email.headerregistry import Group
from django.db import models

# Create your models here.
class SurveyTemplates(models.Model):
    template_name = models.CharField(max_length=40,null=False)
    subject = models.CharField(max_length=50,null=False)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.template_name

class GroupName(models.Model):
    group_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

class Recepient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    group = models.ManyToManyField(GroupName)

    def __str__(self):
        return self.email

    def get_group(self):
        return self.group.all()


    
