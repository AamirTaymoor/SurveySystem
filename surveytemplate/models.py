from django.db import models

# Create your models here.
class SurveyTemplates(models.Model):
    template_name = models.CharField(max_length=40,null=False)
    subject = models.CharField(max_length=50,null=False)
    body = models.TextField()
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.template_name

    
