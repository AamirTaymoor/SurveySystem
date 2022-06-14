
from re import template
from django.shortcuts import render
from .models import SurveyTemplates
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from .forms import CreateTemplateForm, UserLoginForm, RegisterForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from requests import request
from .models import Recepient, SurveyTemplates, GroupName
from django.views.generic import ListView, TemplateView
from django.utils.datastructures import MultiValueDictKeyError
import pandas as pd
import csv
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from surveytemplate.tasks import EmailTask
from django.contrib.auth import login, authenticate, logout
# Create your views here.

class HomeView(TemplateView):
    """Home Page"""
    template_name = "surveytemplate/index.html"


class TemplateListView(ListView):
    """List all Templates"""
    model = SurveyTemplates
    template_name = "surveytemplate/listtemplate.html"
    

class CreateTemplate(CreateView):
    """Create Template"""
    model = SurveyTemplates
    form_class = CreateTemplateForm
    success_url = '/templates'

class EditTemplate(UpdateView):
    """Edit Template"""
    model = SurveyTemplates
    form_class = CreateTemplateForm
    success_url = '/templates'

class DeleteTemplate(DeleteView):
    """Delete Template"""
    model = SurveyTemplates
    success_url = '/templates'


class GroupsView(ListView):
    template_name = "surveytemplate/groups.html"
    model = GroupName
    paginate_by = 5

class RecepientView(ListView):
    model= Recepient
    template_name = 'surveytemplate/participants.html'
    paginate_by = 5

class GroupView(ListView):
    template_name = "surveytemplate/groupview.html"
    paginate_by = 5

    def get_queryset(self):
        return Recepient.objects.filter(group = self.kwargs['pk'])
         

class UploadFiles(View):
    def get(self, request):
        return render(request, 'surveytemplate/upload.html')
    def post(self, request):
        my_f = request.FILES.getlist('my_files')
        print(my_f)
        for f in my_f:
            data = pd.read_excel(f)
            #print(data)
            print(data.shape)
            xx = []
            for i in data.index:
                xx.append(data['FirstName'][i])
                obj2, create = GroupName.objects.get_or_create(group_name = data['Group'][i])
                obj, created = Recepient.objects.get_or_create(email = data['Email'][i])
                if created == True:
                    obj.first_name = data['FirstName'][i]
                    obj.last_name = data['LastName'][i]
                    obj.email = data['Email'][i]
                    obj.address = data['Address'][i]
                    obj.is_active = data['Is_active'][i]
                    #obj2, create = GroupName.objects.get(group_name = row[6])
                    if create == True:
                        obj2.group_name = data['Group'][i]
                        obj2.save()
                        obj.group.add(obj2)
                        obj.save()
                    else:
                        obj.group.add(obj2)
                        obj.save()
                    print(obj,'##########')
                    print(xx)
                    messages.success(request, f"recepient {data['FirstName'][i]} added")
                    #return render(request, 'surveytemplate/upload.html')
                else:
                    print(len(xx),'!!!!!!!!!!!')
                    #obj.update('first_name', 'last_name', 'Address', 'is_active', )
                    Recepient.objects.filter(email = data['Email'][i]).update(first_name = data['FirstName'][i], last_name=data['LastName'][i], address=data['Address'][i], is_active=data['Is_active'][i])
                    obj.group.add(obj2)
                    # for recp in updated_recepients:
                    #     recp.group.add(obj2)
                    messages.warning(request, f"recepient {data['FirstName'][i]} already exists")
                    #return render(request, 'surveytemplate/upload.html')
        print(len(xx))
        return redirect('recepients')

class DownloadRecepients(View):
    def get(self, request):
        results = Recepient.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="recepient.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Address', 'Is_Active', 'Group'])
        for x in results:
            writer.writerow([x.first_name,  x.last_name, x.email, x.address, x.is_active, ','.join([x.group_name for x in x.group.all()]),])
        return response


