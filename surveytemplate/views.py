
from re import template
from tokenize import group
from django.shortcuts import render
# from .models import SurveyTemplates
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from .forms import CreateTemplateForm, UserLoginForm, RegisterForm, CreateGroupForm, CreateRecepientForm, SurveyForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django_celery_results.models import TaskResult
from .models import Recepient, SurveyTemplates, GroupName, Survey
from django.views.generic import ListView, TemplateView
from django.utils.datastructures import MultiValueDictKeyError
import pandas as pd
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator
from .tasks import EmailTask
from datetime import datetime, timedelta
from surveytemplate.tasks import EmailTask
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.

class HomeView(View):
    """Home Page"""
    # template_name = "surveytemplate/index.html"
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'surveytemplate/index.html')
        else:
            return redirect('login')


class TemplateListView(ListView):
    """List all Templates"""
    model = SurveyTemplates
    template_name = "surveytemplate/listtemplate.html"
    def get_queryset(self):
        return SurveyTemplates.objects.filter(user = User.objects.get(username = self.request.user.username))
    

class CreateTemplate(CreateView):
    """Create Template"""
    model = SurveyTemplates
    form_class = CreateTemplateForm
    success_url = '/templates'
    def form_valid(self, form):
        user = User.objects.get(username= self.request.user.username)
        form.instance.user = user
        return super(CreateTemplate, self).form_valid(form)


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
    def get_queryset(self):
        return GroupName.objects.filter(user = User.objects.get(username = self.request.user.username))


class RecepientView(ListView):
    model= Recepient
    template_name = 'surveytemplate/participants.html'
    paginate_by = 5
    def get_queryset(self):
        print(User.objects.get(username=self.request.user.username))
        return Recepient.objects.filter(user = User.objects.get(username = self.request.user.username))



class GroupView(View):
    #template_name = "surveytemplate/groupview.html"
    #paginate_by = 5
    def get(self, request, *args, **kwargs):
        g_id = self.kwargs['pk']
        print(g_id)
        page_obj = Recepient.objects.filter(group = self.kwargs['pk']).filter(user= User.objects.get(username=self.request.user.username))
        g_name = GroupName.objects.get(id = g_id).group_name
        print(g_name)
        context = {'page_obj':page_obj, 'g_id':g_id, 'g_name':g_name}
        return render(request, 'surveytemplate/groupview.html', context)
    # def get_queryset(self):
    #     return  Recepient.objects.filter(group = self.kwargs['pk']).filter(user= User.objects.get(username=self.request.user.username))
  
         

class UploadFiles(View):
    def get(self, request, *args, **kwargs):
        g_id = self.kwargs['pk']
        return render(request, 'surveytemplate/upload.html', {'g_id':g_id})
    def post(self, request, *args, **kwargs):
        my_f = request.FILES.getlist('my_files')
        g_id = self.kwargs['pk']
        print(my_f)
        for f in my_f:
            data = pd.read_excel(f)
            #print(data)
            print(data.shape)
            xx = []
            for i in data.index:
                xx.append(data['FirstName'][i])
                g = GroupName.objects.get(id = self.kwargs['pk'])
                print(g)
                #obj2, create = GroupName.objects.get_or_create(group_name = data['Group'][i], user = User.objects.get(username=self.request.user.username))
                obj, created = Recepient.objects.get_or_create(email = data['Email'][i], user= self.request.user)
                if created == True:
                    obj.user = User.objects.get(username=self.request.user.username)
                    obj.first_name = data['FirstName'][i]
                    obj.last_name = data['LastName'][i]
                    obj.email = data['Email'][i]
                    obj.address = data['Address'][i]
                    obj.is_active = data['Is_active'][i]
                    #obj2, create = GroupName.objects.get(group_name = row[6])
                    # if create == True:
                    #     obj2.user = User.objects.get(username=self.request.user.username)
                    #     print(obj2.user)
                    #     obj2.group_name = data['Group'][i]
                    #     obj2.save()
                    #     obj.group.add(obj2)
                    #     obj.save()
                    # else:
                    #     obj.group.add(obj2)
                    #     obj.save()
                    obj.group.add(g)
                    obj.save()
                    print(obj,'##########')
                    print(xx)
                    messages.success(request, f"recepient {data['FirstName'][i]} added")
                    #return render(request, 'surveytemplate/upload.html')
                else:
                    print(len(xx),'!!!!!!!!!!!')
                    #obj.update('first_name', 'last_name', 'Address', 'is_active', )
                    Recepient.objects.filter(email = data['Email'][i]).filter(user=self.request.user).update(first_name = data['FirstName'][i], last_name=data['LastName'][i], address=data['Address'][i], is_active=data['Is_active'][i])
                    obj.group.add(g)
                    # for recp in updated_recepients:
                    #     recp.group.add(obj2)
                    messages.warning(request, f"recepient {data['FirstName'][i]} already exists")
                    #return render(request, 'surveytemplate/upload.html')
        print(len(xx))
        return HttpResponseRedirect(reverse('group-view', kwargs={'pk': g_id}))
        #return redirect('recepients')

class DownloadRecepients(View):
    def get(self, request, *args, **kwargs):
        g = GroupName.objects.get(id=self.kwargs['pk'])
        results = Recepient.objects.filter(user=request.user).filter(group=g)
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
        queryset = Recepient.objects.filter(user = self.request.user)
        queryset = queryset.filter(Q(first_name__icontains=self.request.GET['searched']) | Q(last_name__icontains=self.request.GET['searched'] ) | Q(address__icontains=self.request.GET['searched'] ) | Q(email__icontains=self.request.GET['searched']))
        return queryset

    
