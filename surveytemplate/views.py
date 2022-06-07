from django.shortcuts import render
from .models import SurveyTemplates
from django.views.generic import ListView, TemplateView
# Create your views here.

class TemplateListVew(ListView):
    """"Displays all Templates"""
    model = SurveyTemplates
    template_name = ""

class HomeView(TemplateView):
    template_name = "index.html"
