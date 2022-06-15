from django.contrib import admin
from .models import SurveyTemplates, Recepient,GroupName

# Register your models here.
admin.site.register(SurveyTemplates)
admin.site.register(Recepient)
admin.site.register(GroupName)