class SelectTemplate(ListView):
   
    # model = SurveyTemplates
    template_name = 'surveytemplate/selecttemplate.html'

    def post(self, request, *args, **kwargs):
        template = request.POST["template"]
        print(type(template))
        return redirect('selectgroups',template ) 
    def get_queryset(self):
        queryset = SurveyTemplates.objects.filter(user= self.request.user)
        return queryset


class SelectGroups(View):
    def get(self,request,*args, **kwargs):
        template_name = kwargs['template']
        return render(request,'surveytemplate/selectgroups.html',{'object_list':GroupName.objects.filter(user = self.request.user)})
    
    def post(self,request,*args, **kwargs):
        #['Banks']
        list_of_input_groups=request.POST.getlist('group')
        hours = int(request.POST.get('hours'))
        days = int(request.POST.get('days'))

        template = kwargs['template']
        recipients = {}
        for group_id in list_of_input_groups:
            data = Recepient.objects.filter(group=group_id).filter(user=self.request.user)
            for record in data:
                recipients[record.first_name]=record.email

        final_recipients = {}
        for key,value in recipients.items():
            if value not in final_recipients.values():
               final_recipients[key] = value
        
        current_user = str(self.request.user)
        print(current_user)
        
        tomorrow = datetime.utcnow() + timedelta(days = days,hours = hours ,minutes = 0,seconds = 0)
        x = EmailTask.apply_async((final_recipients,template, current_user),eta = tomorrow)
        print("-----------------------------------------------")
        print(x.status)
        print("-----------------------------------------------")
        
        return redirect('home')
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
            return redirect("home")
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

class TaskStatus(ListView):
    model = TaskResult
    template_name = 'surveytemplate/status.html'
    
class CreateGroup(CreateView):
    """Create Group"""
    model = GroupName
    form_class = CreateGroupForm
    success_url = '/groups'
    def form_valid(self, form):
        user = User.objects.get(username= self.request.user.username)
        form.instance.user = user
        return super(CreateGroup, self).form_valid(form)

class EditGroup(UpdateView):
    """Edit Group"""
    model = GroupName
    form_class = CreateGroupForm
    success_url = '/groups'

class DeleteGroup(DeleteView):
    """Delete Group"""
    model = GroupName
    success_url = '/groups' 

class DeleteRecepient(DeleteView):
    """Delete Recepient"""
    model = Recepient
    #success_url = '/recepients' 

    def get_success_url(self):
        return reverse( 'group-view', kwargs={'pk': self.kwargs['pk2']})

# class CreateRecepient(CreateView):
#     """Create Recepient"""
#     model = Recepient
#     form_class = CreateRecepientForm
#     success_url = '/groups'
    
#     def form_valid(self, form):
#         user = User.objects.get(username= self.request.user.username)
#         form.instance.user = user    
#         recp = Recepient(user=user)
#         g = GroupName.objects.get(id = self.kwargs['pk'])
#         recp.group.add(g)
#         recp.save()
#         return super(CreateRecepient, self).form_valid(form)
#     # def post(self, request, *args, **kwargs):
#     #     g = GroupName.objects.get(id = self.kwargs['pk'])
#     #     self.object = self.get_object()
#     #     #self.object.save()
#     #     self.object.group.add(g)
#     #     return redirect('groups')

class CreateRecepient(View):
    def post(self, request, *args, **kwargs):
        form = CreateRecepientForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['first_name']
            l_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            is_active = form.cleaned_data['is_active']
            obj = Recepient.objects.create(user=request.user,first_name=f_name, last_name=l_name, email=email, address=address,is_active=is_active)
            g = GroupName.objects.get(id = self.kwargs['pk'])
            obj.group.add(g)
            obj.save()
            print("hhhhhhhhhhhhhh")
            #return redirect('groups')
            return HttpResponseRedirect(reverse('group-view', kwargs={'pk': self.kwargs['pk']}))

    def get(self, request, *args, **kwargs):
        form = CreateRecepientForm()
        return render(request, 'surveytemplate/recepient_form.html',{'form':form})


class EditRecepient(UpdateView):
    """Edit Recepient"""
    model = Recepient
    form_class = CreateRecepientForm
    #success_url = '/recepients'

    def get_success_url(self):
        return reverse( 'group-view', kwargs={'pk': self.kwargs['pk2']})

class CreateSurvey(CreateView):
    """Create Survey"""
    model = Survey
    form_class = SurveyForm
    success_url = '/surveylist'
    def form_valid(self, form):
        user = User.objects.get(username= self.request.user.username)
        form.instance.user = user
        form.instance.created_by = user.username
        return super(CreateSurvey, self).form_valid(form)
    
class SurveyListView(ListView):
    """List all Surveys"""
    model = Survey
    template_name = "surveytemplate/listsurvey.html"
    def get_queryset(self):
        return Survey.objects.filter(user = User.objects.get(username = self.request.user.username))

class DeleteSurvey(DeleteView):
    """Delete Survey"""
    model = Survey
    success_url = '/surveylist' 

class EditSurvey(UpdateView):
    """Edit Survey"""
    model = Survey
    form_class = SurveyForm
    success_url = '/surveylist'