# class SearchRecepients(View):  
#     # def get(self, request, *args, **kwargs):
#     #     #searched = request.GET.get('searched')
#     #     #pk = kwargs['pk']
#     #     #print(pk)
#     #     self.searched
#     #     print(type(self.searched))
#     #     if len(self.searched) != 0:
#     #         print('nothing to search')
#     #         recepients = Recepient.objects.filter(Q(first_name__icontains=self.searched) | Q(last_name__icontains=self.searched) | Q(address__icontains=self.searched) | Q(email__icontains=self.searched))
#     #         paginator = Paginator(recepients, 5)
#     #         page_number = request.GET.get('page')
#     #         page_obj = paginator.get_page(page_number)
#     #         print(page_obj.next_page_number)
#     #         return render (request, 'surveytemplate/participants.html', {'page_obj':page_obj} )
#     #     else:
#     #         messages.warning(request, "Enter some text to search")
#     #         return redirect("recepients")

#     def post(self, request, *args, **kwargs):
#         searched = request.POST.get('searched')
#         print(type(searched))
#         if len(searched) != 0:
#             print('nothing to search')
#             recepients = Recepient.objects.filter(Q(first_name__icontains=searched) | Q(last_name__icontains=searched) | Q(address__icontains=searched) | Q(email__icontains=searched))
#             paginator = Paginator(recepients, 5)
#             page_number = request.POST.get('page')
#             obj = paginator.get_page(page_number)
#             print(obj.next_page_number)
#             return render (request, 'surveytemplate/participants.html', {'page_obj':obj} )
#         else:
#             messages.warning(request, "Enter some text to search")
#             return redirect("recepients")

class SearchRecepients(ListView):
    model = Recepient
    template_name = 'surveytemplate/participants.html'
    paginate_by = 5
    #context_object_name = 'page_obj'
   

    def get_queryset(self):
        queryset = Recepient.objects.all()
        queryset = queryset.filter(Q(first_name__icontains=self.request.GET['searched']) | Q(last_name__icontains=self.request.GET['searched'] ) | Q(address__icontains=self.request.GET['searched'] ) | Q(email__icontains=self.request.GET['searched']))
        return queryset

    
class SelectTemplate(ListView):
   
    model = SurveyTemplates
    template_name = 'surveytemplate/selecttemplate.html'

    def post(self, request, *args, **kwargs):
        template = request.POST["template"]
        return redirect('selectgroups',template ) 
   


class SelectGroups(View):
    def get(self,request,*args, **kwargs):
        template_name = kwargs['template']
        return render(request,'surveytemplate/selectgroups.html',{'object_list':GroupName.objects.all()})
    
    def post(self,request,*args, **kwargs):
        #['Banks']
        list_of_input_groups=request.POST.getlist('group')
        template = kwargs['template']
        recipients = {}
        for group_id in list_of_input_groups:
            data = Recepient.objects.filter(group=group_id)
            for record in data:
                recipients[record.first_name]=record.email

        final_recipients = {}
        for key,value in recipients.items():
            if value not in final_recipients.values():
               final_recipients[key] = value
        
        res = EmailTask.delay(final_recipients,template)
        print(f"id={res.id}, state={res.state}, status={res.status}")
        
        return HttpResponse("Helloclear")

# celery -A SurveySystem worker -l info

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        # pass
        return render(request, "surveytemplate/register.html", context={"register_form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            print(uname,)
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.warning(
            request, "Unsuccessful registration. Invalid data or Username already exists.")
        form = RegisterForm()
        return render(request, "surveytemplate/register.html", context={"register_form": form})

class LoginRequestView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, template_name="surveytemplate/login.html", context={"login_form": form})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.warning(request, "Invalid username or password!!!")
                form = UserLoginForm()
                return render (request, 'surveytemplate/login.html', context={"login_form":form})
        else:
            messages.warning(request, "Invalid username or password!!!")
            form = UserLoginForm()
            return render (request, 'surveytemplate/login.html', context={"login_form":form})

class LogoutRequestView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("login")