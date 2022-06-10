from .models import SurveyTemplates
from django import forms

class CreateTemplateForm(forms.ModelForm):
    class Meta:
        model = SurveyTemplates
        fields = ['template_name','subject','body','is_active']

        widgets = {
            'template_name': forms.TextInput(attrs={
            'class': 'form-control',
            'id':"example-text-input",
            'type' : 'text',
            'placeholder': 'Template Name',
            }),
            'subject': forms.TextInput(attrs={
            'class': 'form-control',
            'id':"example-text-input",
            'type' : 'text',
            'placeholder': 'Subject'}),
            
            'body': forms.Textarea(attrs={
            'rows': 10,
            'class': 'form-control',
            'id':'exampleTextarea',
            'placeholder': 'Template Body'}),

            'is_active':forms.CheckboxInput(attrs={
                'type':'checkbox',
                'name':'Checkboxes1',
                
                
            })
         }