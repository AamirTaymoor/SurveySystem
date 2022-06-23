from django.urls import path
from . import views

urlpatterns = [
    
    path('home/',views.HomeView.as_view(), name='home'),
    path('groups/',views.GroupsView.as_view(), name='groups'),
    path('templates/',views.TemplateListView.as_view(), name='templates'),
    path('create/',views.CreateTemplate.as_view(),name = 'create'),
    path('edit/<str:pk>/',views.EditTemplate.as_view(), name='edit'),
    path('delete/<str:pk>/', views.DeleteTemplate.as_view(),name = 'delete'),
    path('selecttemplate/',views.SelectTemplate.as_view(), name='selecttemplate'),
    path('selectgroups/<str:template>',views.SelectGroups.as_view(), name='selectgroups'),
    path('status/',views.TaskStatus.as_view(), name='taskstatus'),

    path('recepients/',views.RecepientView.as_view(), name='recepients'),
    path('groups/<int:pk>',views.GroupView.as_view(), name='group-view'),
    path('upload/<int:pk>',views.UploadFiles.as_view(), name='upload'),
    path('download/<int:pk>',views.DownloadRecepients.as_view(), name='download'),
    path('search/',views.SearchRecepients.as_view(), name='search'),
    path('login/',views.LoginRequestView.as_view(), name='login'),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('logout/',views.LogoutRequestView.as_view(), name='logout'),
    path('creategroup/',views.CreateGroup.as_view(),name = 'create-group'),
    path('editgroup/<int:pk>/',views.EditGroup.as_view(), name='edit-group'),
    path('deletegroup/<int:pk>/',views.DeleteGroup.as_view(), name='delete-group'),
    path('deleterecepient/<int:pk>/<int:pk2>',views.DeleteRecepient.as_view(), name='delete-recepient'),
    path('createrecepient/<int:pk>',views.CreateRecepient.as_view(),name = 'create-recepient'),
    path('editrecepient/<int:pk>/<int:pk2>',views.EditRecepient.as_view(),name = 'edit-recepient'),
    path('createsurvey/',views.CreateSurvey.as_view(),name = 'create-survey'),
    path('surveylist/',views.SurveyListView.as_view(),name = 'survey-list'),
    path('deletesurvey/<str:pk>',views.DeleteSurvey.as_view(),name = 'delete-survey'),
    path('editsurvey/<str:pk>',views.EditSurvey.as_view(),name = 'edit-survey'),

]
