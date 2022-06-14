from .models import SurveyTemplates
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
#login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
			"class":"form-control form-control-user",
			"type":"text",
			"placeholder":"Username",
	}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
			"class":"form-control form-control-user",
			"type":"password",
			"placeholder":"Enter password",
	}))

#registration form
class RegisterForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"text",
		"placeholder":"First Name",
	}))

	last_name = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"text",
		"placeholder":"Last Name",
	}))

	username = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"text",
		"placeholder":"Username",
	}))

	email = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"email",
		"placeholder":"Email",
	}))
	
	password1 = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"password",
		"placeholder":"Password..Min 8 characters",
	}))

	password2 = forms.CharField(widget=forms.TextInput(attrs={
		"class":"form-control form-control-user",
		"type":"password",
		"placeholder":"Re-enter Password",
	}))

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=True)
    #     user.email = self.cleaned_data['email']
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.username = self.cleaned_data['username']
    #     if commit:
    #         user.save()
    #     return user
