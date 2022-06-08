from django.shortcuts import render
from .models import SurveyTemplates
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
# Create your views here.

class HomeView(TemplateView):
    """Home Page"""
    template_name = "surveytemplate/index.html"


class TemplateListVew(ListView):
    """"List all Templates"""
    model = SurveyTemplates
    template_name = "surveytemplate/listtemplate.html"

class CreateTemplate(CreateView):
     model = SurveyTemplates
     fields = ['template_name','subject','body','is_active']
     success_url = '/templates'

class EditTemplate(UpdateView):
    model = SurveyTemplates
    fields = ['template_name','subject','body','is_active']
    success_url = '/templates'

class DeleteTemplate(DeleteView):
    model = SurveyTemplates
    success_url = '/templates'

