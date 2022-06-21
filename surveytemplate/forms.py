from .models import GroupName, SurveyTemplates, Recepient
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

#create group form
class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = GroupName
        fields = ['group_name']

        widgets = {
            'group_name': forms.TextInput(attrs={
            'class': 'form-control',
            'id':"example-text-input",
            'type' : 'text',
            'placeholder': 'Group Name',
            }),
            # 'subject': forms.TextInput(attrs={
            # 'class': 'form-control',
            # 'id':"example-text-input",
            # 'type' : 'text',
            # 'placeholder': 'Subject'}),
            
            # 'body': forms.Textarea(attrs={
            # 'rows': 10,
            # 'class': 'form-control',
            # 'id':'exampleTextarea',
            # 'placeholder': 'Template Body'}),

            # 'is_active':forms.CheckboxInput(attrs={
            #     'type':'checkbox',
            #     'name':'Checkboxes1',
                
                
            # })
         }

class CreateRecepientForm(forms.ModelForm):
    class Meta:
        model = Recepient
        fields = ['first_name', 'last_name', 'email', 'address', 'is_active']
        
        #groups = GroupName.objects.all()
        # group = forms.ModelMultipleChoiceField(queryset=GroupName.objects, widget=forms.CheckboxSelectMultiple(attrs={
        #     'type':'checkbox',
        #     'class': 'form-check-input',
        #     'name': 'groups',
        #      'id' : 'flexCheckDefault',
        #     }),
        #      required=False)

        widgets = {
            'first_name': forms.TextInput(attrs={
            'class': 'form-control',
            'id':"example-text-input",
            'type' : 'text',
            'placeholder': 'First Name',
            }),

            'last_name': forms.TextInput(attrs={
            'class': 'form-control',
            'id':"example-text-input",
            'type' : 'text',
            'placeholder': 'Last Name',
            }),
            'email': forms.EmailInput(attrs={
            'class': 'form-control',
            'id':"example-text-input",
            'type' : 'text',
            'placeholder': 'Email',
            }),
            'address': forms.TextInput(attrs={
            'class': 'form-control',
            'id':"example-text-input",
            'type' : 'text',
            'placeholder': 'Address',
            }),

            'is_active':forms.CheckboxInput(attrs={
                'type':'checkbox',
                'name':'Checkboxes1',      
            }),
            # 'group': forms.CheckboxSelectMultiple(attrs={
            #     'type': 'checkbox',
            #     'class': 'select multiple',
            #     'name': 'groups',
            #     'id' : 'flexCheckDefault',
            #     'queryset':groups
                
            # })
         }