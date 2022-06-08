from django.shortcuts import render
from .models import SurveyTemplates
from django.views.generic import ListView, TemplateView
# Create your views here.

class HomeView(TemplateView):
    """Home Page"""
    template_name = "surveytemplate/index.html"


class TemplateListVew(ListView):
    """"List all Templates"""
    model = SurveyTemplates
    template_name = "surveytemplate/listtemplate.html"


